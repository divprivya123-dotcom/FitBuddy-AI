from google import genai
import time


PRIMARY_MODEL = "gemini-3.8-flash"
FALLBACK_MODEL = "gemini-flash-lite-latest"


def generate_content(client, prompt):
    """Use the required model and fall back when Gemini reports temporary load."""
    primary_error = None
    for model in (PRIMARY_MODEL, FALLBACK_MODEL):
        for attempt in range(2):
            try:
                return client.models.generate_content(model=model, contents=prompt)
            except Exception as error:
                if "API_KEY_INVALID" in str(error) or "API key not valid" in str(error):
                    raise RuntimeError(
                        "The GOOGLE_API_KEY is invalid. Create a new Gemini API key in Google AI Studio and update .env."
                    ) from error
                primary_error = error
                if attempt == 0:
                    time.sleep(1)
    raise primary_error
