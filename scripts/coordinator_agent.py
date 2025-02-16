from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import MessagesState
from database_agent import create_db_graph
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent

load_dotenv()

@tool
def database_agent(question: str) -> str:
    """Executes a database query based on natural language input.

    This function translates user queries into SQL, retrieves relevant 
    company-specific information, and returns it as natural language.

    Parameters:
    ----------
    question : str
        A natural language question related to company-specific information 
        (e.g., "Who worked on the AI chatbot project?").

    Returns:
    -------
    response: str
        A natural langauge response of the relevent content qeured from the database
        (e.g., "Ayesha Khan worked on the AI chatbot project.")
        

    Example Usage:
    --------------
    >>> database_agent("List all active projects in 2024")
    {
        "No projects are active in 2024."
    }

    Notes:
    ------
    - The function should **only** execute valid, relevant queries.
    - If no relevant data is found, it should return a helpful message.
    - If the query is malformed or unauthorized, it should return an error.
    """
    db_agent_graph = create_db_graph()
    
    config = {"configurable": {"thread_id": "2"}}
    
    ans = db_agent_graph.invoke({"messages": [{"role": "user", "content": question}]}, config = config)

    response = (ans["messages"][-1].content)
    
    return response
    
tools = [database_agent]
llm = ChatOpenAI(model = "gpt-4o")
llm_with_tools = llm.bind_tools(tools)

def assistant(state: MessagesState):
    return {"messages" : llm_with_tools.invoke([sys_msg] + state["messages"])}

builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph = builder.compile()

sys_msg = SystemMessage(content=r"""
You are KPS Assistant, a virtual employee support agent at KPS (KAKA Processing Systems). 

Your primary role is to assist employees with their queries using your general knowledge and company-specific data.

### General Queries:
- Answer based on your knowledge and reasoning.

### Company-Specific Queries:
- If the required information is specific to KPS and not available in your knowledge base, use the Database Agent to retrieve it.

### Database Agent Role:
- The Database Agent can translate natural language queries into SQL, execute them, and return relevant company data.

### Collaboration:
- Determine when a query requires company data and coordinate with the Database Agent to fetch relevant results.

### Response Format:
- Provide clear, concise, and professional answers while ensuring accuracy.

### Fallback Handling:
- If the information is not in the database or outside your expertise, inform the user politely and suggest alternative steps.

### Security Considerations:
- Only retrieve non-sensitive company data.
- Ensure database queries are relevant and efficient.

**Your mission:** 
Act as a knowledgeable, helpful, and proactive assistant to KPS employees, ensuring smooth and efficient interactions.
""")

messages = [HumanMessage(content="what is the name of the company? ")]

messages = graph.invoke({"messages": messages})

for m in messages['messages']:
    m.pretty_print()
    # pass
