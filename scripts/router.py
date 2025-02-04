from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage

load_dotenv()

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

llm = ChatOpenAI(model = 'gpt-4o')
llm_with_tools = llm.bind_tools([multiply])

# node
def tool_calling_llm(state: MessagesState):
    return{"messages": [llm_with_tools.invoke(state["messages"])]}

# Build Graph
builder = StateGraph(MessagesState)

builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))

builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tool_calling_llm", END)

graph = builder.compile()

messages = [HumanMessage(content = "Hello!"), HumanMessage(content = "panch guna do ke ha?")]

messages = graph.invoke({"messages": messages})

for m in messages['messages']: 
    m.pretty_print()




    


