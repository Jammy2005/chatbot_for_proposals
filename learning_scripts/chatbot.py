from langgraph.graph import MessagesState
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatOpenAI(model = "gpt-4o")

def chatbot(state: MessagesState):
    # print(state)
    response = llm.invoke(state["messages"])
    # print (response)
    state["messages"].append(response)
    # print(state)
    # state["messages"] = state["messages"] + AIMessage(content = response)
    return {"messages": state["messages"]}
    

builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

memory = MemorySaver()

graph = builder.compile(checkpointer = memory)

config = {"configurable": {"thread_id": "1"}}

messages = [HumanMessage(content = "My names James")]

messages = graph.invoke({"messages": messages}, config)

# print(messages)
for m in messages['messages']:
    # print(m.content)
    pass
    
messages = [HumanMessage(content = "what is the local language of Pakistan?")]
# print(messages)
# messages = graph.invoke({"messages": messages}, config)

sys_msg = [SystemMessage(content = "You are a helpful assistant!")]
state = {"messages": sys_msg}

messages = HumanMessage(content = "What is the capital of Australia?")
state["messages"].append(messages)
# print (state)
for event in graph.stream(state):
    print(event.values)
                
# print(messages)
# for m in messages['messages']:
#     print(m.content)
#     pass

# if __name__ == "__main__":
#     while True:
#         prompt = input("User: ")
#         if prompt in ["quit", "exit", "q"]:
#             print("Good Bye!")
#             break
#         else:
#             messages = [HumanMessage(content = prompt)]
#             messages = graph.invoke({"messages": messages}, config)
#             message_list = messages["messages"]
#             ai_respone = message_list[-1].content
#             print("AI: ", ai_respone)
            

