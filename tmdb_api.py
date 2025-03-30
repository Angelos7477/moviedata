# tmdb_api.py

import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_now_playing_movies():
    url = f"{TMDB_BASE_URL}/movie/now_playing"
    params = {"api_key": TMDB_API_KEY, "region": "GR"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['results']

def get_movie_credits(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_movie_imdb_id(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/external_ids"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("imdb_id")

def get_director_imdb_link(person_id):
    url = f"{TMDB_BASE_URL}/person/{person_id}/external_ids"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    imdb_id = response.json().get('imdb_id')
    return f"https://www.imdb.com/name/{imdb_id}/" if imdb_id else None

def fetch_movies_with_directors():
    movies = get_now_playing_movies()
    results = []

    for movie in movies:
        print(f"📽️ Processing: {movie['title']}")
        credits = get_movie_credits(movie['id'])
        directors = [person for person in credits['crew'] if person['job'] == 'Director']

        enriched_directors = []
        for director in directors:
            imdb_link = get_director_imdb_link(director['id'])
            if not imdb_link:
                logging.warning(f"No IMDb link found for director: {director['name']}")
            enriched_directors.append({
                'id': director['id'],
                'name': director['name'],
                'imdb_link': imdb_link
            })

        results.append((movie, enriched_directors))
    return results
