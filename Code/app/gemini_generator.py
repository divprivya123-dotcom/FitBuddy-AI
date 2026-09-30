import os
from google import genai
from app.gemini_client import generate_content


def _client():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key or "your_gemini_api_key" in api_key.lower() or api_key == "YOUR_API_KEY_HERE":
        raise RuntimeError("Gemini API key is missing. Add GOOGLE_API_KEY to the .env file.")
    return genai.Client(api_key=api_key)


def generate_workout_gemini(age, weight, goal, intensity, username=""):

    prompt = f"""
Create a personalized 7-day fitness workout plan.

User details:
Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

For each of the 7 days, include:
- Warm-up (5-10 minutes)
- Main workout
- Exercises with sets and reps
- Cool-down or recovery tip

Make the plan clear and easy to follow.
"""

    client = _client()
    response = generate_content(client, prompt)

    return response.text.strip()