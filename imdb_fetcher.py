from functools import wraps
from time import perf_counter
from imdb.imdb import IMDb


def timer(func) -> callable:
    """Prints the runtime of the decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> callable:
        start = perf_counter()
        res = func(*args, **kwargs)
        end = perf_counter()
        print(f'Elapsed time of {func.__name__!r}: {(end - start):.3f} [s]')
        return res
    return wrapper


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
