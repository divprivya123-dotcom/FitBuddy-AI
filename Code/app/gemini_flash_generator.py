import os
from google import genai
from app.gemini_client import generate_content


def _client():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key or "your_gemini_api_key" in api_key.lower() or api_key == "YOUR_API_KEY_HERE":
        raise RuntimeError("Gemini API key is missing. Add GOOGLE_API_KEY to the .env file.")
    return genai.Client(api_key=api_key)


def generate_nutrition_tip_with_flash(goal):

    prompt = f"""
Give one short and practical nutrition or recovery tip
for a person whose fitness goal is: {goal}

Keep the answer simple and useful.
"""

    client = _client()
    response = generate_content(client, prompt)

    return response.text.strip()