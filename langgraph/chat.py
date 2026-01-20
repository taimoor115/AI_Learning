from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    print("We are inside the chatbot node\n")
    return {"messages": ["Hi, This is a message from ChatBot Node\n"]}


def sampleNode(state: State):
    print("We are inside the sampleNode node\n")
    return {"messages": ["Hi, This is a message from Sample Node\n"]}


graph_bulder = StateGraph(State)

graph_bulder.add_node(
    "chatbot",
    chatbot,
)
graph_bulder.add_node(
    "sampleNode",
    sampleNode,
)


graph_bulder.add_edge(START, "chatbot")
graph_bulder.add_edge("chatbot", "sampleNode")
graph_bulder.add_edge("sampleNode", END)


graph = graph_bulder.compile()


updated_state = graph.invoke(
    State({"messages": ["Hi, This is a message from Initial State\n"]})
)

print("\n\n Final State:", updated_state)
