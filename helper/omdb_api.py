# helper/omdb_api.py

import requests
import logging
from helper.config import OMDB_API_KEY

def make_omdb_request(params):
    url = "http://www.omdbapi.com/"
    params["apikey"] = OMDB_API_KEY
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"[OMDb ERROR] Request failed: {e}")
        return None

def get_omdb_data(imdb_id):
    return make_omdb_request({"i": imdb_id})

def extract_ratings(omdb_json):
    imdb_rating = omdb_json.get("imdbRating")
    rt_rating = None
    for rating in omdb_json.get("Ratings", []):
        if rating["Source"] == "Rotten Tomatoes":
            rt_rating = rating["Value"]
            break
    return imdb_rating, rt_rating
