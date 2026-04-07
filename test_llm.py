import os
from google import genai

key = os.getenv("GEMINI_API_KEY")
print("Key length:", len(key) if key else "None")
if key:
    client = genai.Client(api_key=key)
    print("Client created")
