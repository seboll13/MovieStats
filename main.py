"""The main file to run the program.

This file is used to run the program and display the results of the RatingsAnalyser object.
"""


from ratings_analyser import RatingsAnalyser
from db_functions import create_local_database, populate_database


def on_start():
    """The function to run when the program starts.

    Parameters
    ----------
    analyser: The RatingsAnalyzer object to use
    """
    create_local_database()
    populate_database()


def format_output(data: list) -> str:
    """Formats the output of the RatingsAnalyser object.

    Parameters
    ----------
    data: The data to format

    Returns
    ----------
    The formatted data
    """
    return '\n'.join([f'{idx+1}: {movie_tuple}' for idx,movie_tuple in enumerate(data)])


if __name__ == '__main__':
    on_start()

    analyser = RatingsAnalyser('imdb_ratings.db')
    
    # print('###### Total movie watching time ######')
    # print(f'{analyser.get_total_movie_watching_time(days=True)} days\n')
    # print('###### Top 10 movies/shows ######')
    # print(format_output(analyser.get_top_ratings()))
    # print()
    # print('###### Favourite actors ######')
    # print(format_output(analyser.get_stats_for_most_frequent_actors()))
    # print()
    # print('###### Rated Movies with Scarlett Johansson ######')
    # print(format_output(analyser.get_movie_list_for('Scarlett Johansson')))

    del analyser
