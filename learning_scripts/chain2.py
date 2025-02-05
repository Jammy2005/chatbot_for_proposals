from pprint import pprint
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langchain_ollama.llms import OllamaLLM
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END, MessagesState


# using MessageState
class MessageState(MessagesState):
    pass

def dummy3(state: MessagesState):
    print(state)
    print("XXXXXXXXXXXX")
    return {"messages": "I am"}

def dummy(state: MessagesState):
    print(state)
    print(state["messages"])
    print("XXXXXXXXXXXX")
    return {"messages": "CHAD"}

def dummy2(state: MessagesState):
    print(state)
    return {"messages": state["messages"]}

# building graph
builder = StateGraph(MessageState)
builder.add_node("tool_calling_model", dummy3)
builder.add_node("dummy", dummy)
builder.add_node("dummy2", dummy2)
builder.add_edge(START, "tool_calling_model")
builder.add_edge("tool_calling_model", "dummy")
builder.add_edge("dummy", "dummy2")
builder.add_edge("dummy2", END)
# builder.add_edge("tool_calling_model", END)

graph = builder.compile()

messages = graph.invoke({"messages": HumanMessage(content='Hello')})

for m in messages['messages']:
    # print(m.content)
    # m.pretty_print()
    pass









    



