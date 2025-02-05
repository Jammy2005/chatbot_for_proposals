from pprint import pprint
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langchain_ollama.llms import OllamaLLM
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END, MessagesState

load_dotenv()
    
# model = OllamaLLM(model = "deepseek-r1:7b")
model = ChatOpenAI(model="gpt-4o", temperature=0) 

# define as tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# define model with tool
model_with_tools = model.bind_tools([multiply])

# using MessageState
class MessageState(MessagesState):
    pass

def tool_calling_model(state: MessagesState):
    # print(state)
    # print("XXXXXXXXXXXX")
    # print({"messages": [model_with_tools.invoke(state["messages"])]})
    # print("XXXXXXXXXXXX")
    # print(state)
    return {"messages": [model_with_tools.invoke(state["messages"])]}

def dummy(state: MessagesState):
    # print(state)
    # print("XXXXXXXXXXXX")
    return {"messages": state["messages"]}

def dummy2(state: MessagesState):
    # print(state)
    return {"messages": state["messages"]}

# building graph
builder = StateGraph(MessageState)
builder.add_node("tool_calling_model", tool_calling_model)
builder.add_node("dummy", dummy)
builder.add_node("dummy2", dummy2)
builder.add_edge(START, "tool_calling_model")
builder.add_edge("tool_calling_model", "dummy")
builder.add_edge("dummy", "dummy2")
builder.add_edge("dummy2", END)
# builder.add_edge("tool_calling_model", END)

graph = builder.compile()

messages = graph.invoke({"messages": HumanMessage(content='2 multiply by 3')})

for m in messages['messages']:
    # print(m.content)
    m.pretty_print()









    



