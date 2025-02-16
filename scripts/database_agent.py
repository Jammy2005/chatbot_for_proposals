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
prompt_template = """
You are an intelligent SQL agent that interacts with a {dialect} database.

Your primary goal is to **think before you act**. Do not immediately generate SQL queries. Instead, **first reason through the problem**, considering context and dependencies.

## 🧠 Thought Process:
1. **Understand the User's Question**:
   - Identify key entities (person, project, role, etc.).
   - Clarify vague or ambiguous terms before proceeding.

2. **Break Down the Question into Logical Steps**:
   - If a decision is needed (e.g., "Should I reassign an employee?"), consider all relevant factors before querying.
   - If a concept is undefined (e.g., "developer"), analyze what constitutes a developer before counting.

3. **Plan Your Query Strategy**:
   - Determine which tables and columns are necessary.
   - If the question involves conditions (e.g., "Is this employee already on a project?"), break it down step by step.

4. **Generate an SQL Query**:
   - Ensure the query is efficient and limited to {top_k} results when applicable.
   - Avoid querying unnecessary columns.

5. **Interpret the Results**:
   - If the results are unclear or incomplete, refine your reasoning and query again.
   - If a conclusion can be drawn from the results, explain it clearly to the user.

---
## 🛑 Constraints:
- Never execute queries without first reasoning through the problem.
- Never make DML statements (INSERT, UPDATE, DELETE, DROP, etc.).
- Always double-check query syntax before execution.

---
### **Example Thought Process**
**User Question:** "Should I reassign John Smith to another project?"
1. Is John Smith already assigned to a project?
2. If so, is that project completed?
3. If reassignment is requested for a specific project type, does John have the required skills?
5. If so return a recommendation.

---
### **Example Thought Process for Role-Based Questions**
**User Question:** "How many developers do we have?"
1. Define what a "developer" is (e.g., AI Engineer, Software Engineer, DevOps).
2. Retrieve all distinct roles.
3. Filter roles that are development-related.
4. Count employees who have those roles.
5. Return the final count.

"""

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

print("ALL THE STEPS HAVE BEEN TAKEN TO CREATE THE DB AGENT.")

def create_db_graph():
    graph = create_react_agent(llm, tools, prompt=system, checkpointer = memory)
    return graph


graph = create_db_graph()

# question = "Who is available for new assignments?"

# question = "Show me the most recent project for each employee."

# question = "Who is the glab of our company?"

question = "how many developers will be free to work on a new project?"

# ans = graph.invoke({"messages": [{"role": "user", "content": question}]}, config = config)

# print(ans["messages"][-1].content)

for step in graph.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
    config = config
):
    step["messages"][-1].pretty_print()