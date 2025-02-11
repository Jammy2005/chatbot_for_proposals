from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState
from chatbot_utils import create_graph
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver

def database_agent(question: str) -> str:
    """Can communicate with the KPS internal website to query company specific information.

    Args:
        question: the query/question. Just plain text of what information needs to be extracted from the database.
    """
    my_graph = create_graph()
    response = my_graph.invoke(question)
    return response

tools = [database_agent]
llm = ChatOpenAI(model = "gpt-4o")
llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(content = "You work at KPS(KAKA processing systems). You are a helpful assistant tasked with helping employees with whatever they need. You can use the tools as your disposable to gain insight and answer the with KPS specific knowledge.")

def assistant(state: MessagesState):
    return {"messages" : llm_with_tools.invoke([sys_msg] + state["messages"])}

builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph = builder.compile()

messages = [HumanMessage(content="I am working on a project that requires making an RGB game. It is a three week long project. the game will have ai characters too, that have reasoning capabilities. can u pls give me a time line and plan aswell as suggest who i should allocate to this project?")]

messages = graph.invoke({"messages": messages})

for m in messages['messages']:
    m.pretty_print()
    # pass
    
# memory = MemorySaver()
# memory_graph = builder.compile(checkpointer = memory)

# config = {"configurable": {"thread_id": "1"}}

# messages = [HumanMessage(content = "My names James")]

# messages = memory_graph.invoke({"messages": messages},config)
# for m in messages['messages']:
#     # m.pretty_print()
#     pass
    
# messages = [HumanMessage(content="Whats my name?")]
# messages = memory_graph.invoke({"messages": messages}, config)
# for m in messages['messages']:
#     # m.pretty_print()
#     pass