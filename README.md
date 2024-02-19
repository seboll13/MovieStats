# Movie and Show Statistics Analyser

## Overview
This project offers a comprehensive tool for analysing personal ratings of movies and shows, featuring a straightforward recommendation system. Utilising the `moviestats` package and `main.py` script, the program initialises a ratings database from `imdb_ratings.csv` and enriches it with detailed IMDb data, including cast and crew, upon first execution. Subsequent runs update the database to reflect any changes in the CSV.

## Components
- `ratings_analyser.py`: Manages databse connextions to compute statistics from user ratings.
- `imdb_fetcher.py`: Fetches detailed information from IMDb to complete database entries.
- `db_functions.py`: Handles database interations, such as table creation, data insertion, and queries.
- `plotting_utils.py`: Provides data visualisation capabilities.
- `helpers.py`: Includes various utility functions supporting data analysis.

## Recommendations
The `recommendations.py` module offers personalised movie suggestions based on user ratings. The algorithm is under development and currently simply gives the most possible genre combinations.

## Current Features
- Total movie watching time
- Top rated movies and shows
- The distribution of rating differences between IMDb and personal ratings
- Average rating for highest-rated actors and directors
- Movie list for a specific actor or director
- ... and more to come!

## Requirements
Before running the script, ensure you have the following requirements installed:
- Python 3.9 or higher
- pandas, matplotlib, numpy, sqlite3, imdbpy

## Getting Started
1. Navigate to the `Code` directory.
2. Run `python main.py` in your terminal.
3. Review the statistics and graphs output to the terminal.

Note: Ensure that the `imdb_ratings.csv` file is in the folder `Code/data/`. Please keep the csv file content as is to avoid any parsing error whilst executing the script. The file should contain the following columns: Const, Your Rating, Date Rated, Title, URL, Title Type, IMDb Rating, Runtime (mins), Year, Genres, Num Votes, Release Date, Directors.

## Development and Contributions
The project is actively being enhanced with new features. Contributions, suggestions, and feedback are welcome.

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute the code as you see fit.

## Contact
For any questions or suggestions, feel free to contact me at [seboll13@gmail.com](mailto:seboll13@gmail.com).