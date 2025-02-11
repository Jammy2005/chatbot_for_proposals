from langgraph.graph import MessagesState
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama.llms import OllamaLLM


# Model to use: 
# llm = OllamaLLM(model="deepseek-r1:1.5b")
llm = ChatOpenAI(model = "gpt-4o")

# Chatbot Node
def chatbot(state: MessagesState):
    response = llm.invoke(state["messages"])
    state["messages"].append(response)
    return {"messages": state["messages"]}
    
# constructing the graph:
builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")

builder.add_edge("chatbot", END)

# gaining persistance (memory) through memorySaver and checkpointers
memory = MemorySaver()

config = {"configurable": {"thread_id": "1"}}

graph = builder.compile(checkpointer = memory)
