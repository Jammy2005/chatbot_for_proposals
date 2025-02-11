import ast
import re
from langchain_community.utilities import SQLDatabase
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.agents.agent_toolkits import create_retriever_tool



db = SQLDatabase.from_uri("mysql://root:Farheen2005@localhost:3306/kps_knowledge_base")
embeddings = OllamaEmbeddings(model="llama3")
vector_store = InMemoryVectorStore(embeddings)

# Define the query_as_list function
def query_as_list(db, query):
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", str(el)).strip() for el in res]
    return list(set(res))

# Sample SQL queries for the different columns

# Extract project names and descriptions
project_names = query_as_list(db, "SELECT Project_Name FROM projects")
project_descriptions = query_as_list(db, "SELECT Description FROM projects")

# Extract resource names, roles, and core technical expertise
resource_names = query_as_list(db, "SELECT Name FROM resources")
resource_roles = query_as_list(db, "SELECT Role FROM resources")
resource_expertise = query_as_list(db, "SELECT Core_Technical_Expertise FROM resources")

# Extract deliverable descriptions
deliverable_descriptions = query_as_list(db, "SELECT Deliverable_Description FROM project_deliverables")

# Extract project types
project_types = query_as_list(db, "SELECT Project_Type FROM project_types")

# Combine all the extracted data for embedding
combined_data = (
    project_names +
    project_descriptions +
    resource_names +
    resource_roles +
    resource_expertise +
    deliverable_descriptions +
    project_types
)

# Display a sample of the combined data
# print("Sample data to embed in the vector store:")
# print(combined_data)  # Display the first 10 entries

_ = vector_store.add_texts(combined_data)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
description = (
    "Use to look up values to filter on. Input is an approximate spelling "
    "of the proper noun, output is valid proper nouns. Use the noun most "
    "similar to the search."
)
retriever_tool = create_retriever_tool(
    retriever,
    name="search_proper_nouns",
    description=description,
)

print("CREATED VECTOR STORE, sorry for the wait.")


