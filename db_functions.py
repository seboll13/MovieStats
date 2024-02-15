import pandas as pd
from os import path
from sqlite3 import connect
from imdb_fetcher import IMDbDataFetcher


DB_NAME = 'imdb_ratings.db'
RATINGS_FILE = 'imdb_ratings.csv'


def create_ratings_table(cursor: connect):
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


def create_actors_table(cursor: connect):
    """Create a table to store actors.
    """
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS actors(
            actor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )'''
    )


def create_movie_actors_table(cursor: connect):
    """Create a table to store the relationships between movies and actors.
    """
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS movie_actors(
            movie_id INTEGER,
            actor_id INTEGER,
            FOREIGN KEY(movie_id) REFERENCES imdb_ratings(id),
            FOREIGN KEY(actor_id) REFERENCES actors(actor_id)
            UNIQUE(movie_id, actor_id)
        )'''
    )


def create_local_database(db_name: str = DB_NAME):
    """Create a local sqlite database to store IMDb ratings.
    """
    if not path.exists(db_name):
        conn = connect(db_name)
        cursor = conn.cursor()

        create_ratings_table(cursor)
        create_actors_table(cursor)
        create_movie_actors_table(cursor)

        conn.commit()
        conn.close()
        print('Database created successfully')
    else:
        print('Database already exists')


def populate_database(csv_ratings: str = RATINGS_FILE):
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
                    const, your_rating, date_rated, title, url, title_type, imdb_rating,
                    runtime_mins, year, genres, num_votes, release_date, directors
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
                    row['Const'], row['Your Rating'], row['Date Rated'], row['Title'], row['URL'],
                    row['Title Type'], row['IMDb Rating'], row['Runtime (mins)'], row['Year'],
                    row['Genres'], row['Num Votes'], row['Release Date'], row['Directors']
                )
            )
            actors = fetcher.get_full_cast_and_crew(row['Const'])
            movie_id = cursor.lastrowid
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
    conn.commit()
    if cursor.execute('''SELECT COUNT(*) FROM imdb_ratings''').fetchone()[0] > num_db_entries:
        print('Database updated successfully')
    else:
        print('No new entries found')
    conn.close()
