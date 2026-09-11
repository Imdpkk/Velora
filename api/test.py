import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.5-flash"   # Change this if needed

try:
    response = client.models.generate_content(
        model=MODEL,
        contents="Say hello in one sentence."
    )
    print("SUCCESS!")
    print(response.text)
except Exception as e:
    print("ERROR:")
    print(e)