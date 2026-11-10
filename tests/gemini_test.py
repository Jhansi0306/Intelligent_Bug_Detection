
import os
from dotenv import load_dotenv
from google import genai

print("Step 1: Loading API key...", flush=True)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key not found in .env")
    raise SystemExit

print("Step 2: API key loaded.", flush=True)

try:
    print("Step 3: Creating Gemini client...", flush=True)

    client = genai.Client(
        api_key=api_key,
        http_options={"timeout": 30000}
    )

    print("Step 4: Sending test request...", flush=True)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents="Reply with only: Gemini connection successful"
    )

    print("Step 5: Response received!", flush=True)
    print(response.text)

except Exception as error:
    print("Gemini Error:", repr(error))
