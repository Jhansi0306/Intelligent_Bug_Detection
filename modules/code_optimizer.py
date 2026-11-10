
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
You are an expert Python code optimization assistant.

Analyze the following Python source code:

{source_code}

Tasks:
1. Identify inefficient code.
2. Suggest performance improvements.
3. Improve code readability.
4. Identify unnecessary variables.
5. Suggest better coding practices.
6. Provide complete optimized Python code.

Explain each improvement in simple language.
Do not change the intended functionality.
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

        return response.text

    except Exception as error:

        error_message = str(error)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            return "Gemini AI is temporarily busy. Please try again later."

        elif "504" in error_message or "DEADLINE_EXCEEDED" in error_message:
            return "Gemini AI request timed out. Please try again."

        else:
            return f"Optimization Error: {error_message}"


if __name__ == "__main__":

    sample_code = """
def calculate_sum(numbers):
    total = 0

    for i in range(len(numbers)):
        total = total + numbers[i]

    return total


numbers = [10, 20, 30, 40, 50]
print(calculate_sum(numbers))
"""

    print("======================================")
    print(" AI CODE OPTIMIZATION SYSTEM")
    print("======================================")

    print("\nAnalyzing source code...")

    result = optimize_code(sample_code)

    print("\n======================================")
    print(" OPTIMIZATION RESULTS")
    print("======================================")

    print(result)
