
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.5-flash"


def explain_bug(source_code, issue_message):

    if not API_KEY:
        return "Error: Gemini API key not found."

    prompt = f"""
You are a beginner-friendly Python bug explanation assistant.

Python Code:
{source_code}

Detected Issues:
{issue_message}

Instructions:
1. Explain each issue separately.
2. Use simple English.
3. Give one short sentence for each explanation.
4. Give one short sentence for each fix.
5. Avoid long paragraphs.
6. Do not repeat information.
7. Do not provide complete rewritten code.
8. Do not explain unrelated issues.

Use this format:

Issue: [Issue name]
Why: [One short sentence]
Fix: [One short sentence]
"""

    try:
        client = genai.Client(
            api_key=API_KEY,
            http_options={"timeout": 60000}
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return "Gemini could not explain the issues. Please try again."

    except Exception as error:

        message = str(error)

        if "429" in message or "RESOURCE_EXHAUSTED" in message:
            return "Gemini request limit reached. Try again after the quota resets."

        elif "504" in message or "DEADLINE_EXCEEDED" in message:
            return "Gemini timed out. Please try again."

        elif "503" in message or "UNAVAILABLE" in message:
            return "Gemini is temporarily busy. Please try again."

        else:
            return f"Gemini API Error: {message}"


if __name__ == "__main__":

    sample_code = """
def add_numbers(a, b):
    temp_value = 100
    return a + b
"""

    issue = "Unused variable 'temp_value'"

    print(explain_bug(sample_code, issue))
