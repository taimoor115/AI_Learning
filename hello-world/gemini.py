from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=["Hello"],
    
)

for chunk in response:
    if chunk.text:
        print(chunk.text, end="")