#
# python src/main/py/com/example/agentic/mcp/mysqlserver.py
#
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Optional
from email.message import EmailMessage
from com.example.utils.MysqlProcessor import MysqlProcessor
import json

# 1. Initialize FastMCP server
mcp = FastMCP("MySQl MCP Server")

# 2. Define Complex Data Type for Email
class MysqlPayload(BaseModel):
    template: Optional[str]
    params : Optional[dict[str, str]] = Field(description="key-value pairs for sql template")
    

mysqlProcessor = MysqlProcessor()

# 3. Define Tool with Complex Input
@mcp.tool()
def fetchAll(request: MysqlPayload) -> str:
    """_summary_
    Fetch results for provided complex mysql sql query template and params:
    Args:
        template: str
        params: dict
    Returns:
        results as json string
    Example:
        fetch results for provided complex sql query with parameters :
        --template select `NAME`, `AGE`, `ADDRESS`, CONVERT(SALARY, FLOAT) AS `SALARY` from CUSTOMERS WHERE ID = {id}
        --params {"id":"1"}
    """
    _sql = None
    if request.template and request.params:
        #_sql = request.template.format(**request.params)
        _sql = request.template.format_map(request.params)
    else:
        _sql = "select `NAME`, `AGE`, `ADDRESS`, CONVERT(SALARY, FLOAT) AS `SALARY` from CUSTOMERS WHERE ID = {id}"
        
    records = mysqlProcessor.fetchAll(sql=_sql, isdict= True)
    json_string = json.dumps(records)
    return json_string

@mcp.tool()
def execute(request: MysqlPayload) -> dict:
    """_summary_
    Execute a complex mysql sql query with template and params:
    Args:
        template: str
        params: dict
    Returns: 
        count of updated records
    Example:
        execute below give complex sql query with provide parameters :
        --template UPDATE CUSTOMERS SET `ADDRESS`='{address}' WHERE ID = {id}
        --params {"id":"1", "address":"A2-803 Acolade Co. HSG"}
    """
    _result = {"status":"true"}
    try:
        _sql = None
        if request.template and request.params:
            #_sql = request.template.format(**request.params)
            _sql = request.template.format_map(request.params)
        else:
            _sql = "UPDATE CUSTOMERS SET `ADDRESS`='{address}' WHERE ID = {id}"
        _cnt = mysqlProcessor.execute(sql=_sql)
        _result["count"]= str(_cnt)
    except Exception as e:
        # Print any error messages to stdout
        print(f"An error occurred: {e}")
        _result["status"]= "false"
        _result["count"]= "0"
        _result["message"]= f"{e}"
    finally:
        pass
    

    return {"status":"true", "count":f"{_cnt}"}

#
if __name__ == "__main__":
    mcp.run(transport="stdio")