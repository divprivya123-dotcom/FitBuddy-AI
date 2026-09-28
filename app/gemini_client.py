from google import genai
import time


PRIMARY_MODEL = "gemini-3.1-flash-lite"
FALLBACK_MODEL = "gemini-3.8-flash"


def generate_content(client, prompt):
    """Use the required model and fall back when Gemini reports temporary load."""
    last_error = None
    for model in (PRIMARY_MODEL, FALLBACK_MODEL):
        for attempt in range(2):
            try:
                chat = client.chats.create(model=model)
                return chat.send_message(prompt)
            except Exception as error:
                if "API_KEY_INVALID" in str(error) or "API key not valid" in str(error):
                    raise RuntimeError(
                        "The GOOGLE_API_KEY is invalid. Create a new Gemini API key in Google AI Studio and update .env."
                    ) from error
                last_error = error
                if attempt == 0:
                    time.sleep(1)
    if (
        getattr(last_error, "status_code", None) == 503
        or getattr(last_error, "code", None) == 503
    ):
        raise RuntimeError(
            "Gemini is temporarily experiencing high demand. Please try again shortly."
        ) from last_error
    raise last_error
