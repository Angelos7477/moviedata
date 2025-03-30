# viewer.py

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_CONFIG = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': os.getenv("DB_PORT", "5432")
}

def fetch_movies_with_directors():
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cur = conn.cursor()
    query = """
        SELECT m.title, m.original_title, m.description, m.imdb_rating, m.rt_rating,
               m.imdb_rating_is_fallback, d.name, d.imdb_link
        FROM movies m
        JOIN movie_directors md ON m.id = md.movie_id
        JOIN directors d ON d.id = md.director_id
        ORDER BY m.title, d.name;
    """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    # Group directors by movie
    movie_dict = {}
    for title, original_title, description, imdb_rating, rt_rating, is_fallback, director_name, imdb_link in rows:
        if title not in movie_dict:
            movie_dict[title] = {
                'original_title': original_title,
                'description': description,
                'imdb_rating': imdb_rating,
                'rt_rating': rt_rating,
                'imdb_rating_is_fallback': is_fallback,
                'directors': []
            }
        movie_dict[title]['directors'].append((director_name, imdb_link))
    return movie_dict

def display_movies(movie_dict):
    print("\n🎬 Now Playing Movies:\n")
    sorted_movies = []
    for title, info in movie_dict.items():
        try:
            imdb_score = float(info["imdb_rating"]) if info["imdb_rating"] and info["imdb_rating"] != "N/A" else 0.0
        except ValueError:
            imdb_score = 0.0
        try:
            rt_score = float(info["rt_rating"].replace("%", "")) if info["rt_rating"] and info["rt_rating"] != "N/A" else 0.0
        except ValueError:
            rt_score = 0.0
        sorted_movies.append((imdb_score, rt_score, title, info))

    sorted_movies.sort(reverse=False)
    for imdb_score,rt_score, title, info in sorted_movies:
        print(f"\n🎬 Movie: {title}")
        print(f"   🎬 Original Title: {info['original_title']}")
        print(f"   📄 Description: {info['description']}")
        imdb = info.get('imdb_rating', 'N/A')
        if imdb != 'N/A' and info.get('imdb_rating_is_fallback'):
            imdb = f"~{imdb}"  # tilde to show it's a fallback from TMDB
        print(f"   ⭐ IMDb Rating: {imdb}")
        print(f"   🍅 Rotten Tomatoes: {info.get('rt_rating', 'N/A')}")
        print(f"   🎬 Directors:")
        for name, imdb_link in info['directors']:
            link = imdb_link if imdb_link else "No IMDb link"
            print(f"     - {name} ({link})")
        #print()

def main():
    movie_dict = fetch_movies_with_directors()
    if not movie_dict:
        print("No movie data found. Did you run the data importer?")
    else:
        display_movies(movie_dict)

if __name__ == "__main__":
    main()