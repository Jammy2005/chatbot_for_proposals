from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model = "gpt-4o")

IDK = "system msg: You are an assistant as KPS. Your job is to help the user with whatever queries you have. At your disposal you have another agent that can retreive information from a database. You must answer the users query and if it requires the use of a db just out put the message that should be sent to the db agent i will manually give it that msg. thanks. usermsg: Who worked on the ai chatbot project? aimessage: Please provide the message to be sent to the database agent: Retrieve the list of people who worked on the AI chatbot project.,"

response = llm.invoke(IDK)

print(response.content)