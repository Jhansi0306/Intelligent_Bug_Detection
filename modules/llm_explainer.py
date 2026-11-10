
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
You are an expert Python programming assistant.

Analyze the following code issue.

Source Code:
{source_code}

Detected Issue:
{issue_message}

Explain:
1. Why this issue occurs.
2. How it affects the program.
3. How to fix it.
4. Provide corrected code.

Use simple language.
"""

    try:
        client = genai.Client(
            api_key=API_KEY,
            http_options={"timeout": 30000}
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as error:
        return f"Gemini API Error: {error}"


if __name__ == "__main__":

    sample_code = """
def add_numbers(a, b):
    temp_value = 100
    return a + b
"""

    issue = "Unused variable 'temp_value'"

    print("======================================")
    print(" GEMINI AI BUG EXPLANATION")
    print("======================================")

    explanation = explain_bug(sample_code, issue)

    print(explanation)
