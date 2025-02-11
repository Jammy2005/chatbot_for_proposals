from langchain_community.utilities import SQLDatabase
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain import hub
from typing_extensions import Annotated
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langgraph.graph import START, StateGraph
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
import ast
import re
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

from create_vector_store import retriever_tool


load_dotenv()

db = SQLDatabase.from_uri("mysql://root:Farheen2005@localhost:3306/kps_knowledge_base")

llm = ChatOpenAI(model = "gpt-4o")
# llm = OllamaLLM(model = "deepseek-r1:1.5b")

embeddings = OllamaEmbeddings(model="llama3")

vector_store = InMemoryVectorStore(embeddings)

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

class QueryOutput(TypedDict):
    """Generate sql query"""
    query: Annotated[str, ..., "Syntactically valid SQL query."] # this means: must be string, no default, desctription
    
def write_query(state: State):
    """Generate SQL query to fetch information."""
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )  
    structured_llm = llm.with_structured_output(QueryOutput) # enforce llm to structure output as defined above
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}
    
query = write_query({"question": "How many Employees are there?"})
# print(query)

def execute_query(state: State):
    """Execute SQL query"""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}
# print (execute_query(query))


def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}

graph_builder = StateGraph(State).add_sequence(
    [write_query, execute_query, generate_answer]
)
graph_builder.add_edge(START, "write_query")
graph = graph_builder.compile()
    
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()
   
system_message = prompt_template.format(dialect="MySQL", top_k=5)

suffix = (
    "If you need to filter on a proper noun like a Name, you must ALWAYS first look up "
    "the filter value using the 'search_proper_nouns' tool! Do not try to "
    "guess at the proper name - use this function to find similar ones."
)

system = f"{system_message}\n\n{suffix}"

tools.append(retriever_tool)

agent_executor = create_react_agent(llm, tools, prompt=system_message)

# question = "i am looking to allocate two of my employees to a new project where we need to design a NN that can recognize captchas. can u pls reccomend which empoyees i shoud use. "
# question = " what is the relationship bw api's and enterprise service bus? can u reccomend an employee in the db who could work on a project that involves enterprise service bus."
question = " Retrieve the list of people who worked on the AI chatbot project. "

for step in agent_executor.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()







