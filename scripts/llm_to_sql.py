import openai
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_sql_database import SQLDatabaseChain
from mysql_connection import create_connection
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI LLM
llm = ChatOpenAI(model = "gpt-4o",temperature=0)

# Connect to MySQL and initialize the SQLDatabase
sql_database = SQLDatabase.from_uri("mysql+mysqlconnector://root:your_mysql_password@localhost/kps_knowledge_base")

# Set up LangChain's SQL chain
db_chain = SQLDatabaseChain.from_llm(llm, sql_database)

def answer_query(query):
    try:
        # Pass the user's natural language query to the LLM
        result = db_chain.run(query)
        print(f"Query Result:\n{result}")
        return result
    except Exception as e:
        print(f"Error executing query: {e}")

if __name__ == "__main__":
    user_query = "Which resources are best for an NLP project?"
    answer_query(user_query)
