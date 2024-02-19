"""The main file to run the program.

This file is used to run the program and display the results of the RatingsAnalyser object.
"""

from ratings_analyser import RatingsAnalyser
from helpers import format_genre_combinations_output
from plotting_utils import plot_movie_genre_combinations
from recommendations import get_movie_genre_combination_ratings
from db_functions import create_local_database, populate_database


def on_start():
    """The function to run when the program starts.

    Parameters
    ----------
    analyser: The RatingsAnalyzer object to use
    """
    create_local_database()
    populate_database()


if __name__ == '__main__':
    #on_start()
    analyser = RatingsAnalyser('imdb_ratings.db')

    movie_genre_combinations = get_movie_genre_combination_ratings(analyser)
    movie_3genre_combinations = [comb for comb in movie_genre_combinations if len(comb[0]) == 3]

    print(format_genre_combinations_output(movie_genre_combinations))
    plot_movie_genre_combinations(movie_3genre_combinations[:10])

    del analyser
