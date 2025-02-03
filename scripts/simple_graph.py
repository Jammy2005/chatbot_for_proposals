from typing_extensions import TypedDict
import random
from typing import Literal
from langgraph.graph import StateGraph, START, END

# acts as input schema for all nodes and edges in our graph
class State(TypedDict):   
    graph_state: str
    
    
    
# nodes are just python functions that take in the state

def node1(state):
    print("--NODE 1--")
    return {"graph_state": state['graph_state'] + " i am" }

def node2(state):
    print("--NODE 2--")
    return {"graph_state": state['graph_state'] + " happy" }

def node3(state):
    print("--NODE 3--")
    return {"graph_state": state['graph_state'] + " sad" }


# edges connect nodes: normally or conditionally

def decide_mood(state) -> Literal["node2", "node3"]:
    
    # 50 split between nodes 2, 3
    if random.random() < 0.5:

        # 50% of the time, we return Node 2
        return "node2"
    
    # 50% of the time, we return Node 3
    return "node3"


# graph construction: buiding it from the individual components

builder = StateGraph(State)

builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.add_node("node3", node3)

builder.add_edge(START, 'node1')
builder.add_conditional_edges('node1', decide_mood)
builder.add_edge('node2', END)
builder.add_edge('node3', END)

graph = builder.compile()

result = graph.invoke({"graph_state": "Hi, this is Macbeth."})

print (result)

