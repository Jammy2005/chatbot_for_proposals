from langchain_community.utilities import SQLDatabase
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain import hub
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from create_vector_store import retriever_tool
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, AIMessage


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

agent_executor = create_react_agent(llm, tools, prompt=system, checkpointer = memory)

# agent_executor.compile()

# question = " Which projects are curently being supported? "

# for step in agent_executor.stream(
#     {"messages": [{"role": "user", "content": question}]},
#     stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()

if __name__ == "__main__":
    
    sys_msg = [SystemMessage(content = "You are a helpful assistant working at KDS. Throught the tools made available to you, you have access to the KPS internal database. Please use this database and your intuition to answer the users queries to the best of your abilities.")]
    state = {"messages": sys_msg}
    # running the chatbot in a loop
    while True:
        prompt = input("\nUser: ")
        if prompt.lower() in ["quit", "exit", "q"]:
            print("Good Bye!")
            break
        else:
            messages = HumanMessage(content = prompt)
            state["messages"].append(messages)
                
            # messages = graph.invoke({"messages": messages},config)
            # print("Assistant: ", messages['messages'][-1].content)
            
            for data, stream_mode in agent_executor.stream(state, config=config, stream_mode="messages"):
                # print(data)
                if data.type == "AIMessageChunk":
                    print (data.content, end="")
            

