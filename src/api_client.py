import os

import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


def search_movie(query: str) -> dict:
    url = "https://api.themoviedb.org/3/search/movie"
    headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_API_KEY}"}
    params = {"query": query, "language": "en-US", "page": 1}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json().get("results", [])

        if results:
            movie = results[0]
            return {
                "title": movie.get("title"),
                "release_date": movie.get("release_date"),
                "rating": movie.get("vote_average"),
                "overview": movie.get("overview"),
            }
        return {"error": "No results found."}
    except requests.RequestException as e:
        return {"error": str(e)}
