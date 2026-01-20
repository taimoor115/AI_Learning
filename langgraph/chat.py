from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    return {"messages": ["Hi, This is a message from ChatBot Node"]}


def sampleNode(state: State):
    return {"messages": ["Hi, This is a message from Sample Node"]}


graph_bulder = StateGraph(State)

graph_bulder.add_node(
    "chatbot",
    chatbot,
)
graph_bulder.add_node(
    "sampleNode",
    sampleNode,
)
