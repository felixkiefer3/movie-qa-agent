import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.api_client import get_streaming_platforms, search_movie

load_dotenv()
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "ES")

client = genai.Client(http_options={"api_version": "v1beta"})

system_prompt = (
    "You are a concise movie expert. Use search_movie for general info. "
    "If asked where to watch a movie, use get_streaming_platforms with the movie ID. "
    f"Default country code is '{DEFAULT_COUNTRY}' unless the user specifies otherwise."
)

config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    tools=[search_movie, get_streaming_platforms],
    temperature=0.7,
)

chat_session = client.chats.create(model="gemini-2.5-flash", config=config)


def ask_movie_agent(user_query: str) -> str:
    response = chat_session.send_message(user_query)
    return response.text
