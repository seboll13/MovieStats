# Movie and Show Statistics Analyser

## Overview
The goal of this project is to provide a simple and easy-to-use tool to analyse personal ratings of movies and shows along with a simple recommending system.
The script `ratings_analyser.py` initiates a connection to a local database to retrieve the provided ratings and then computes various statistics based on the data. The main program `main.py` intially creates and populates the database based on a provided csv file. When populating, the `imdb_fetcher.py` script is used to fetch cast and crew information from IMDb since it is not provided by default in the csv file. The `imdb_fetcher.py` script uses the IMDbPY library to fetch the required information. Finally, `db_functions.py` contains all functions necessary to interact with the database.

## Recommendations
The `recommendations.py` module is used to provide movie recommendations based on the analysed IMDb ratings data. The recommendations are tailored to the user's preferences, which are inferred from the provided csv file of ratings. The recommendation algorithm considers multiple parameters, which are currently being tested and optimised for the best performance.

## Features
- Total watching time
- Top rated movies and shows
- The list of movies and shows for each rating
- The distribution of rating differences between IMDb and personal ratings
- Average rating for highest-rated actors and directors
- Movie count and average rating for most frequent actors
- Movie list for a specific actor or director

## Requirements
Before running the script, ensure you have the following requirements installed:
- Python 3.9 or higher
- pandas, matplotlib, numpy, sqlite3, imdbpy

## Usage
To use the script, simply type `python main.py` in your terminal. The script will output the statistics to the terminal.

Ensure that the `imdb_ratings.csv` file is in the folder `data/`. Please keep the csv file content as is to avoid any parsing error whilst executing the script. The file should contain the following columns: Const, Your Rating, Date Rated, Title, URL, Title Type, IMDb Rating, Runtime (mins), Year, Genres, Num Votes, Release Date, Directors.

## Development
The project is still in development and will be updated with new features and improvements over time.

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute the code as you see fit.

## Contact
For any questions or suggestions, feel free to contact me at [seboll13@gmail.com](mailto:seboll13@gmail.com).