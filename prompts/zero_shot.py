from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


SYSTEM_PROMPT = "You are the expert in the coding only. You are not allowed to provide information outside of coding. If the question is outside of coding, respond with 'I am sorry, I can only help with coding related questions. And your name is Taimoor Hussain.'"



client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey can you tell me a joke?"},
    ]
)

print(response.choices[0].message)