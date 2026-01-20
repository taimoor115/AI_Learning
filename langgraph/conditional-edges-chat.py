from typing_extensions import TypedDict
from dotenv import load_dotenv
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

load_dotenv()

client = OpenAI()


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good_response: Optional[bool]


def evaluate_response(state: State) -> Literal["chatbot_gemini", "end_node"]:
    if True:
        return "end_node"
    return "chatbot_gemini"


def chatbot(state: State):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": state["user_query"]}],
    )

    state["llm_output"] = response.choices[0].message.content
    print("Chatbot response:", state["llm_output"])

    return state


def chatbot_gemini(state: State):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": state["user_query"]}],
    )

    state["llm_output"] = response.choices[0].message.content
    print("Chatbot response:", state["llm_output"])

    return state


def end_node(state: State):
    print("Final LLM Output:", state["llm_output"])
    return state


graph_bulder = StateGraph(State)


graph_bulder.add_node(
    "chatbot",
    chatbot,
)
graph_bulder.add_node(
    "chatbot_gemini",
    chatbot_gemini,
)
graph_bulder.add_node(
    "end_node",
    end_node,
)


graph_bulder.add_edge(START, "chatbot")
graph_bulder.add_conditional_edges("chatbot", evaluate_response)
graph_bulder.add_edge("chatbot_gemini", "end_node")
graph_bulder.add_edge(
    "end_node",
    END,
)


graph = graph_bulder.compile()


# Correct state initialization
updated_state = graph.invoke(State({"user_query": "Hi, What is 1+1?\n"}))

print("\n\n Final State:", updated_state)
