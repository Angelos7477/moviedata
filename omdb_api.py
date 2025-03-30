# omdb_api.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

def get_omdb_data(imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    try:
        return response.json()
    except Exception as e:
        print(f"[OMDb ERROR] Failed to parse JSON for IMDb ID {imdb_id}: {response.text}")
        return None

def extract_ratings(omdb_json):
    imdb_rating = omdb_json.get("imdbRating")
    rt_rating = None
    for rating in omdb_json.get("Ratings", []):
        if rating["Source"] == "Rotten Tomatoes":
            rt_rating = rating["Value"]
            break
    return imdb_rating, rt_rating
