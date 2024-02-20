import os
import pandas as pd
from pathlib import Path
from mysql.connector import connect, Error
from moviestats.imdb_fetcher import IMDbDataFetcher


RATINGS_FILE = Path(__file__).parent.resolve() / '../data/imdb_ratings.csv'


def create_db_connection():
    """Creates a connection to the database.

    Returns
    -------
    connection: The connection to the database
    """
    try:
        connection = connect(
            host='localhost',
            user='seboll13',
            password=os.environ.get('DB_PASSWORD'),
            database='title_ratings',
            port=3306
        )
        return connection
    except Error as e:
        print(e)
        return None


def create_ratings_table(connection) -> None:
    """Creates a table to store IMDb ratings.

    Parameters
    ----------
    connection: The MySQL connector to use
    """
    with connection.cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS imdb_ratings(
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                const TEXT NOT NULL,
                your_rating INTEGER,
                date_rated TEXT,
                title TEXT,
                url TEXT,
                title_type TEXT,
                imdb_rating REAL,
                runtime_mins INTEGER,
                year INTEGER,
                num_votes INTEGER,
                release_date TEXT
            )'''
        )


def create_supplementary_table(connection, table_name: str, columns: list) -> None:
    """Creates a table to store table_name elements.

    Parameters
    ----------
    connection: The MySQL connector to use
    table_name: The name of the table to create
    columns: The columns to create in the table (must be of length 2)
    """
    if len(columns) != 2:
        raise ValueError('columns must be of length 2')
    with connection.cursor() as cursor:
        cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS {table_name}(
                {columns[0]} INTEGER PRIMARY KEY AUTO_INCREMENT,
                {columns[1]} TEXT
            )'''
        )


def create_movie_relations_table(connection, table_name: str, columns: list) -> None:
    """Creates a table to store the relationships between movies and other elements.

    Parameters
    ----------
    connection: The MySQL connector to use
    table_name: The name of the table to create
    columns: The columns to create in the table (must be of length 2)
    """
    if len(columns) != 2:
        raise ValueError('columns must be of length 2')
    with connection.cursor() as cursor:
        cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS {table_name}(
                movie_id INTEGER,
                {columns[0]} INTEGER,
                PRIMARY KEY(movie_id, {columns[0]}),
                FOREIGN KEY(movie_id) REFERENCES imdb_ratings(id),
                FOREIGN KEY({columns[0]}) REFERENCES {columns[1]}({columns[0]})
            )'''
        )


def create_db_tables() -> None:
    """Creates the required tables to fit in the title_ratings database.
    """
    conn = create_db_connection()
    if conn:
        create_ratings_table(conn)
        create_supplementary_table(conn, 'actors', ['actor_id', 'name'])
        create_movie_relations_table(conn, 'movie_actors', ['actor_id', 'actors'])
        create_supplementary_table(conn, 'directors', ['director_id', 'name'])
        create_movie_relations_table(conn, 'movie_directors', ['director_id', 'directors'])
        create_supplementary_table(conn, 'genres', ['genre_id', 'name'])
        create_movie_relations_table(conn, 'movie_genres', ['genre_id', 'genres'])
        create_supplementary_table(conn, 'musicians', ['musician_id', 'name'])
        create_movie_relations_table(conn, 'movie_musicians', ['musician_id', 'musicians'])
        conn.commit()
        conn.close()
        print('Database created successfully')


def add_cast_to_db(
    row: pd.Series,
    connection,
    fetcher: IMDbDataFetcher,
    movie_id: int
) -> None:
    """Add actors to the titles database.

    Parameters
    ----------
    row: The target row to fetch the cast from
    connection: The MySQL connector to use
    fetcher: The IMDbDataFetcher object to use
    movie_id: The id of the movie to link the actors to
    """
    actors = fetcher.get_full_cast(row['Const'])
    for actor in actors:
        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO actors (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=name''', (actor.strip(),)
            )
            actor_id = cursor.execute(
                '''SELECT actor_id FROM actors WHERE name = %s''', (actor.strip(),)
            ).fetchone()[0]
            cursor.execute(
                '''INSERT INTO movie_actors (
                    movie_id, actor_id
                ) VALUES (%s,%s) ON DUPLICATE KEY UPDATE movie_id=movie_id''', (movie_id, actor_id)
            )


def add_genres_to_database(
    row: pd.Series,
    connection,
    movie_id: int
) -> None:
    """Add genres to the local sqlite database.

    Parameters
    ----------
    row: The target row to fetch the genres from
    connection: The MySQL connector to use
    movie_id: The id of the movie to link the genres to
    """
    genres = row['Genres'].strip().split(',') # strip() fixes whitespace issue
    for genre in genres:
        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO genres (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=name''', (genre,)
            )
            genre_id = cursor.execute(
                '''SELECT genre_id FROM genres WHERE name = %s''', (genre,)
            ).fetchone()[0]
            cursor.execute(
                '''INSERT INTO movie_genres (
                    movie_id, genre_id
                ) VALUES (%s,%s) ON DUPLICATE KEY UPDATE movie_id=movie_id''', (movie_id, genre_id)
            )


def add_directors_to_database(
    row: pd.Series,
    connection,
    fetcher: IMDbDataFetcher,
    movie_id: int
) -> None:
    """Add directors to the titles database.

    Parameters
    ----------
    row: The target row to fetch the directors from
    connection: The MySQL connector to use
    fetcher: The IMDbDataFetcher object to use
    movie_id: The id of the movie to link the directors to
    """
    directors = fetcher.get_directors(row['Const'])
    for director in directors:
        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO directors (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=name''', (director.strip(),)
            )
            director_id = cursor.execute(
                '''SELECT director_id FROM directors WHERE name = %s''', (director.strip(),)
            ).fetchone()[0]
            cursor.execute(
                '''INSERT INTO movie_directors (
                    movie_id, director_id
                ) VALUES (%s,%s) ON DUPLICATE KEY UPDATE movie_id=movie_id''', (movie_id, director_id)
            )


def add_musicians_to_database(
    row: pd.Series,
    connection,
    fetcher: IMDbDataFetcher,
    movie_id: int
) -> None:
    """Add musicians to the titles database.

    Parameters
    ----------
    row: The target row to fetch the musicians from
    connection: The MySQL connector to use
    fetcher: The IMDbDataFetcher object to use
    movie_id: The id of the movie to link the musicians to
    """
    musicians = fetcher.get_music_contributors(row['Const'])
    for musician in musicians:
        with connection.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO musicians (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=name''', (musician.strip(),)
            )
            musician_id = cursor.execute(
                '''SELECT musician_id FROM musicians WHERE name = %s''', (musician.strip(),)
            ).fetchone()[0]
            cursor.execute(
                '''INSERT INTO movie_musicians (
                    movie_id, musician_id
                ) VALUES (%s,%s) ON DUPLICATE KEY UPDATE movie_id=movie_id''', (movie_id, musician_id)
            )


def populate_database() -> None:
    """Populate the local sqlite database with IMDb ratings.
        This function will search for ratings that are not already in the database and add them.
    """
    conn = create_db_connection()
    cursor = conn.cursor()
    fetcher = IMDbDataFetcher()
    ratings = pd.read_csv(RATINGS_FILE)
    num_db_entries = cursor.execute('''SELECT COUNT(*) FROM imdb_ratings''').fetchone()[0]
    for _, row in ratings.iterrows():
        cursor.execute('''SELECT const FROM imdb_ratings WHERE const = %s''', (row['Const'],))
        data = cursor.fetchone()
        if not data:
            cursor.execute(
                '''INSERT INTO imdb_ratings (
                    const, your_rating, date_rated, title, url, title_type,
                    imdb_rating, runtime_mins, year, num_votes, release_date
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (
                    row['Const'], row['Your Rating'], row['Date Rated'], row['Title'], row['URL'],
                    row['Title Type'], row['IMDb Rating'], row['Runtime (mins)'], row['Year'],
                    row['Num Votes'], row['Release Date']
                )
            )
            movie_id = cursor.lastrowid
            add_cast_to_db(row, conn, fetcher, movie_id)
            add_genres_to_database(row, conn, movie_id)
            add_directors_to_database(row, conn, fetcher, movie_id)
    conn.commit()
    if cursor.execute('''SELECT COUNT(*) FROM imdb_ratings''').fetchone()[0] > num_db_entries:
        print('Database updated successfully')
    else:
        print('No new entries found')
    conn.close()
