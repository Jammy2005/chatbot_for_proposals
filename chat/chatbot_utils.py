# # chat/chatbot_utils.py
# import sys
# from langgraph.graph import MessagesState, StateGraph, START, END
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
# from langgraph.checkpoint.memory import MemorySaver
# from langchain_ollama.llms import OllamaLLM  # if needed

# load_dotenv()

# # Initialize the LLM (using GPT-4 in your case)
# llm = ChatOpenAI(model="gpt-4o")
# # llm = OllamaLLM(model="deepseek-r1:1.5b")
# # If needed, you could swap in OllamaLLM.

# def chatbot(state: MessagesState):
#     response = llm.invoke(state["messages"])
#     state["messages"].append(response)
#     return {"messages": state["messages"]}

# def create_graph():
#     """Construct and return the state graph for the chatbot."""
#     builder = StateGraph(MessagesState)
#     builder.add_node("chatbot", chatbot)
#     builder.add_edge(START, "chatbot")
#     builder.add_edge("chatbot", END)
#     memory = MemorySaver()
#     graph = builder.compile(checkpointer=memory)
#     return graph  

from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain import hub
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from create_vector_store import retriever_tool
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()
db = SQLDatabase.from_uri("mysql+mysqlconnector://root:Farheen2005@localhost:3306/kps_knowledge_base")
# db = SQLDatabase.from_uri("mysql://root:Farheen2005@localhost:3306/kps_knowledge_base")
llm = ChatOpenAI(model = "gpt-4o")
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
tools.append(retriever_tool)

system_message = prompt_template.format(dialect="MySQL", top_k=5)
suffix = (
    "If you need to filter on a proper noun like a Name, you must ALWAYS first look up "
    "the filter value using the 'search_proper_nouns' tool! Do not try to "
    "guess at the proper name - use this function to find similar ones."
)
system = f"{system_message}\n\n{suffix}"

memory = MemorySaver()

config = {"configurable": {"thread_id": "2"}}

def create_graph():
    graph = create_react_agent(llm, tools, prompt=system, checkpointer = memory)
    return graph

# agent_executor.compile()