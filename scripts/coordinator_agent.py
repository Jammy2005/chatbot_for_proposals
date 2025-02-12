from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import MessagesState
from chat.chatbot_utils import create_graph
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver

# class State(MessagesState):
#     db_results: list[str]
    
# def database_agent(args: dict) -> dict:
#     # Extract the question from args
#     question = args.get("question", "")

#     # Now do your normal process:
#     print("Processing question:", question)

#     my_graph = create_graph()  # your retrieval or DB logic

#     # Store the streamed messages in a list
#     result_messages = []
#     for step in my_graph.stream(
#         {"messages": [{"role": "user", "content": question}]},
#         stream_mode="values",
#     ):
#         step["messages"][-1].pretty_print()
#         result_messages.append(step["messages"][-1])

#     # Return a valid dictionary
#     if not result_messages:
#         return {"messages": [AIMessage(content="No response from DB tool.")]}

#     return {"messages": result_messages}
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b



tools = [multiply]#[database_agent]
llm = ChatOpenAI(model = "gpt-4o")
llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(content = "5 into 9")

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