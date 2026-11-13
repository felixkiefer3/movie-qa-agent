import os

import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "ES")


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
                "id": movie.get("id"),
                "title": movie.get("title"),
                "release_date": movie.get("release_date"),
                "rating": movie.get("vote_average"),
                "overview": movie.get("overview"),
            }
        return {"error": "No results found."}
    except requests.RequestException as e:
        return {"error": str(e)}


def get_streaming_platforms(movie_id: int, country: str = DEFAULT_COUNTRY) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
    headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        providers = response.json().get("results", {}).get(country, {})

        return {
            "streaming": [
                p.get("provider_name") for p in providers.get("flatrate", [])
            ],
            "rent": [p.get("provider_name") for p in providers.get("rent", [])],
            "buy": [p.get("provider_name") for p in providers.get("buy", [])],
        }
    except requests.RequestException as e:
        return {"error": str(e)}


def get_movie_credits(movie_id: int) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        cast = [c.get("name") for c in data.get("cast", [])[:5]]
        directors = [
            c.get("name") for c in data.get("crew", []) if c.get("job") == "Director"
        ]
        return {"cast": cast, "directors": directors}
    except requests.RequestException as e:
        return {"error": str(e)}


def get_similar_movies(movie_id: int) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar"
    headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        results = response.json().get("results", [])[:5]
        return {"similar_movies": [m.get("title") for m in results]}
    except requests.RequestException as e:
        return {"error": str(e)}


def get_now_playing(country: str = DEFAULT_COUNTRY) -> dict:
    url = f"https://api.themoviedb.org/3/movie/now_playing?region={country}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        results = response.json().get("results", [])[:5]
        return {"now_playing": [m.get("title") for m in results]}
    except requests.RequestException as e:
        return {"error": str(e)}
