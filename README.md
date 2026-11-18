# Movie QA Agent

A conversational AI agent that acts as a movie expert. It uses the Google Gemini API for reasoning and natural language processing, and the TMDB (The Movie Database) API to fetch real-time movie data, currently playing films, streaming platforms, and credits. The user interface is built with Streamlit and features real-time text streaming.

## Prerequisites

Before you begin, ensure you have the following requirements:
- [Python 3.12 or higher](https://www.python.org/downloads/) (if running locally).
- [Docker](https://docs.docker.com/get-docker/) (if running via containers).
- A Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey).
- A TMDB API Key from [The Movie Database](https://www.themoviedb.org/settings/api).

## Configuration

Create a file named `.env` in the root directory of the project. Add your API keys and default country code exactly as shown below. 

**Important:** Do not use quotes (`"`) around the values. Docker reads the `.env` file literally, and quotes will invalidate your API keys.

```text
GEMINI_API_KEY=your_gemini_api_key_here
TMDB_API_KEY=your_tmdb_api_key_here
DEFAULT_COUNTRY=ES
```

---

## Option 1: Local Execution (Without Docker)

Follow these steps to run the application directly on your machine.

1. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment:**
   * On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   * On macOS and Linux:
     ```bash
     source .venv/bin/activate
     ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application:**
   To ensure Python correctly identifies the project paths, run Streamlit as a Python module:
   ```bash
   python -m streamlit run src/app.py
   ```

5. **Access the web interface:**
   Open your web browser and navigate to `http://localhost:8501`.

---

## Option 2: Docker Execution

Follow these steps to run the application using a Docker container. You do not need Python installed on your machine for this method.

1. **Build the Docker image:**
   Open your terminal in the project's root directory and run:
   ```bash
   docker build -t movie-agent .
   ```

2. **Run the Docker container:**
   Start the container and inject your `.env` file so the application can access the API keys safely:
   ```bash
   docker run -p 8501:8501 --env-file .env movie-agent
   ```

3. **Access the web interface:**
   Open your web browser and navigate to `http://localhost:8501`.

## Usage

Once the application is running, simply type your movie-related questions in the chat interface. You can ask for recommendations based on dates, check what is currently playing in theaters, find out where a specific movie is streaming, or simply chat about your favorite films.