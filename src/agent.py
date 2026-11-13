import os
from datetime import datetime  # NUEVO

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.api_client import (
    discover_movies_by_date,  # NUEVO
    get_movie_credits,
    get_now_playing,
    get_similar_movies,
    get_streaming_platforms,
    search_movie,
)

load_dotenv()
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "ES")
TODAY = datetime.now().strftime("%Y-%m-%d")  # NUEVO

client = genai.Client(http_options={"api_version": "v1beta"})

system_prompt = (
    "You are a concise movie expert. Use search_movie for general info. "
    "Use get_streaming_platforms to find where to watch a movie. "
    "Use get_movie_credits for actors and directors. "
    "Use get_similar_movies for classic recommendations based on a title. "
    "Use get_now_playing for movies currently in theaters. "
    f"Use discover_movies_by_date for movies in a specific time range. Today is {TODAY}. "
    "IMPORTANT: When asked for recommendations in theaters or specific dates based on a movie they like, "
    "read the overviews from the tool results and logically analyze which one shares themes with the user's favorite movie. "
    f"Default country code is '{DEFAULT_COUNTRY}' unless specified."
)

config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    tools=[
        search_movie,
        get_streaming_platforms,
        get_movie_credits,
        get_similar_movies,
        get_now_playing,
        discover_movies_by_date,  # NUEVO
    ],
    temperature=0.7,
)

chat_session = client.chats.create(model="gemini-2.5-flash", config=config)


def ask_movie_agent(user_query: str) -> str:
    response = chat_session.send_message(user_query)
    return response.text
