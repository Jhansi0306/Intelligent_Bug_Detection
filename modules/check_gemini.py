
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key not found in .env")
else:
    try:
        response = requests.get(
            "https://generativelanguage.googleapis.com/v1beta/models",
            headers={"x-goog-api-key": api_key},
            timeout=20
        )

        print("HTTP Status:", response.status_code)

        if response.status_code == 200:
            models = response.json().get("models", [])
            print("Gemini API connection successful!")

            for model in models:
                if "generateContent" in model.get(
                    "supportedGenerationMethods", []
                ):
                    print("Available model:", model["name"])

        else:
            print("API response:", response.text[:500])

    except requests.RequestException as error:
        print("Connection failed:", error)
