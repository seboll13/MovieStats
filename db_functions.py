import pandas as pd
from os import path
from sqlite3 import connect
from imdb_fetcher import IMDbDataFetcher


DB_NAME = 'imdb_ratings.db'
RATINGS_FILE = 'data/imdb_ratings.csv'


def create_ratings_table(cursor: connect) -> None:
    """Create a table to store IMDb ratings.
    """
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS imdb_ratings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            const TEXT UNIQUE,
            your_rating INTEGER,
            date_rated TEXT,
            title TEXT,
            url TEXT,
            title_type TEXT,
            imdb_rating REAL,
            runtime_mins INTEGER,
            year INTEGER,
            genres TEXT,
            num_votes INTEGER,
            release_date TEXT,
            directors TEXT,
            cast TEXT
        )'''
    )


def create_supplementary_table(cursor: connect, table_name: str, columns: list) -> None:
    """Create a table to store table_name elements.

    Parameters
    ----------
    cursor: The SQL cursor to use
    table_name: The name of the table to create
    columns: The columns to create in the table (must be of length 2)
    """
    if len(columns) != 2:
        raise ValueError('columns must be of length 2')
    cursor.execute(
        f'''CREATE TABLE IF NOT EXISTS {table_name}(
            {columns[0]} INTEGER PRIMARY KEY AUTOINCREMENT,
            {columns[1]} TEXT UNIQUE
        )'''
    )


def create_movie_relations_table(cursor: connect, table_name: str, columns: list) -> None:
    """Create a table to store the relationships between movies and other elements.

    Parameters
    ----------
    cursor: The SQL cursor to use
    table_name: The name of the table to create
    columns: The columns to create in the table (must be of length 2)
    """
    if len(columns) != 2:
        raise ValueError('columns must be of length 2')
    cursor.execute(
        f'''CREATE TABLE IF NOT EXISTS {table_name}(
            movie_id INTEGER,
            {columns[0]} INTEGER,
            FOREIGN KEY(movie_id) REFERENCES imdb_ratings(id),
            FOREIGN KEY({columns[0]}) REFERENCES {columns[1]}({columns[0]})
            UNIQUE(movie_id, {columns[0]})
        )'''
    )


def create_local_database(db_name: str = DB_NAME) -> None:
    """Create a local sqlite database to store IMDb ratings.
    """
    if not path.exists(db_name):
        conn = connect(db_name)
        cursor = conn.cursor()

        create_ratings_table(cursor)

        create_supplementary_table(cursor, 'actors', ['actor_id', 'name'])
        create_movie_relations_table(cursor, 'movie_actors', ['actor_id', 'actors'])

        create_supplementary_table(cursor, 'directors', ['director_id', 'name'])
        create_movie_relations_table(cursor, 'movie_directors', ['director_id', 'directors'])

        create_supplementary_table(cursor, 'genres', ['genre_id', 'name'])
        create_movie_relations_table(cursor, 'movie_genres', ['genre_id', 'genres'])

        conn.commit()
        conn.close()
        print('Database created successfully')
    else:
        print('Database already exists')


def add_actors_to_database(
    row: pd.Series,
    cursor: connect,
    fetcher: IMDbDataFetcher,
    movie_id: int
) -> None:
    """Add actors to the local sqlite database.

    Parameters
    ----------
    cursor: The SQL cursor to use
    fetcher: The IMDbDataFetcher object to use
    movie_id: The id of the movie to link the actors to
    """
    actors = fetcher.get_full_cast_and_crew(row['Const'])
    for actor in actors:
        cursor.execute(
            '''INSERT OR IGNORE INTO actors (name) VALUES (?)''', (actor,)
        ) # ensures each actors is added only once
        actor_id = cursor.execute(
            '''SELECT actor_id FROM actors WHERE name = ?''', (actor,)
        ).fetchone()[0]
        cursor.execute(
            '''INSERT OR IGNORE INTO movie_actors (
                movie_id, actor_id
            ) VALUES (?,?)''', (movie_id, actor_id)
        ) # links the movie to the actors


def add_genres_to_database(
    row: pd.Series,
    cursor: connect,
    movie_id: int
) -> None:
    """Add genres to the local sqlite database.

    Parameters
    ----------
    cursor: The SQL cursor to use
    movie_id: The id of the movie to link the genres to
    """
    genres = row['Genres'].split(',')
    for genre in genres:
        cursor.execute(
            '''INSERT OR IGNORE INTO genres (name) VALUES (?)''', (genre,)
        ) # ensures each genre is added only once
        genre_id = cursor.execute(
            '''SELECT genre_id FROM genres WHERE name = ?''', (genre,)
        ).fetchone()[0]
        cursor.execute(
            '''INSERT OR IGNORE INTO movie_genres (
                movie_id, genre_id
            ) VALUES (?,?)''', (movie_id, genre_id)
        ) # links the movie to the genres


def add_directors_to_database(
    row: pd.Series,
    cursor: connect,
    movie_id: int
) -> None:
    """Add directors to the local sqlite database.

    Parameters
    ----------
    cursor: The SQL cursor to use
    fetcher: The IMDbDataFetcher object to use
    movie_id: The id of the movie to link the directors to
    """
    if pd.isna(row['Directors']):
        return
    directors = row['Directors'].split(',')
    for director in directors:
        cursor.execute(
            '''INSERT OR IGNORE INTO directors (name) VALUES (?)''', (director,)
        ) # ensures each director is added only once
        director_id = cursor.execute(
            '''SELECT director_id FROM directors WHERE name = ?''', (director,)
        ).fetchone()[0]
        cursor.execute(
            '''INSERT OR IGNORE INTO movie_directors (
                movie_id, director_id
            ) VALUES (?,?)''', (movie_id, director_id)
        ) # links the movie to the directors


def populate_database(csv_ratings: str = RATINGS_FILE) -> None:
    """Populate the local sqlite database with IMDb ratings.
        This function will search for ratings that are not already in the database and add them.
    """
    conn = connect(DB_NAME)
    cursor = conn.cursor()
    fetcher = IMDbDataFetcher()
    ratings = pd.read_csv(csv_ratings)
    num_db_entries = cursor.execute('''SELECT COUNT(*) FROM imdb_ratings''').fetchone()[0]
    for _, row in ratings.iterrows():
        cursor.execute('''SELECT const FROM imdb_ratings WHERE const = ?''', (row['Const'],))
        data = cursor.fetchone()
        if not data:
            cursor.execute(
                '''INSERT INTO imdb_ratings (
                    const, your_rating, date_rated, title, url, title_type,
                    imdb_rating, runtime_mins, year, num_votes, release_date
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (
                    row['Const'], row['Your Rating'], row['Date Rated'], row['Title'], row['URL'],
                    row['Title Type'], row['IMDb Rating'], row['Runtime (mins)'], row['Year'],
                    row['Num Votes'], row['Release Date']
                )
            )
            movie_id = cursor.lastrowid
            add_actors_to_database(row, cursor, fetcher, movie_id)
            add_genres_to_database(row, cursor, movie_id)
            add_directors_to_database(row, cursor, movie_id)
    conn.commit()
    if cursor.execute('''SELECT COUNT(*) FROM imdb_ratings''').fetchone()[0] > num_db_entries:
        print('Database updated successfully')
    else:
        print('No new entries found')
    conn.close()
