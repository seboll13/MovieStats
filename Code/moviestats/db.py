import os
import pandas as pd
from pathlib import Path
from mysql.connector import connect, Error
from moviestats.imdb_fetcher import IMDbDataFetcher


RATINGS_FILE = Path(__file__).parent.resolve() / '../data/imdb_ratings.csv'


class MySQLDatabaseHandler:
    """A class to handle the MySQL database.
    
    This class initiates a connection with the previously created title_ratings MySQL database
    and creates the required tables to store IMDb ratings and their supplementary data."""
    def __init__(self):
        self.connection = self.create_db_connection()
        if self.connection:
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(buffered=True)
        else:
            raise ValueError('Connection to the database could not be established')


    def __del__(self):
        self.connection.close()


    def create_db_connection(self):
        """Creates a connection to the database.

        Returns
        -------
        connection: The connection to the database
        """
        try:
            connection = connect(
                host='localhost',
                user='root', #'seboll13',
                password='root', #os.environ.get('MOVIEDB_PASSWORD'),
                database='title_ratings',
                port=3306
            )
        except Error as e:
            print(e)
            return None
        return connection


    def create_ratings_table(self) -> None:
        """Creates a table to store IMDb ratings.

        Parameters
        ----------
        connection: The MySQL connector to use
        """
        self.cursor.execute(
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


    def create_supplementary_table(self, table_name: str, columns: list) -> None:
        """Creates a table to store table_name elements.

        Parameters
        ----------
        connection: The MySQL connector to use
        table_name: The name of the table to create
        columns: The columns to create in the table (must be of length 2)
        """
        if len(columns) != 2:
            raise ValueError('columns must be of length 2')
        self.cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS {table_name}(
                {columns[0]} INTEGER PRIMARY KEY AUTO_INCREMENT,
                {columns[1]} TEXT
            )'''
        )


    def create_movie_relations_table(self, table_name: str, columns: list) -> None:
        """Creates a table to store the relationships between movies and other elements.

        Parameters
        ----------
        connection: The MySQL connector to use
        table_name: The name of the table to create
        columns: The columns to create in the table (must be of length 2)
        """
        if len(columns) != 2:
            raise ValueError('columns must be of length 2')
        self.cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS {table_name}(
                movie_id INTEGER,
                {columns[0]} INTEGER,
                PRIMARY KEY(movie_id, {columns[0]}),
                FOREIGN KEY(movie_id) REFERENCES imdb_ratings(id),
                FOREIGN KEY({columns[0]}) REFERENCES {columns[1]}({columns[0]})
            )'''
        )


    def create_db_tables(self) -> None:
        """Creates the required tables to fit in the title_ratings database.
        """
        if self.connection:
            self.create_ratings_table()
            self.create_supplementary_table('actors', ['actor_id', 'name'])
            self.create_movie_relations_table('movie_actors', ['actor_id', 'actors'])
            self.create_supplementary_table('directors', ['director_id', 'name'])
            self.create_movie_relations_table('movie_directors', ['director_id', 'directors'])
            self.create_supplementary_table('genres', ['genre_id', 'name'])
            self.create_movie_relations_table('movie_genres', ['genre_id', 'genres'])
            self.create_supplementary_table('musicians', ['musician_id', 'name'])
            self.create_movie_relations_table('movie_musicians', ['musician_id', 'musicians'])
            self.connection.commit()
            print('Tables created successfully')


    def add_cast_to_db(
        self,
        row: pd.Series,
        fetcher: IMDbDataFetcher,
        movie_id: int
    ) -> None:
        """Add actors to the titles database.

        Parameters
        ----------
        row: The target row to fetch the cast from
        fetcher: The IMDbDataFetcher object to use
        movie_id: The id of the movie to link the actors to
        """
        actors = fetcher.get_full_cast(row['Const'])
        for actor in actors:
            self.cursor.execute(
                '''INSERT INTO actors (name) VALUES (%s)
                ON DUPLICATE KEY UPDATE name=name''', (actor.strip(),)
            )
            self.cursor.execute(
                '''SELECT actor_id FROM actors WHERE name = %s''', (actor.strip(),)
            )
            actor_id = self.cursor.fetchone()[0]
            self.cursor.execute(
                '''INSERT INTO movie_actors (
                    movie_id, actor_id
                ) VALUES (%s,%s) 
                ON DUPLICATE KEY UPDATE movie_id=movie_id''', (movie_id, actor_id)
            )


    def add_genres_to_database(
        self,
        row: pd.Series,
        movie_id: int
    ) -> None:
        """Add genres to the local sqlite database.

        Parameters
        ----------
        row: The target row to fetch the genres from
        movie_id: The id of the movie to link the genres to
        """
        genres = row['Genres'].strip().split(',') # strip() fixes whitespace issue
        for genre in genres:
            self.cursor.execute(
                '''INSERT INTO genres (name) VALUES (%s)
                ON DUPLICATE KEY UPDATE name=name''', (genre,)
            )
            self.cursor.execute(
                '''SELECT genre_id FROM genres WHERE name = %s''', (genre,)
            )
            genre_id = self.cursor.fetchone()[0]
            self.cursor.execute(
                '''INSERT INTO movie_genres (
                    movie_id, genre_id
                ) VALUES (%s,%s)
                ON DUPLICATE KEY UPDATE movie_id=movie_id''', (movie_id, genre_id)
            )


    def add_directors_to_database(
        self,
        row: pd.Series,
        fetcher: IMDbDataFetcher,
        movie_id: int
    ) -> None:
        """Add directors to the titles database.

        Parameters
        ----------
        row: The target row to fetch the directors from
        fetcher: The IMDbDataFetcher object to use
        movie_id: The id of the movie to link the directors to
        """
        directors = fetcher.get_directors(row['Const'])
        for director in directors:
            self.cursor.execute(
                '''INSERT INTO directors (name) VALUES (%s)
                ON DUPLICATE KEY UPDATE name=name''', (director.strip(),)
            )
            self.cursor.execute(
                '''SELECT director_id FROM directors WHERE name = %s''', (director.strip(),)
            )
            director_id = self.cursor.fetchone()[0]
            self.cursor.execute(
                '''INSERT INTO movie_directors (
                    movie_id, director_id
                ) VALUES (%s,%s)
                ON DUPLICATE KEY UPDATE movie_id=movie_id''', (movie_id, director_id)
            )


    def add_musicians_to_database(
        self,
        row: pd.Series,
        fetcher: IMDbDataFetcher,
        movie_id: int
    ) -> None:
        """Add musicians to the titles database.

        Parameters
        ----------
        row: The target row to fetch the musicians from
        fetcher: The IMDbDataFetcher object to use
        movie_id: The id of the movie to link the musicians to
        """
        musicians = fetcher.get_music_contributors(row['Const'])
        for musician in musicians:
            self.cursor.execute(
                '''INSERT INTO musicians (name) VALUES (%s)
                ON DUPLICATE KEY UPDATE name=name''', (musician.strip(),)
            )
            self.cursor.execute(
                '''SELECT musician_id FROM musicians WHERE name = %s''', (musician.strip(),)
            )
            musician_id = self.cursor.fetchone()[0]
            self.cursor.execute(
                '''INSERT INTO movie_musicians (
                    movie_id, musician_id
                ) VALUES (%s,%s)
                ON DUPLICATE KEY UPDATE movie_id=movie_id''', (movie_id, musician_id)
            )


    def populate_database(self) -> None:
        """Populate the local sqlite database with IMDb ratings.
            This function will search for ratings that are not already in the database and add them.
        """
        fetcher = IMDbDataFetcher()
        ratings = pd.read_csv(RATINGS_FILE)

        count_query = '''SELECT COUNT(*) FROM imdb_ratings'''
        self.cursor.execute(count_query)
        num_db_entries = self.cursor.fetchone()[0]

        for _, row in ratings.iterrows():
            self.cursor.execute(
                '''SELECT const FROM imdb_ratings WHERE const = %s''', (row['Const'],)
            )
            if not self.cursor.fetchone():
                values = (
                    row['Const'], row['Your Rating'], row['Date Rated'], row['Title'], row['URL'],
                    row['Title Type'], row['IMDb Rating'], row['Runtime (mins)'], row['Year'],
                    row['Num Votes'], row['Release Date']
                )
                values = tuple(None if pd.isna(v) else v for v in values)
                self.cursor.execute(
                    '''INSERT INTO imdb_ratings (
                        const, your_rating, date_rated, title, url, title_type,
                        imdb_rating, runtime_mins, year, num_votes, release_date
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (values)
                )
                movie_id = self.cursor.lastrowid
                self.add_cast_to_db(row, fetcher, movie_id)
                self.add_genres_to_database(row, movie_id)
                self.add_directors_to_database(row, fetcher, movie_id)
                self.add_musicians_to_database(row, fetcher, movie_id)
        self.connection.commit()

        self.cursor.execute(count_query)
        if self.cursor.fetchone()[0] > num_db_entries:
            print('Database updated successfully')
        else:
            print('No new entries found')


    def update_cast_for_missing_movies(self):
        """This function can be used to update missing cast and crew information for movies
            that already figure in the imdb_ratings table.
            
            This includes merely actor, director and musician information.
        """
        fetcher = IMDbDataFetcher()

        contributor_types = {
            'actors': ('get_full_cast', 'actors', 'movie_actors', 'actor_id'),
            'directors': ('get_directors', 'directors', 'movie_directors', 'director_id'),
            'musicians': ('get_music_contributors', 'musicians', 'movie_musicians', 'musician_id')
        }

        # Tentative query to select the movies for which we need to update cast and crew info
        # This query can be changed to your liking.
        self.cursor.execute('''SELECT id, const FROM imdb_ratings ORDER BY id ASC LIMIT 10''')
        movies_to_update = self.cursor.fetchall()

        for movie_id, const in movies_to_update:
            for _, (fetch_method, table_name, link_table, column_id) in contributor_types.items():
                contributors = getattr(fetcher, fetch_method)(const)
                for contributor_name in contributors:
                    # Check if the contributor already exists and get their ID, insert them if not
                    self.cursor.execute(
                        f'''SELECT {column_id} FROM {table_name} WHERE name = %s''', (contributor_name,)
                    )
                    contributor_id = self.cursor.fetchone()
                    if not contributor_id:
                        self.cursor.execute(
                            f'''INSERT INTO {table_name} (name) VALUES (%s)''', (contributor_name,)
                        )
                        contributor_id = self.cursor.lastrowid
                    else:
                        contributor_id = contributor_id[0]
                    # Link the contributor to the movie, avoiding duplicates
                    self.cursor.execute(
                        f'''INSERT IGNORE INTO {link_table} (movie_id, {column_id})
                        VALUES (%s, %s)''', (movie_id, contributor_id)
                    )
        self.connection.commit()
