import os
import warnings
import pymysql.cursors
from com.example.ai.apps.mysql_chat.crew import ChatWithMysql
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

#
# fastapi dev src/main/py/com/example/ai/apps/mysql_chat/main.py
#
schema_info = None
mysql_connection = None

class DatabaseConfig(BaseModel):
    hostname: str = Field(description="", default="mysqlserver.sandbox.net")
    username: str = Field(description="", default="mysqladmin")
    password: str = Field(description="", default=f"{os.environ['MYSQL_ADMIN_PASSWORD']}")
    database: str = Field(description="", default="SANDBOXDB")

def get_schema(conn):
    """
    Get database schema information using provided connection
    """
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    schema_info = "Database Schema:\n"
    for table in tables:
        table_name = table[0]
        schema_info += f"\nTable: {table_name}\n"
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        for column in columns:
            schema_info += f"  {column[0]}: {column[1]}\n"
    
    cursor.close()
    return schema_info

app = FastAPI()

@app.post("/connect")
async def connect(config: DatabaseConfig):
    """
    API endpoint to establish MySQL connection
    """
    global mysql_connection
    global schema_info
    
    try:
        mysql_connection = pymysql.connect(
            host=config.hostname,
            user=config.username,
            password=config.password,
            database=config.database
        )
        schema_info = get_schema(mysql_connection)
        return {"message": f"Successfully connected to {config.database} database"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect: {str(e)}")

@app.get("/query")
async def query(question: str):
    """
    API endpoint to handle database queries
    """
    if not mysql_connection:
        raise HTTPException(status_code=400, detail="Database connection not established. Call /connect first")
        
    inputs = {
        'schema': schema_info,
        'question': question
    }
    return ChatWithMysql().crew().kickoff(inputs=inputs).raw


def start():
    """Launched with `poetry run start`"""
    uvicorn.run("com.example.ai.apps.mysql_chat.main:app", host="0.0.0.0", port=8000, reload=True)