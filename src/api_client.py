import os

import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "ES")


def search_movie(query: str) -> dict:
    """
    Searches for a movie by title and returns its basic details.

    Args:
        query (str): The title of the movie to search for.

    Returns:
        dict: A dictionary containing id, title, release_date, rating, and overview, or an error message.
    """
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
    """
    Retrieves available streaming, rent, and buy platforms for a specific movie ID.

    Args:
        movie_id (int): The unique TMDB identifier for the movie.
        country (str, optional): The ISO 3166-1 alpha-2 country code. Defaults to DEFAULT_COUNTRY.

    Returns:
        dict: Lists of streaming, rent, and buy platforms, or an error message.
    """
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
    """
    Fetches the top cast and directors for a given movie ID.

    Args:
        movie_id (int): The unique TMDB identifier for the movie.

    Returns:
        dict: Lists of top cast members and directors, or an error message.
    """
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
    """
    Returns a list of classic similar movies based on a provided movie ID.

    Args:
        movie_id (int): The unique TMDB identifier for the movie.

    Returns:
        dict: A list of titles of similar movies, or an error message.
    """
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
    """
    Gets a list of movies currently playing in theaters with their overviews.

    Args:
        country (str, optional): The ISO 3166-1 alpha-2 country code. Defaults to DEFAULT_COUNTRY.

    Returns:
        dict: A list of dictionaries containing movie titles and overviews, or an error message.
    """
    url = f"https://api.themoviedb.org/3/movie/now_playing?region={country}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        results = response.json().get("results", [])[:5]
        return {
            "now_playing": [
                {"title": m.get("title"), "overview": m.get("overview")}
                for m in results
            ]
        }
    except requests.RequestException as e:
        return {"error": str(e)}


def discover_movies_by_date(start_date: str, end_date: str) -> dict:
    """
    Discovers movies released within a specific date range.

    Args:
        start_date (str): The start date in YYYY-MM-DD format.
        end_date (str): The end date in YYYY-MM-DD format.

    Returns:
        dict: A list of dictionaries containing movie titles and overviews, or an error message.
    """
    url = f"https://api.themoviedb.org/3/discover/movie?primary_release_date.gte={start_date}&primary_release_date.lte={end_date}&sort_by=popularity.desc"
    headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        results = response.json().get("results", [])[:20]
        return {
            "discovered_movies": [
                {"title": m.get("title"), "overview": m.get("overview")}
                for m in results
            ]
        }
    except requests.RequestException as e:
        return {"error": str(e)}
