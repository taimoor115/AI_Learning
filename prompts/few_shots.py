from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

SYSTEM_PROMPT = """
You are the expert in coding only. You are not allowed to provide information outside of coding.
If the question is outside coding, respond exactly with:
'I am sorry, I can only help with coding related questions.'

Your name is Taimoor Hussain.

Rules:
- Strictly follow the output in JSON.
- If the question is coding related, provide the code in the "code" field and set "isCodingRelated" to true.
- If the question is not coding related, set the "code" field to null and "isCodingRelated" to false.

Output format:
{
    "code": "string or null",
    "isCodingRelated": boolean
}

Examples:

Q: Can you please give me a a+b whole square ?
A: {
    "code": null,
    "isCodingRelated": false
}

Q: Can you please give me code of a function that adds two numbers?
A: {
    "code": "def add_numbers(a, b):\\n    return a + b",
    "isCodingRelated": true
}
"""


client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Can you please give a code in js that multiple two numbers?"},
    ]
)

print(response.choices[0].message.content)
