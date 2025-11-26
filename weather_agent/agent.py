from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
from pydantic import BaseModel, Field
from typing import Optional
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


class MyOutputModel(BaseModel):
    step: str = Field(
        ..., description="The ID of the step. Example: PLAN, TOOL, OUTPUT etc"
    )
    content: Optional[str] = Field(
        None, description="The optional string content for the step"
    )
    tool: Optional[str] = Field(None, description="The ID of the tool that called")
    input: Optional[str] = Field(
        None, description="The input of the function that LLM gives"
    )


def getWeatherLocation(city: str):
    """Get current temperature of a city using Open-Meteo API"""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if not data.get("results"):
            return f"City '{city}' not found."

        long = data["results"][0]["longitude"]
        lat = data["results"][0]["latitude"]

        weather_data = getWeatherData(long, lat)
        return weather_data.get("temperature", "No temperature found")

    return "Something went wrong with geocoding API."


def getWeatherData(long, lat):
    """Get weather data for specific coordinates"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("current_weather", {})

    return {}


available_tools = {"_getWeatherLocation": getWeatherLocation}

SYSTEM_PROMPT = """
You are an AI Assistant that resolves user queries using tools.
Follow the steps: START → PLAN → (TOOL call if needed) → OBSERVE → OUTPUT.

RULES:
- Always use JSON format strictly.
- Only run one step at a time.
- Wait for OBSERVE before continuing after TOOL call.

AVAILABLE TOOLS:
_getWeatherLocation(city:str) — Returns temperature of the city in Celsius.

JSON FORMAT EXAMPLES:

START:
{
  "step":"START",
  "content":"What is the weather of Lahore?"
}

PLAN:
{
  "step":"PLAN",
  "content":"User wants weather info of Lahore. We can use _getWeatherLocation tool."
}

TOOL CALL:
{
  "step":"PLAN",
  "tool":"_getWeatherLocation",
  "input":"Lahore"
}

OBSERVE (after calling tool):
{
  "step":"OBSERVE",
  "tool":"_getWeatherLocation",
  "input":"Lahore",
  "output":"35"
}

OUTPUT:
{
  "step":"OUTPUT",
  "content":"The weather in Lahore is 35°C."
}
"""

client = OpenAI()

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

user_query = input("Please give me your prompt please...👨‍💼 ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format=MyOutputModel,
        messages=message_history,
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    parsed = json.loads(raw_result)

    step = parsed.get("step")
    tool = parsed.get("tool")

    if step == "START":
        print("🤷‍♀️", parsed.get("content"))
        continue

    if step == "PLAN" and tool is None:
        print("🙌", parsed.get("content"))
        continue

    if tool is not None:
        tool_func = available_tools.get(tool)
        tool_input = parsed.get("input")

        print("🐱‍🏍 Calling tool:", {"tool": tool, "input": tool_input})

        result = tool_func(tool_input)
        print("🛠️ Tool output:", result)

        message_history.append(
            {
                "role": "developer",
                "content": json.dumps(
                    {
                        "step": "OBSERVE",
                        "tool": tool,
                        "input": tool_input,
                        "output": result,
                    }
                ),
            }
        )
        continue

    if step == "OUTPUT":
        print("😍", parsed.get("content"))
        break
