"""Utility functions for plotting data from the IMDb dataset.
"""


from statistics import fmean
import numpy as np
import matplotlib.pyplot as plt


def plot_favourite_genre_ratings_histogram(top_genres: list) -> None:
    """Draw a bar plot of favourite genres with their associated title count and average rating."""
    plt.figure(figsize=(12, 8))
    genres, counts, ratings = zip(*top_genres)
    indices = range(len(genres))

    plt.barh(indices, counts, color='skyblue', alpha=0.7, label='Movie Count')

    # Add average ratings as text next to the bars
    for i, (count, rating) in enumerate(zip(counts, ratings)):
        plt.text(count, i, f' {rating:.2f}', va='center', ha='left', color='black')

    plt.yticks(indices, genres)
    plt.xlabel('Movie Count')
    plt.title('Top-Rated Genres with Average Ratings')

    plt.show()


def plot_rating_difference_scatter(ratings: list) -> None:
    """Draw scatter plot of IMDb ratings vs. personal ratings

    Parameters
    ----------
    ratings: list of 3-tuples containing movie, IMDb rating and the personal rating
    """
    imdb_ratings = np.array([movie[1] for movie in ratings])
    personal_ratings = np.array([movie[2] for movie in ratings])
    slope, intercept = np.polyfit(imdb_ratings, personal_ratings, 1)

    reg_line = slope * imdb_ratings + intercept

    # Add regression line to scatter plot
    plt.scatter(imdb_ratings, personal_ratings)
    plt.plot(imdb_ratings, reg_line, color='red')  # regression line
    plt.xlabel('IMDb Rating')
    plt.ylabel('Personal Rating')
    plt.title('IMDb vs Personal Rating Differences incl. Regression Line')

    plt.show()


def plot_rating_difference_distribution(rating_differences: list) -> None:
    """Plot the distribution of rating differences.

    Parameters
    ----------
    rating_differences: list of 2-tuples with movie and the rating difference
    """
    rating_differences = [diff for _,diff in rating_differences]
    plt.figure(figsize=(10, 6))
    plt.hist(rating_differences, bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution of Rating Differences (Your Rating - IMDb Rating)')
    plt.xlabel('Rating Difference')
    plt.ylabel('Frequency')

    rmean = fmean(rating_differences)
    plt.axvline(rmean, color='red', linestyle='dashed', linewidth=1)
    plt.text(
        rmean,
        plt.ylim()[1]*0.9,
        f'Mean: {rmean:.2f}',
        color = 'red'
    )
    plt.grid(True)
    plt.show()
