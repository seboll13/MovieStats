"""A module to provide simple movie recommendations based on IMDb ratings data.
"""


from collections import defaultdict
from moviestats.helpers import compute_weighted_rating
from moviestats.ratings_analyser import RatingsAnalyser


def get_movie_genre_combination_ratings(analyser: RatingsAnalyser) -> list:
    """Gets useful metrics for each distinct movie genre combination.

    Parameters
    ----------
    analyser: The RatingsAnalyser object to use

    Returns
    ----------
    The # of times and the average rating for each genre combination
    """
    genre_combinations = defaultdict(list)

    for _, genres, rating in analyser.get_title_genre_ratings():
        genre_combinations[tuple(sorted(genres.split(',')))].append(rating)

    genre_combinations_avg_ratings = {
        comb: compute_weighted_rating(
            len(ratings), sum(ratings) / len(ratings), analyser.get_mean_rating()
        ) for comb, ratings in genre_combinations.items()
    }

    return sorted(
        genre_combinations_avg_ratings.items(),
        key=lambda x: x[1], reverse=True
    )
