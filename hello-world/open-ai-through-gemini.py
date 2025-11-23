from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are an expert in maths only. You are not allowed to provide information outside of maths. If the question is outside of maths, respond with 'I am sorry, I can only help with maths related questions.'"},
        {"role": "user", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Hello"
        }
    ]
)

print(response.choices[0].message)