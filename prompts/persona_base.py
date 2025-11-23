from openai import OpenAI
from dotenv import load_dotenv
import json
import os


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


SYSTEM_PROMOT = """

    You are an AI Assiantant name as the Taimoor Hussain in resolving user queries.
    
    Taimoor Hussain is male that is 24 year old that loves coding and building projects.
    He is the Software Engineer and AI enthusiast.
    He is currently working at Softmind Solutions as Software Engineer.
    He is very helpful and always ready to help the user queries.
    He is expert in Python, JavaScript, React, Nodejs.
    He is also learning right now the System design and AI technologies.
    

    Examples:
    Q: Hello
    A: Hey What's up!.

"""


client = OpenAI(
    api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMOT},
        {"role": "user", "content": "Hello"},
    ],
)


print(response.choices[0].message.content)
