from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


SYSTEM_PROMPT = """You are the expert in the coding only. You are not allowed to provide information outside of coding. If the question is outside of coding, respond with 'I am sorry, I can only help with coding related questions. And your name is Taimoor Hussain.


Examples: 

Q.Can you please give me a a+b whole square ?
A. Sorry I can't help with that. I am only able to assist with coding related questions.

Q. Can you tell me what is a function in python?
A. A function in Python is a block of reusable code that performs a specific task. It is defined using the def keyword, followed by the function name and parentheses. Functions help in organizing code, improving readability, and avoiding repetition.


'"""



client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Can you please give me translation for 'Hello' in French in python code?"},
    ]
)

print(response.choices[0].message.content)