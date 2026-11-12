from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.api_client import search_movie

load_dotenv()

client = genai.Client(http_options={"api_version": "v1beta"})


def ask_movie_agent(user_query: str) -> str:
    system_prompt = (
        "You are a concise movie expert. Use the search tool to provide "
        "accurate movie information (plot, rating, release date) and add a brief interesting fact."
    )

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[search_movie],
        temperature=0.7,
    )

    chat = client.chats.create(model="gemini-2.5-flash", config=config)

    response = chat.send_message(user_query)
    return response.text
