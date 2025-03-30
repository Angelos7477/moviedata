# movie_data_loader.py (main entry point)

from dotenv import load_dotenv
import os
from tmdb_api import fetch_movies_with_directors, get_movie_imdb_id
from db import connect_db, clear_database, insert_movie_with_directors
from utils import print_summary, setup_logger
from omdb_api import get_omdb_data, extract_ratings

load_dotenv()

POSTGRES_CONFIG = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': os.getenv("DB_PORT", "5432")
}

def main():
    logger = setup_logger()
    logger.info("Starting movie data import...")
    try:
        conn = connect_db(POSTGRES_CONFIG)
        clear_database(conn)
        movies_with_directors = fetch_movies_with_directors()
        for movie, directors in movies_with_directors:
            imdb_rating = None
            rt_rating = None
            imdb_rating_is_fallback = False
            # Get IMDb ID from the first director’s IMDb link
            imdb_id = get_movie_imdb_id(movie['id'])  # ✅ This gets the *movie's* IMDb ID
            if imdb_id:
                logger.debug(f"IMDb ID: {imdb_id}")
                omdb_data = get_omdb_data(imdb_id)
                logger.debug(f"OMDb data for {imdb_id}: {omdb_data}")
                if omdb_data:
                    imdb_rating, rt_rating = extract_ratings(omdb_data)
                # Fallback: use TMDB's vote_average if IMDb rating is missing
                if (not imdb_rating or imdb_rating == "N/A") and movie.get("vote_average"):
                    imdb_rating = str(movie["vote_average"])
                    imdb_rating_is_fallback = True
                    logger.info(f"Used TMDB vote_average as fallback for {movie['title']}: {imdb_rating}")
                if not imdb_rating:
                    logger.warning(f"No IMDb rating found for {movie['title']} (IMDb ID: {imdb_id})")
                if not rt_rating:
                    logger.warning(f"No RT rating found for {movie['title']} (IMDb ID: {imdb_id})")
            logger.info(f"{movie['title']} - IMDb: {imdb_rating or 'N/A'}, RT: {rt_rating or 'N/A'}")
            insert_movie_with_directors(conn, movie, directors, imdb_rating, rt_rating, imdb_rating_is_fallback)
            logger.info(f"Imported: {movie['title']}")
        print_summary(movies_with_directors)
        conn.close()
    except Exception as e:
        logger.exception("An error occurred during movie import.")

if __name__ == "__main__":
    main()
