import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def generate_report(prompt):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set."
        )

    try:
        client = genai.Client(api_key=api_key)

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
        )

        if not interaction.output_text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return interaction.output_text

    except Exception as error:
        raise RuntimeError(
            f"Gemini API request failed: {error}"
        ) from error