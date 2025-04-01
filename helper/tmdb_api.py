# helper/tmdb_api.py

import requests
import logging
from helper.config import TMDB_API_KEY

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def make_tmdb_request(endpoint, params=None):
    url = f"{TMDB_BASE_URL}/{endpoint}"
    if params is None:
        params = {}
    params["api_key"] = TMDB_API_KEY
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"[TMDB ERROR] Request to {url} failed: {e}")
        return None

def get_now_playing_movies():
    data = make_tmdb_request("movie/now_playing", {"region": "GR"})
    return data.get("results", []) if data else []

def get_movie_credits(movie_id):
    return make_tmdb_request(f"movie/{movie_id}/credits")

def get_movie_imdb_id(movie_id):
    data = make_tmdb_request(f"movie/{movie_id}/external_ids")
    return data.get("imdb_id") if data else None

def get_director_imdb_link(person_id):
    data = make_tmdb_request(f"person/{person_id}/external_ids")
    imdb_id = data.get("imdb_id") if data else None
    return f"https://www.imdb.com/name/{imdb_id}/" if imdb_id else None

def fetch_movies_with_directors():
    movies = get_now_playing_movies()
    results = []
    for movie in movies:
        print(f"📽️ Processing: {movie['title']}")
        credits = get_movie_credits(movie['id'])
        directors = [person for person in credits['crew'] if person['job'] == 'Director'] if credits else []
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
