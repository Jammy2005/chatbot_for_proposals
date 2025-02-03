from pprint import pprint
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langchain_ollama.llms import OllamaLLM
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END, MessagesState



messages = [AIMessage(content= f'So your researching oceam mammals?', name = 'Frank')]

messages.append(HumanMessage(content=f"Yes, that's right.",name="Jammy"))

messages.append(AIMessage(content=f"Great, what would you like to learn about.", name="Frank"))

messages.append(HumanMessage(content=f"I want to learn about the best place to see Orcas in the US.", name="Jammy"))

for m in messages:
    pass
    # m.pretty_print()
    
load_dotenv()
    
# model = OllamaLLM(model = "deepseek-r1:7b")
model = ChatOpenAI(model="gpt-4o", temperature=0) 

result = model.invoke(messages)

# print(result.content)

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

model_with_tools = model.bind_tools([multiply])

tool_call = model_with_tools.invoke([HumanMessage(content = 'what is 2*3', name = 'Jammy')])

# print (tool_call)

# using typedict
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    
# using MessageState
class MessageState(MessagesState):
    pass

def tool_calling_model(state: MessagesState):
    return {"messages": [model_with_tools.invoke(state["messages"])]}

# building graph
builder = StateGraph(MessageState)
builder.add_node("tool_calling_model", tool_calling_model)
builder.add_edge(START, "tool_calling_model")
builder.add_edge("tool_calling_model", END)

graph = builder.compile()

messages = graph.invoke({"messages": HumanMessage(content='Hello')})

for m in messages['messages']:
    m.pretty_print()









    



