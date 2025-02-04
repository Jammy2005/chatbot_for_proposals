from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class TypedDictState(TypedDict):
    foo: str
    bar: str
    
class TypedDictState(TypedDict):
    name: str
    mood: Literal["happy", "sad"]
    
def node_1(state):
    print("---Node 1---")
    return {"name": state['name'] + " is ... "}

def node_2(state):
    print("---Node 2---")
    return {"mood": "happy"}

def node_3(state):
    print("---Node 3---")
    return {"mood": "sad"}

def decide_mood(state) -> Literal["node_2", "node_3"]:
        
    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:

        # 50% of the time, we return Node 2
        return "node_2"
    
    # 50% of the time, we return Node 3
    return "node_3"
    
    
builder = StateGraph(TypedDictState)

builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph = builder.compile()

messages = [AIMessage(content = "Hey so you mentioned you were researching good reads? ", name = "bot")]
messages.append(HumanMessage(content = "Yh i just read the Quran and really enjoyed it, what others should i read?", name = "Jammy"))

for m in messages:
    m.pretty_print()

print ("xxxx")

llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke(messages)

messages.append(AIMessage(content = response.content, name = "bot"))

for m in messages:
    m.pretty_print()