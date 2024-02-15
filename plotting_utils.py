import numpy as np
import matplotlib.pyplot as plt
from constants import RATING_COL, IMDB_RATING_COL, GENRES_COL


def draw_genre_histogram(top_genres, rating_col_name='Average Rating'):
    """Draw a horizontal bar plot of favourite genres with their associated title count.
    
    Parameters
    ----------
    top_genres: the DataFrame containing the top-rated genres
    """
    plt.figure(figsize=(10, 8))
    plt.barh(top_genres[GENRES_COL], top_genres[rating_col_name], color='skyblue')
    plt.xlabel(rating_col_name)
    plt.title('Top-Rated Genres')

    for index,value in enumerate(top_genres[rating_col_name]):
        plt.text(value, index, str(top_genres['Movie Count'].iloc[index]))

    plt.gca().invert_yaxis()
    plt.show()


def draw_scatter_plot(ratings):
    """Draw scatter plot of IMDb ratings vs. personal ratings
    """
    plt.scatter(ratings[IMDB_RATING_COL], ratings[RATING_COL])
    plt.xlabel(IMDB_RATING_COL)
    plt.ylabel(RATING_COL)
    plt.title('My Ratings vs. IMDb Ratings')
    plt.show()


def draw_scatter_plot_with_regression(ratings):
    """Draw scatter plot of IMDb ratings vs. personal ratings with regression line
    """
    x = ratings[IMDB_RATING_COL]
    y = ratings[RATING_COL]
    m, b = np.polyfit(x, y, 1)  # m = slope, b = intercept

    # Add regression line to scatter plot
    plt.scatter(x, y)
    plt.plot(x, m*x + b, color='red')  # regression line
    plt.xlabel(IMDB_RATING_COL)
    plt.ylabel(RATING_COL)
    plt.title('My Ratings vs. IMDb Ratings with Regression Line')
    plt.show()


def plot_rating_differences(ratings):
    """Plot the distribution of rating differences.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(ratings['Rating Difference'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution of Rating Differences (Your Rating - IMDb Rating)')
    plt.xlabel('Rating Difference')
    plt.ylabel('Frequency')
    plt.axvline(ratings['Rating Difference'].mean(), color='red', linestyle='dashed', linewidth=1)
    plt.text(
        ratings['Rating Difference'].mean(),
        plt.ylim()[1]*0.9,
        f'Mean: {ratings["Rating Difference"].mean():.2f}',
        color = 'red'
    )
    plt.grid(True)
    plt.show()
