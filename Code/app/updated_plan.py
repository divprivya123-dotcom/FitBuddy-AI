import os
from google import genai
from app.gemini_client import generate_content


def _client():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key or "your_gemini_api_key" in api_key.lower() or api_key == "YOUR_API_KEY_HERE":
        raise RuntimeError("Gemini API key is missing. Add GOOGLE_API_KEY to the .env file.")
    return genai.Client(api_key=api_key)


def update_workout_plan(original_plan, feedback):

    prompt = f"""
Update the following 7-day workout plan based on the user's feedback.

Original workout plan:
{original_plan}

User feedback:
{feedback}

Create a revised 7-day workout plan.

Keep the plan clear, practical, and organized by day.
Include warm-up, main workout, and cool-down/recovery guidance.
"""

    client = _client()
    response = generate_content(client, prompt)

    return response.text.strip()