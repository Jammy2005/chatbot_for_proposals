from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain import hub
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from chat.create_vector_store import retriever_tool
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()
db = SQLDatabase.from_uri("mysql+mysqlconnector://root:Farheen2005@localhost:3306/kps_knowledge_base")
# db = SQLDatabase.from_uri("mysql://root:Farheen2005@localhost:3306/kps_knowledge_base")
llm = ChatOpenAI(model = "gpt-4o")
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
tools.append(retriever_tool)

system_message = prompt_template.format(dialect="MySQL", top_k=8)
suffix = (
    "If you need to filter on a proper noun like a Name, you must ALWAYS first look up "
    "the filter value using the 'search_proper_nouns' tool! Do not try to "
    "guess at the proper name - use this function to find similar ones."
)
system = f"{system_message}\n\n{suffix}"

memory = MemorySaver()

config = {"configurable": {"thread_id": "2"}}

print("ALL THE STEPS HAVE BEEN TAKEN TO CREATE THE DB AGENT. sorry for the wait")

def create_db_graph():
    graph = create_react_agent(llm, tools, prompt=system, checkpointer = memory)
    return graph


graph = create_db_graph()

question = "current team members and their skills"

# ans = graph.invoke({"messages": [{"role": "user", "content": question}]}, config = config)

# print(ans["messages"][-1].content)

for step in graph.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
    config = config
):
    step["messages"][-1].pretty_print()