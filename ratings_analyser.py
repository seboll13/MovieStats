"""This module provides functions to analyze IMDb ratings data."""

from sqlite3 import connect


POSITIVE_INT_ERR_MESSAGE = 'top_n must be a positive integer'


class RatingsAnalyser:
    """A class to analyse IMDb ratings data.
    """

    def __init__(self, db_name):
        self.conn = connect(db_name)
        self.cursor = self.conn.cursor()


    def __del__(self):
        self.conn.close()


    def get_top_ratings(self, top_n=10):
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
            f'''SELECT title, your_rating FROM imdb_ratings ORDER BY your_rating DESC LIMIT {top_n}'''
        ).fetchall()


    def get_movies_per_rating(self):
        """Gets the list of movies and/or TV shows for each rating.
        
        Returns
        ----------
        The list of movies and/or TV shows
        """
        return self.cursor.execute(
            '''SELECT your_rating, title FROM imdb_ratings
            GROUP BY your_rating ORDER BY your_rating DESC'''
        ).fetchall()


    def get_total_movie_watching_time(self, days=False):
        """Get the total watching time in hours/days. Filter is done on movies only.
        
        Parameters
        ----------
        days: if True, return the total watching time in days
        
        Returns
        ----------
        The total watching time in hours/days
        """
        movies = self.cursor.execute(
            '''SELECT runtime_mins FROM imdb_ratings WHERE title_type = 'movie' '''
        ).fetchall()
        total_time = sum(movie[0] for movie in movies)
        if days:
            return total_time / 60 / 24
        return total_time / 60


    def get_rating_differences(self):
        """Calculates the differences between personal ratings and IMDb ratings.
        
        Returns
        ----------
        The list of differences
        """
        return self.cursor.execute(
            '''SELECT title, your_rating - imdb_rating FROM imdb_ratings'''
        ).fetchall()


    # def get_favourite_genres(self, top_n=10, min_count=5):
    #     """Get the mean rating and the movie count for each genre.
        
    #     Parameters
    #     ----------
    #     top_n: the number of top-rated genres to return
    #     min_count: the minimum number of movies for a genre to be considered
    #         This helps reduce the influence of genres with very few movies
        
    #     Returns
    #     ----------
    #     The mean rating and the movie count for each genre
    #     """
    #     self.data[GENRES_COL] = self.data[GENRES_COL].str.split(',')
    #     ratings_expanded = self.data.explode(GENRES_COL)
    #     ratings_expanded[GENRES_COL] = ratings_expanded[GENRES_COL].str.strip() # remove whitespaces

    #     genre_stats = ratings_expanded.groupby(GENRES_COL).agg({
    #         RATING_COL: ['mean', 'count']
    #     }).reset_index()

    #     # Filter out genres with few movies
    #     genre_stats = genre_stats[genre_stats[TITLE_COL] >= min_count]

    #     top_genres = genre_stats.sort_values(by=RATING_COL, ascending=False).head(top_n)
    #     top_genres = top_genres.rename(columns = {
    #         RATING_COL: 'Average Rating',
    #         TITLE_COL: 'Movie Count'
    #     })
    #     return top_genres


    # def get_mean_rating_for_highest_directors(self, top_n=10):
    #     """Gets the mean personal rating for the top_n highest-rated directors

    #     Parameters
    #     ----------
    #     top_n: the number of entries to return
        
    #     Returns
    #     ----------
    #     The mean rating for each director
    #     """
    #     return self.cursor.execute(
    #         f'''SELECT directors, AVG(your_rating) FROM imdb_ratings
    #         GROUP BY directors ORDER BY AVG(your_rating) DESC LIMIT {top_n}'''
    #     ).fetchall()


    # def get_mean_rating_for_most_frequent_directors(self, top_n=10):
    #     """Gets the mean personal rating for the top_n directors with the most rated movies
        
    #     Parameters
    #     ----------
    #     top_n: the number of entries to return

    #     Returns
    #     ----------
    #     The mean rating for each director
    #     """
    #     return self.cursor.execute(
    #         f'''SELECT directors, AVG(your_rating) FROM imdb_ratings
    #         GROUP BY directors ORDER BY COUNT(directors) DESC LIMIT {top_n}'''
    #     ).fetchall()


    def get_mean_rating_for_highest_actors(self, top_n=10):
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


    def get_stats_for_most_frequent_actors(self, top_n=10):
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


    def get_movie_list_for(self, actor_name):
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
    