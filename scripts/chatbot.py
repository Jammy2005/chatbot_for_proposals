from langgraph.graph import MessagesState
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama.llms import OllamaLLM

load_dotenv()

# Model to use: 
# llm = OllamaLLM(model="deepseek-r1:7b")
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

graph = builder.compile(checkpointer = memory)

config = {"configurable": {"thread_id": "1"}}

# TODO: the 'data.type == "AIMessageChunk"', used may be concidered bad practice due to the hardcoded type,
# better to replace to mitigate this hard coded type perhaps using the visitor pattern.
if __name__ == "__main__":
    
    sys_msg = [SystemMessage(content = "You are a helpful assistant!")]
    state = {"messages": sys_msg}
    # running the chatbot in a loop
    while True:
        prompt = input("\nUser: ")
        if prompt.lower() in ["quit", "exit", "q"]:
            print("Good Bye!")
            break
        else:
            messages = HumanMessage(content = prompt)
            state["messages"].append(messages)
                
            for data, stream_mode in graph.stream(state, config=config, stream_mode="messages"):
                if data.type == "AIMessageChunk":
                    print (data.content, end="")
            
            
