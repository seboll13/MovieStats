"""The main file to run the program.

This file is used to run the program and display the results of the RatingsAnalyser object.
"""

from statistics import fmean
from moviestats.db import MySQLDatabaseHandler

from moviestats.helpers import format_basic_output
from moviestats.ratings_analyser import RatingsAnalyser
from moviestats.db_functions import create_local_database, populate_database


def sqlite_on_start():
    """The function to run when the program starts.

    Parameters
    ----------
    analyser: The RatingsAnalyzer object to use
    """
    create_local_database()
    populate_database()


def sqlite_main():
    """Main function to run when using sqlite3 as the database.
    """
    sqlite_on_start()
    analyser = RatingsAnalyser('imdb_ratings.db')

    movie_list = analyser.get_movie_list_for('Morgan Freeman')
    print(format_basic_output(movie_list))
    print(f'Average rating : {fmean((m[1] for m in movie_list))}')

    del analyser


def mysql_on_start():
    """The function to run for MySQL database population when the program starts.
    """
    mysql_db = MySQLDatabaseHandler()

    mysql_db.create_db_tables()
    mysql_db.populate_database()

    del mysql_db


if __name__ == '__main__':
    #mysql_on_start()
    #sqlite_on_start()

    analyser = RatingsAnalyser('imdb_ratings.db')
    print(format_basic_output(analyser.get_top_ratings(10)))
    