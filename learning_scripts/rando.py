# from langgraph.graph import MessagesState, StateGraph, START, END
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, SystemMessage
# from langgraph.checkpoint.memory import MemorySaver

# load_dotenv()

# # Initialize LLM
# llm = ChatOpenAI(model="gpt-4o")

# # Define the chatbot function
# def chatbot(state: MessagesState):
#     response = llm.invoke(state["messages"])
#     state["messages"].append(response)
#     return {"messages": state["messages"]}

# # Build the graph
# builder = StateGraph(MessagesState)
# builder.add_node("chatbot", chatbot)
# builder.add_edge(START, "chatbot")
# builder.add_edge("chatbot", END)

# # Compile with MemorySaver checkpointer
# memory = MemorySaver()
# graph = builder.compile(checkpointer=memory)

# # Initialize state with a system message and user input
# initial_state = {
#     "messages": [
#         SystemMessage(content="You are a helpful assistant!"),
#         HumanMessage(content="What is the capital of Australia?")
#     ]
# }

# # Required configuration for checkpointer
# config = {"configurable": {"thread_id": "1"}}

# # Stream messages and unpack the event tuples
# for stream_mode, data in graph.stream(initial_state, config=config, stream_mode="messages"):
#     if stream_mode == "messages":
#         # Access and print the latest message content
#         ai_message = data[-1]  # Last message chunk
#         print(ai_message.content)


# from typing_extensions import TypedDict
# from typing import Literal
# from langgraph.graph import StateGraph, START, END
# from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv

# load_dotenv()

# class TypedDictState(TypedDict):
#     foo: str
#     bar: str
    
# class TypedDictState(TypedDict):
#     name: str
#     mood: Literal["happy", "sad"]
    
# def node_1(state):
#     print("---Node 1---")
#     return {"name": state['name'] + " is ... "}

# def node_2(state):
#     print("---Node 2---")
#     return {"mood": "happy"}

# def node_3(state):
#     print("---Node 3---")
#     return {"mood": "sad"}

# def decide_mood(state) -> Literal["node_2", "node_3"]:
        
#     # Here, let's just do a 50 / 50 split between nodes 2, 3
#     if random.random() < 0.5:

#         # 50% of the time, we return Node 2
#         return "node_2"
    
#     # 50% of the time, we return Node 3
#     return "node_3"
    
    
# builder = StateGraph(TypedDictState)

# builder.add_node("node_1", node_1)
# builder.add_node("node_2", node_2)
# builder.add_node("node_3", node_3)

# # Logic
# builder.add_edge(START, "node_1")
# builder.add_conditional_edges("node_1", decide_mood)
# builder.add_edge("node_2", END)
# builder.add_edge("node_3", END)

# # Add
# graph = builder.compile()

# messages = [AIMessage(content = "Hey so you mentioned you were researching good reads? ", name = "bot")]
# messages.append(HumanMessage(content = "Yh i just read the Quran and really enjoyed it, what others should i read?", name = "Jammy"))

# for m in messages:
#     m.pretty_print()

# print ("xxxx")

# llm = ChatOpenAI(model="gpt-4o")
# response = llm.invoke(messages)

# messages.append(AIMessage(content = response.content, name = "bot"))

# for m in messages:
#     m.pretty_print()
    
    
    
    
    
    
    
    
    
    
    
    
from langgraph.graph import MessagesState
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama.llms import OllamaLLM

load_dotenv()

llm = OllamaLLM(model="deepseek-r1:1.5b")

def chatbot(state: MessagesState):
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content = response))
    return {"messages": state["messages"]}

builder = StateGraph(MessagesState)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

memory = MemorySaver()

graph = builder.compile(checkpointer = memory)

# messages = [HumanMessage(content="hi")]

messages = [SystemMessage(content = "You are a helpful assistant!")]
human_messages = HumanMessage(content = "what is the capital of Pakistan!")
messages.append(human_messages)

config = {"configurable": {"thread_id": "1"}}

messages = graph.invoke({"messages": messages},config)

# for m in messages['messages']:
#     print(m.content)
#     # m.pretty_print()
#     # pass
    
print(messages['messages'][-1].content)



    
    
    
# messages = [SystemMessage(content = "You are a helpful assistant!")]

# human_messages = HumanMessage(content = "hi!")

# messages.append(human_messages)

# initial_state["messages"].append(messages)
# initial_state = {"messages": sys_msg}
    
    

