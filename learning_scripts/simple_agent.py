from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b


tools = [add, divide, multiply]
llm = ChatOpenAI(model = "gpt-4o")

llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

# System Message
sys_msg = SystemMessage(content = "You are doing a Dave Chappele impersonation. You will perform arithmatics on sets of inputs.")

# Node
def assistant(state: MessagesState):
    return {"messages" : llm_with_tools.invoke([sys_msg] + state["messages"])}



builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph = builder.compile()

messages = [HumanMessage(content="2+3*5, use the tools at ur disposle")]

messages = graph.invoke({"messages": messages})

for m in messages['messages']:
    m.pretty_print()
    pass
    
memory = MemorySaver()
memory_graph = builder.compile(checkpointer = memory)

config = {"configurable": {"thread_id": "1"}}

messages = [HumanMessage(content = "My names James")]

messages = memory_graph.invoke({"messages": messages},config)
for m in messages['messages']:
    # m.pretty_print()
    pass
    
messages = [HumanMessage(content="Whats my name?")]
messages = memory_graph.invoke({"messages": messages}, config)
for m in messages['messages']:
    # m.pretty_print()
    pass