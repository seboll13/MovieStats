"""This module provides functions to analyze IMDb ratings data.
"""

from sqlite3 import connect


POSITIVE_INT_ERR_MESSAGE = 'top_n must be a positive integer'


class RatingsAnalyser:
    """A class to analyse IMDb ratings data.
    """

    def __init__(self, db_name: str = 'data/imdb_ratings.db'):
        self.conn = connect(db_name)
        self.cursor = self.conn.cursor()


    def __del__(self):
        self.conn.close()


    def __len__(self) -> int:
        return self.cursor.execute('SELECT COUNT(*) FROM imdb_ratings').fetchone()[0]


    def get_top_ratings(self, top_n: int=10) -> list:
        """Gets the top_n personally highest-rated movies
        
        Parameters
        ----------
        top_n: the number of movies to return
        
        Returns
        ----------
        The top n movies by personal rating
        """
        if top_n < 1:
            raise ValueError(POSITIVE_INT_ERR_MESSAGE)
        return self.cursor.execute(
            f'''SELECT title, your_rating FROM imdb_ratings 
            ORDER BY your_rating DESC LIMIT {top_n}'''
        ).fetchall()


    def get_movies_per_rating(self) -> list:
        """Gets the list of movies and/or TV shows for each rating.
        
        Returns
        ----------
        The list of movies and/or TV shows
        """
        return self.cursor.execute(
            '''SELECT title, your_rating FROM imdb_ratings 
            GROUP BY your_rating ORDER BY your_rating DESC'''
        ).fetchall()


    def get_total_movie_watching_time(self, days: bool=False) -> float:
        """Get the total watching time in hours/days. Filter is done on movies only.
        
        Parameters
        ----------
        days: if True, return the total watching time in days
        
        Returns
        ----------
        The total watching time in hours/days
        """
        movies = self.cursor.execute(
            '''SELECT runtime_mins FROM imdb_ratings 
            WHERE title_type = 'movie' '''
        ).fetchall()
        total_time = sum(movie[0] for movie in movies)
        if days:
            return total_time / 60 / 24
        return total_time / 60


    def get_ratings(self) -> list:
        """Gets the list of IMDb and personal ratings.
        
        Returns
        ----------
        The list of ratings
        """
        return self.cursor.execute(
            '''SELECT title, your_rating, imdb_rating FROM imdb_ratings'''
        ).fetchall()


    def get_rating_differences(self) -> list:
        """Calculates the differences between personal ratings and IMDb ratings.
        
        Returns
        ----------
        The list of differences
        """
        return self.cursor.execute(
            '''SELECT title, your_rating - imdb_rating FROM imdb_ratings'''
        ).fetchall()


    def get_average_rating_by_genre(self) -> list:
        """Gets the average rating for each genre
        
        Returns
        ----------
        The average rating for each genre
        """
        return self.cursor.execute(
            '''SELECT TRIM(genres.name), AVG(ratings.your_rating) FROM imdb_ratings AS ratings
            JOIN movie_genres ON ratings.id = movie_genres.movie_id
            JOIN genres ON movie_genres.genre_id = genres.genre_id
            GROUP BY TRIM(genres.name) ORDER BY AVG(ratings.your_rating) DESC'''
        ).fetchall()


    def get_title_genre_ratings(self, is_movie: bool=True) -> list:
        """Gets the mean personal rating and list of corresponding genres for each movie or TV show

        Parameters
        ----------
        is_movie: if True, return only movies. Otherwise, return only TV shows or mini-series

        Returns
        ----------
        A list of tuples containing the mean rating and list of genres for each title
        """
        type_filter = "title_type='movie'" if is_movie else "(title_type='tvSeries' OR title_type='tvMiniSeries')"
        return self.cursor.execute(
            f'''SELECT title, your_rating, GROUP_CONCAT(genres.name) FROM imdb_ratings AS ratings
            JOIN movie_genres ON ratings.id = movie_genres.movie_id
            JOIN genres ON movie_genres.genre_id = genres.genre_id
            WHERE {type_filter} GROUP BY title ORDER BY title'''
        ).fetchall()


    def get_mean_rating_for_highest_directors(self, top_n=10):
        """Gets the mean personal rating for the top_n highest-rated directors

        Parameters
        ----------
        top_n: the number of entries to return
        
        Returns
        ----------
        The mean rating for each director
        """
        if top_n < 1:
            raise ValueError(POSITIVE_INT_ERR_MESSAGE)
        return self.cursor.execute(
            f'''SELECT directors.name, AVG(ratings.your_rating) FROM imdb_ratings AS ratings
            JOIN movie_directors ON ratings.id = movie_directors.movie_id
            JOIN directors ON movie_directors.director_id = directors.director_id
            GROUP BY directors.name ORDER BY AVG(your_rating) DESC LIMIT {top_n}'''
        ).fetchall()


    def get_stats_for_most_frequent_directors(self, top_n=10):
        """Gets the mean personal rating and count for the top_n directors with the most rated movies
        
        Parameters
        ----------
        top_n: the number of entries to return

        Returns
        ----------
        The mean rating and count for each director
        """
        if top_n < 1:
            raise ValueError(POSITIVE_INT_ERR_MESSAGE)
        return self.cursor.execute(
            f'''SELECT directors.name, COUNT(ratings.id), AVG(ratings.your_rating)
            FROM imdb_ratings AS ratings
            JOIN movie_directors ON ratings.id = movie_directors.movie_id
            JOIN directors ON movie_directors.director_id = directors.director_id
            GROUP BY directors.name ORDER BY COUNT(ratings.id) DESC LIMIT {top_n}'''
        ).fetchall()


    def get_mean_rating_for_highest_actors(self, top_n :int=10) -> list:
        """Gets the mean personal rating for the top_n highest-rated actors
        
        Parameters
        ----------
        top_n: the number of entries to return
        
        Returns
        ----------
        The mean rating for each actor
        """
        if top_n < 1:
            raise ValueError(POSITIVE_INT_ERR_MESSAGE)
        return self.cursor.execute(
            f'''SELECT actors.name, AVG(ratings.your_rating) FROM imdb_ratings AS ratings
            JOIN movie_actors ON ratings.id = movie_actors.movie_id
            JOIN actors ON movie_actors.actor_id = actors.actor_id
            GROUP BY actors.name ORDER BY AVG(your_rating) DESC LIMIT {top_n}'''
        ).fetchall()


    def get_stats_for_most_frequent_actors(self, top_n :int=10) -> list:
        """Gets the mean personal rating and count for the top_n actors with the most rated movies
        
        Parameters
        ----------
        top_n: the number of entries to return
        
        Returns
        ----------
        The mean rating and movie count for each actor
        """
        if top_n < 1:
            raise ValueError(POSITIVE_INT_ERR_MESSAGE)
        return self.cursor.execute(
            f'''SELECT actors.name, COUNT(ratings.id), AVG(ratings.your_rating)
            FROM imdb_ratings AS ratings
            JOIN movie_actors ON ratings.id = movie_actors.movie_id
            JOIN actors ON movie_actors.actor_id = actors.actor_id
            GROUP BY actors.name ORDER BY COUNT(ratings.id) DESC LIMIT {top_n}'''
        ).fetchall()


    def get_movie_list_for(self, actor_name: str) -> list:
        """Gets the list of movies and/or TV shows for a given actor.
        
        Parameters
        ----------
        actor_name: the name of the actor
        
        Returns
        ----------
        The list of movies and/or TV shows
        """
        return self.cursor.execute(
            '''SELECT title, your_rating FROM imdb_ratings
            JOIN movie_actors ON imdb_ratings.id = movie_actors.movie_id
            JOIN actors ON movie_actors.actor_id = actors.actor_id
            WHERE actors.name = ?''', (actor_name,)
        ).fetchall()
    