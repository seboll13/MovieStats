from imdb.imdb import IMDb
from moviestats.helpers import timer


class IMDbDataFetcher:
    """A class to fetch data from the IMDb database.
    """
    def __init__(self):
        self.ia = IMDb()


    @timer
    def get_full_cast_and_crew(self, movie_id: str) -> list[str]:
        """Get the full cast and crew of a movie or TV show by its IMDb ID.

        Parameters
        ----------
        movie_id: The IMDb ID of the movie or TV show

        Returns
        ----------
        The full cast and crew of the movie or TV show
        """
        return self.ia.full_cast_and_crew(movie_id).cast_name
