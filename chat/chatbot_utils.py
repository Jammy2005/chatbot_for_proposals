# chat/chatbot_utils.py
import sys
from langgraph.graph import MessagesState, StateGraph, START, END
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
# from langchain_ollama.llms import OllamaLLM  # if needed

load_dotenv()

# Initialize the LLM (using GPT-4 in your case)
llm = ChatOpenAI(model="gpt-4o")
# If needed, you could swap in OllamaLLM.

def chatbot(state: MessagesState):
    response = llm.invoke(state["messages"])
    state["messages"].append(response)
    return {"messages": state["messages"]}

def create_graph():
    """Construct and return the state graph for the chatbot."""
    builder = StateGraph(MessagesState)
    builder.add_node("chatbot", chatbot)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    return graph  # Removed the trailing comma
