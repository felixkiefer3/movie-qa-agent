import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.api_client import (
    discover_movies_by_date,
    get_movie_credits,
    get_now_playing,
    get_similar_movies,
    get_streaming_platforms,
    search_movie,
)

load_dotenv()
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "ES")
TODAY = datetime.now().strftime("%Y-%m-%d")

client = genai.Client(http_options={"api_version": "v1beta"})

system_prompt = (
    "You are a concise movie expert. Use search_movie for general info. "
    "Use get_streaming_platforms to find where to watch a movie. "
    "Use get_movie_credits for actors and directors. "
    "Use get_similar_movies for classic recommendations based on a title. "
    "Use get_now_playing for movies currently in theaters. "
    f"Use discover_movies_by_date for movies in a specific time range. Today is {TODAY}. "
    "IMPORTANT: If the user asks for movies similar to X but restricted by a date or currently in theaters, "
    "DO NOT use get_similar_movies. You MUST use discover_movies_by_date or get_now_playing first, "
    "read their overviews, and logically analyze which ones share themes or broad genres with movie X. "
    "If no perfect match is found, suggest the closest options and explain why. "
    "CONVERSATION RULE: If the user greets you, asks how you are, or says thanks, respond politely and naturally as a friendly movie expert. DO NOT try to use any search tools for casual chit-chat. "
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
        discover_movies_by_date,
    ],
    temperature=0.7,
)

chat_session = client.chats.create(model="gemini-2.5-flash", config=config)


def ask_movie_agent(user_query: str) -> str:
    """
    Sends a query to the movie expert agent and returns the full text response.

    Args:
        user_query (str): The user's input question or prompt.

    Returns:
        str: The agent's complete text response.
    """
    response = chat_session.send_message(user_query)
    return response.text


def ask_movie_agent_stream(user_query: str):
    """
    Sends a query to the movie expert agent and yields the response as a stream.

    Args:
        user_query (str): The user's input question or prompt.

    Yields:
        str: Chunks of the agent's text response in real-time.
    """
    response = chat_session.send_message_stream(user_query)
    for chunk in response:
        if chunk.text:
            yield chunk.text
