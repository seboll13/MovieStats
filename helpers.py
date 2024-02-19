MAX_GENRE_COMBINATIONS = 4


def format_basic_output(data: list) -> str:
    """Formats the output of the RatingsAnalyser object.

    Parameters
    ----------
    data: The data to format

    Returns
    ----------
    The formatted data
    """
    return '\n'.join([f'{idx+1}: {movie_tuple}' for idx,movie_tuple in enumerate(data)])


def format_genre_combinations_output(data: list, top_n: int=10):
    """Formats the output of the get_movie_genre_combination_ratings function.
        This function prints the top_n most popular genre combinations for each combination size.

    Parameters
    ----------
    data: The data to format
    top_n: The number of entries to return

    Returns
    ----------
    All formatted comparisons.
    """
    top_entries_by_length = {i: [] for i in range(1, MAX_GENRE_COMBINATIONS+1)}

    for comb, rating in data:
        comb_length = len(comb)
        if comb_length <= MAX_GENRE_COMBINATIONS:
            top_entries_by_length[comb_length].append((comb, rating))
            top_entries_by_length[comb_length].sort(key=lambda x: -x[1])
            if len(top_entries_by_length[comb_length]) > top_n:
                top_entries_by_length[comb_length] = top_entries_by_length[comb_length][:top_n]

    formatted_output = ''
    for i in range(1, MAX_GENRE_COMBINATIONS+1):
        formatted_output += f'###### Top {top_n} {i}-genre combinations ######\n'
        for idx, (comb, rating) in enumerate(top_entries_by_length[i], start=1):
            formatted_output += f'{idx+1}: {comb} - {rating:.2f}\n'
        formatted_output += '\n'

    return formatted_output


def compute_weighted_rating(v: int, R: float, C: float, m: int=5) -> float:
    """Computes the weighted rating for a genre combination.
        Credit goes to IMDb for the formula.

    Parameters
    ----------
    v: The number of ratings
    R: The average rating
    C: The mean rating across the dataset
    m: The minimum number of ratings to consider, used to avoid outliers

    Returns
    ----------
    The weighted rating
    """
    return (v / (v + m)) * R + (m / (v + m)) * C