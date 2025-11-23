from openai import OpenAI
from dotenv import load_dotenv
import json
import os


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


print("\n\n\n\n\n")
SYSTEM_PROMPT = """
    You are an AI Assistant in resolving user queries using the chain of thoughts.
    You work on Start, Plan and OUTPUT steps.
    You need to first PLAN that needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    
    
    RULES:
    - Stricly follow the give json format.
    - Only run one step at a time.
    - The sequence of the steps START (where user gives an input), PLAN (That can be multple times) and finally OUTPUT (which is going to be disabled to the user.)
    OUTPUT JSON FORMAT:
    
    {
        "step":"START" | "PLAN" | "OUTPUT",
        "content":"string"
    }
    
    Example: 
    
    START: Hey can solve 2+2 * 5 / 3 ?
    PLAN: {
        "step":"PLAN",
        "content": "Seems like user is interested in math problem"
        }
    PLAN: {
        "step":"PLAN",
        "content": "Looking at a problem we should solve it using the BODMAS rule."
        }
    PLAN: {
        "step":"PLAN",
        "content": "Yes BODMAS is the correct thing here to be done."
        }
     PLAN: {
        "step":"PLAN",
        "content": "Then we should do the multiplication first 2+10/3"
        }
     PLAN: {
        "step":"PLAN",
        "content": "Then we should do the division 2+3.33"
        }
     PLAN: {
        "step":"PLAN",
        "content": "Finally we should do the addition 2+3.33 = 5.33"
        }
    OUTPUT: {
        "step":"OUTPUT",
        "content": "The final result is 5.33"
    }
"""


client = OpenAI(
    api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)


message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

user_query = input("Please give me your prompt please...👨‍💼")
message_history.append({"role": "user", "content": user_query})


while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=message_history,
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🤷‍♀️", parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "PLAN":
        print("🙌", parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "OUTPUT":
        print("😍", parsed_result.get("content"))
        break
    break


print("\n\n\n\n\n")
