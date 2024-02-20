"""The main file to run the program.

This file is used to run the program and display the results of the RatingsAnalyser object.
"""

from statistics import fmean
from moviestats.helpers import format_basic_output
from moviestats.ratings_analyser import RatingsAnalyser
from moviestats.db_functions import create_local_database, populate_database


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

    movie_list = analyser.get_movie_list_for('Morgan Freeman')
    print(format_basic_output(movie_list))
    print(f'Average rating : {fmean((m[1] for m in movie_list))}')

    del analyser
