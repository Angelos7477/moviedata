MovieData - Cinema Movie Importer
=================================

Overview
--------
MovieData is a simple Python application that retrieves a list of movies currently in theaters in Greece using the TMDB API and enriches them with IMDb and Rotten Tomatoes ratings (via OMDb API). The data is stored in a PostgreSQL relational database.

Features:
- Fetches currently playing movies in Greece from TMDB
- Stores movie details: title, description, original title
- Retrieves and stores a list of directors for each movie
- Fetches and stores the IMDb link for each director (if available)
- Attempts to retrieve IMDb & Rotten Tomatoes ratings via OMDb
- Falls back to TMDB's vote_average when IMDb rating is missing
- Stores all data in a normalized PostgreSQL schema
- Includes a viewer script that displays sorted results by rating

---

Requirements
------------
- Python 3.8+
- PostgreSQL
- pip (Python package manager)
- TMDB API key (already included)
- OMDb API key (optional for extra ratings)

---

Setup Instructions
------------------

1. Clone the project or extract the files to your local machine. (https://github.com/Angelos7477/moviedata)

2. Install Python dependencies:

pip install -r requirements.txt


3. Create a PostgreSQL database (e.g., `moviedata`) and run the schema:

Use `schema.sql`:


4. Configure environment variables:

Copy the provided `.env.example` file and fill in your credentials:

An OMDb API key is optional, but recommended for enhanced ratings.
You can get one at http://www.omdbapi.com/apikey.aspx and set it in your `.env`.

---

How to Use
----------

1. To import the latest movies and their data into the database:

python movie_data_loader.py


This will:
- Clear the existing database content
- Fetch new movie data from TMDB
- Retrieve director info and external IMDb links
- Try to fetch IMDb/RT ratings from OMDb (if key is set)
- Log progress and store everything in PostgreSQL

2. To view the stored data:

python viewer.py


This will:
- Display each movie with its description, ratings, and directors
- Ratings marked with ~ indicate fallback to TMDB vote_average

---

Tools & Technologies
--------------------
- Python
- PostgreSQL
- TMDB API (https://developers.themoviedb.org/3)
- OMDb API (http://www.omdbapi.com/)
- `psycopg2` for PostgreSQL connection
- `requests` for API calls
- `dotenv` for secure configuration

---

Notes
-----
- If OMDb is not used or fails, the app logs the issue and falls back to TMDB's vote_average.
- The `imdb_rating_is_fallback` flag is stored in the DB to help distinguish data sources.
- The project can be extended to support genres, release dates, showtimes, etc.

---

Author: Angelos Georgakopoulos
