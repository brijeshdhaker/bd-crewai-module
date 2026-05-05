import os
from crewai import Agent, Crew, Process, Task
from crewai.tools import tool
from crewai_tools import MySQLSearchTool
from com.example.ai.config import create_rag_config




_rag_tool_config = create_rag_config()

# Initialize the tool with the database URI and the target table name
mysqluser = os.environ["MYSQL_ADMIN_USER"]
mysqlpass = os.environ["MYSQL_ADMIN_PASSWORD"]
mysql_uri = f"mysql://{mysqluser}:{mysqlpass}@mysqlserver.sandbox.net:3306/SANDBOXDB"
tool = MySQLSearchTool(
    db_uri=mysql_uri,
    table_name='CUSTOMERS',
    config=_rag_tool_config
)

print(tool.run("Show Ramesh Age and Address"))

# from crewai_tools import NL2SQLTool
# nl2sql = NL2SQLTool(
#     db_uri=f'mysql+pymysql://{mysqluser}:{mysqlpass}@mysqlserver.sandbox.net:3306/SANDBOXDB',
#     allow_dml=True,
#     #tables=['CUSTOMERS']
# )

# print(nl2sql.run("list CUSTOMERS who live in city Hyderabad"))

#nl2sql.run("Retrieve the average, maximum, and minimum monthly revenue for each city,"
#           "but only include cities that have more than one user. Also, count the number"
#           "of user in each city and sort the results by the average monthly revenue in descending order")

import os
from crewai.tools import tool
from crewai_tools import MySQLSearchTool
from langchain_community.utilities import SQLDatabase
from langchain_community.tools import  ListSQLDatabaseTool

mysqluser = os.environ["MYSQL_ADMIN_USER"]
mysqlpass = os.environ["MYSQL_ADMIN_PASSWORD"]

# Replace with your credentials
mysql_uri = f"mysql+mysqlconnector://{mysqluser}:{mysqlpass}@mysqlserver.sandbox.net:3306/SANDBOXDB"
db = SQLDatabase.from_uri(mysql_uri)

@tool("list_tables")
def list_tables() -> str:
    """List the available tables in the database"""
    return ListSQLDatabaseTool(db=db).invoke("")

list_tables.run()

from langchain_community.tools import InfoSQLDatabaseTool

@tool("tables_schema")
def tables_schema(tables: str) -> str:
    """
    Input is a comma-separated list of tables, output is the schema and sample rows
    for those tables. Be sure that the tables actually exist by calling `list_tables` first!
    Example Input: table1, table2, table3
    """
    tool = InfoSQLDatabaseTool(db=db)
    return tool.invoke(tables)

print(tables_schema.run("CUSTOMERS"))

from langchain_community.tools import QuerySQLDatabaseTool


@tool("execute_sql")
def execute_sql(sql_query: str) -> str:
    """Execute a SQL query against the database. Returns the result"""
    return QuerySQLDatabaseTool(db=db).invoke(sql_query)

execute_sql.run("SELECT * FROM CUSTOMERS WHERE ID > 1 LIMIT 5")


from langchain_community.tools import QuerySQLCheckerTool
from langchain.chat_models import init_chat_model

llm=init_chat_model(
    model="groq:openai/gpt-oss-20b",
    temperature=0.7,
)

@tool("check_sql")
def check_sql(sql_query: str) -> str:
    """
    Use this tool to double check if your query is correct before executing it. Always use this
    tool before executing a query with `execute_sql`.
    """
    return QuerySQLCheckerTool(
        db=db, 
        llm=llm
    ).invoke({"query": sql_query})

check_sql.run("SELECT * WHERE ID > 1 LIMIT 5 table = CUSTOMERS")

# mysql_search_tool = MySQLSearchTool(
#     db_uri=mysql_uri,
#     table_name='CUSTOMERS',
#     config=dict(
#         llm=dict(
#             provider="ollama", # or google, openai, anthropic, llama2, ...
#             config=dict(
#                 model="llama3.2:3b-instruct-q8_0",
#                 base_url="http://localhost:11434",
#                 # temperature=0.5,
#                 # top_p=1,
#                 # stream=true,
#             ),
#         ),
#         embedder={
#             "provider": "sentence-transformer",
#             "config": {
#                 "model_name": "all-mpnet-base-v2",
#                 "device":"cpu",
#                 "normalize_embeddings": False
#             }
#         }
#     )
# )

#print(mysql_search_tool.run(query="show all CUSTOMERS"))