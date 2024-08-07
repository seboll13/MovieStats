"""This module contains helper functions for the RatingsAnalyser class.
"""

from functools import wraps
from time import perf_counter


MAX_GENRE_COMBINATIONS = 4


def timer(func) -> callable:
    """Prints the runtime of the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> callable:
        start = perf_counter()
        res = func(*args, **kwargs)
        end = perf_counter()
        print(f"Elapsed time of {func.__name__!r}: {(end - start):.3f} [s]")
        return res

    return wrapper


def format_basic_output(data: list) -> str:
    """Formats the output of the RatingsAnalyser object.

    Parameters
    ----------
    data : list
        The data to format

    Returns
    ----------
    str
        The formatted output
    """
    return "\n".join(
        [f"{idx+1}: {movie_tuple}" for idx, movie_tuple in enumerate(data)]
    )


def format_genre_combinations_output(data: list, top_n: int = 10) -> str:
    """Formats the output of the get_movie_genre_combination_ratings function.
        This function prints the top_n most popular genre combinations for each combination size.

    Parameters
    ----------
    data : list
        The data to format
    top_n : int
        The number of top entries to display for each combination

    Returns
    ----------
    str
        The formatted output
    """
    top_entries_by_length = {i: [] for i in range(1, MAX_GENRE_COMBINATIONS + 1)}

    for comb, rating in data:
        comb_length = len(comb)
        if comb_length <= MAX_GENRE_COMBINATIONS:
            top_entries_by_length[comb_length].append((comb, rating))
            top_entries_by_length[comb_length].sort(key=lambda x: -x[1])
            if len(top_entries_by_length[comb_length]) > top_n:
                top_entries_by_length[comb_length] = top_entries_by_length[comb_length][
                    :top_n
                ]

    formatted_output = ""
    for i in range(1, MAX_GENRE_COMBINATIONS + 1):
        formatted_output += f"###### Top {top_n} {i}-genre combinations ######\n"
        for idx, (comb, rating) in enumerate(top_entries_by_length[i], start=1):
            formatted_output += f"{idx+1}: {comb} - {rating:.2f}\n"
        formatted_output += "\n"

    return formatted_output


def compute_weighted_rating(v: int, R: float, C: float, m: int = 5) -> float:
    """Computes the weighted rating for a genre combination.
        Credit goes to IMDb for the formula.

    Parameters
    ----------
    v : int
        The number of votes
    R : float
        The average rating
    C : float
        The mean rating across all movies
    m : int
        The minimum number of votes required to be considered.
        5 is the default value

    Returns
    ----------
    The weighted rating
    """
    return (v / (v + m)) * R + (m / (v + m)) * C
