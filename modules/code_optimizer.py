
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.5-flash"


def optimize_code(source_code):

    if not API_KEY:
        return "Error: Gemini API key not found."

    prompt = f"""
You are a beginner-friendly Python code optimization assistant.

Python Code:
{source_code}

Instructions:

1. Give a maximum of 5 useful suggestions.
2. Each suggestion must be one short sentence.
3. Use simple English.
4. Avoid long paragraphs.
5. Do not repeat suggestions.
6. Suggest only improvements relevant to this code.
7. Preserve the original functionality.
8. Provide the complete optimized Python code.
9. Do not add unnecessary explanations.

Use this format:

SUGGESTIONS:
- Short suggestion 1.
- Short suggestion 2.
- Short suggestion 3.

OPTIMIZED CODE:
Provide complete Python code inside a python code block.
"""

    try:
        client = genai.Client(
            api_key=API_KEY,
            http_options={"timeout": 90000}
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return "Gemini could not optimize the code. Please try again."

    except Exception as error:

        message = str(error)

        if "429" in message or "RESOURCE_EXHAUSTED" in message:
            return "Gemini request limit reached. Try again after the quota resets."

        elif "504" in message or "DEADLINE_EXCEEDED" in message:
            return "Gemini optimization timed out. Please try again."

        elif "503" in message or "UNAVAILABLE" in message:
            return "Gemini is temporarily busy. Please try again."

        else:
            return f"Optimization Error: {message}"


if __name__ == "__main__":

    sample_code = """
def calculate_sum(numbers):
    total = 0

    for i in range(len(numbers)):
        total = total + numbers[i]

    return total

print(calculate_sum([10, 20, 30, 40, 50]))
"""

    print(optimize_code(sample_code))
