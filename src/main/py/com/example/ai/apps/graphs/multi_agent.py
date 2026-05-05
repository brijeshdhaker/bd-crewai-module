#
# https://medium.com/@Shamimw/multi-agent-orchestration-with-langgraph-retrieving-rag-data-querying-mysql-summarizing-files-ebd99edc2ba9
#

from typing import Literal, Annotated, Sequence, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.types import Command
from langgraph.graph.message import add_messages
import os, json, uuid, mysql.connector
from langchain.tools import Tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_classic.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.utilities import GoogleSerperAPIWrapper

#
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = input("Enter your OpenAI API key : ")


# **Initialize Vector Store & LLM**
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#
vectorstore = Chroma(persist_directory="/apps/sandbox/chroma_db", embedding_function=embeddings)

#
llm = init_chat_model(model="groq:openai/gpt-oss-20b")

#
system_prompt = (
    "You manage three workers: web_researcher, rag, and mysql."
    " Decide the next step and respond with a JSON object: {\"next\": \"worker_name\"}."
    " If no more tasks are needed, return: {\"next\": \"FINISH\"}."
)

class Router(TypedDict):
    next: Literal["web_researcher", "rag", "mysql", "FINISH"]

#
# **Supervisor Node**
#
def supervisor_node(state: MessagesState) -> Command:
    user_input = state["messages"][-1].content.lower()
    
    if user_input.startswith("select ") and "from orders" in user_input:
        return Command(goto="mysql")

    response_text = llm.invoke([{"role": "system", "content": system_prompt}] + state["messages"]).content
    goto = json.loads(response_text).get("next", "web_researcher") if response_text else "web_researcher"
    
    return Command(goto=END if goto == "FINISH" else goto)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# **Create Agent**
def create_agent(llm, tools):
    def chatbot(state: AgentState):
        user_message = state["messages"][-1].content
        for tool in tools:
            if hasattr(tool, "name") and tool.name.lower() in user_message.lower():
                return {"messages": [HumanMessage(content=str(tool.func(user_message)), name="tool_response")]}
        return {"messages": [AIMessage(content=str(llm.invoke(state["messages"]).content))]}
    
    agent_graph = StateGraph(AgentState)
    agent_graph.add_node("agent", chatbot)
    agent_graph.set_entry_point("agent")
    return agent_graph.compile()

# **Web Search**
def google_search(query: str) -> str:
    results = GoogleSerperAPIWrapper().results(query)
    return json.dumps(results, indent=2) if results else "No search results found."

websearch_agent = create_agent(llm, [Tool(name="Web Search", func=google_search)])

def web_research_node(state: MessagesState) -> Command:
    return Command(update={"messages": [HumanMessage(content=websearch_agent.invoke(state)["messages"][-1].content, name="web_researcher")]}, goto="supervisor")

# **RAG Retrieval**
def retrieve_vector_data(prompt: str) -> str:
    retriever = vectorstore.as_retriever(search_type="similarity")
    response = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever).invoke({"query": prompt})
    return response.get("result", "No response generated.")

rag_agent = create_agent(llm, [Tool(name="RAG Retriever", func=retrieve_vector_data)])

def rag_node(state: MessagesState) -> Command:
    return Command(update={"messages": [HumanMessage(content=rag_agent.invoke(state)["messages"][-1].content, name="rag")]}, goto="supervisor")

# **MySQL Query**
def mysql_query(query: str) -> str:
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="pwd", database="db1")
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return json.dumps(results, indent=2) if results else "No data found in orders table."
    except mysql.connector.Error as err:
        return f"Database error: {err}"

mysql_query_agent = create_agent(llm, [Tool(name="MySQL Query", func=mysql_query)])

def mysql_query_agent_node(state: MessagesState) -> Command:
    return Command(update={"messages": [HumanMessage(content=mysql_query(state["messages"][-1].content.strip()), name="mysql")]}, goto="supervisor")

# **Build Execution Graph**
builder = StateGraph(MessagesState)
builder.add_edge(START, "supervisor")
builder.add_node("supervisor", supervisor_node)
builder.add_node("web_researcher", web_research_node)
builder.add_node("rag", rag_node)
builder.add_node("mysql", mysql_query_agent_node)
graph = builder.compile()

# **Run the System**
config = {"configurable": {"thread_id": str(uuid.uuid4())}}

user = input("User: ")
if user.lower() in {"q", "quit"}:
    print("Goodbye!")
    exit()

output = graph.invoke({"messages": [HumanMessage(content=user)]}, config=config)
print("AI:", output["messages"][-1].content)