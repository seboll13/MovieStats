from imdb.imdb import IMDb
from moviestats.helpers import timer


class IMDbDataFetcher:
    """A class to fetch data from the IMDb database.
    """
    def __init__(self):
        self.ia = IMDb()


    @timer
    def get_full_cast(self, movie_id: str) -> list[str]:
        """Get the full cast of a movie or TV show by its IMDb ID.

        Parameters
        ----------
        movie_id: The IMDb ID of the movie or TV show

        Returns
        ----------
        The full cast of the title
        """
        return self.ia.full_cast_and_crew(movie_id).cast_name


    @timer
    def get_directors(self, movie_id: str) -> list[str]:
        """Get the list of directors of a movie or TV show by its IMDb ID.

        Parameters
        ----------
        movie_id: The IMDb ID of the movie or TV show

        Returns
        ----------
        The list of directors of the title
        """
        return self.ia.full_cast_and_crew(movie_id).directors_name


    @timer
    def get_music_contributors(self, movie_id: str) -> list[str]:
        """Get the list of music contributors of a movie or TV show by its IMDb ID.

        Parameters
        ----------
        movie_id: The IMDb ID of the movie or TV show

        Returns
        ----------
        The list of music contributors of the title
        """
        return self.ia.full_cast_and_crew(movie_id).music_name
