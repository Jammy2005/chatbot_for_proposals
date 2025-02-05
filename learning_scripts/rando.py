from langgraph.graph import MessagesState, StateGraph, START, END
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o")

# Define the chatbot function
def chatbot(state: MessagesState):
    response = llm.invoke(state["messages"])
    state["messages"].append(response)
    return {"messages": state["messages"]}

# Build the graph
builder = StateGraph(MessagesState)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# Compile with MemorySaver checkpointer
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Initialize state with a system message and user input
initial_state = {
    "messages": [
        SystemMessage(content="You are a helpful assistant!"),
        HumanMessage(content="What is the capital of Australia?")
    ]
}

# Required configuration for checkpointer
config = {"configurable": {"thread_id": "1"}}

# Stream messages and unpack the event tuples
for stream_mode, data in graph.stream(initial_state, config=config, stream_mode="messages"):
    if stream_mode == "messages":
        # Access and print the latest message content
        ai_message = data[-1]  # Last message chunk
        print(ai_message.content)
