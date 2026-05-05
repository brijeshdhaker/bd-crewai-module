#
# python src/main/py/com/example/agentic/mcp/mathserver.py
#
from mcp.server.fastmcp import FastMCP

#mcp server name
mcp = FastMCP("SANDBOX MCP Server",port=8000)

@mcp.tool()
def greet(name: str) -> str:
    """_summary_
    perform greeting action
    """
    return f"Hello, {name} !!! How Are You ..?"

@mcp.tool()
def add(a: int, b:int) -> int:
    """_summary_
    perform add for two numbers
    """
    return a+b

@mcp.tool()
def multiply(a: int, b:int) -> int:
    """_summary_
    perform multiplication for two numbers
    """
    return a*b

if __name__ == "__main__":
    #mcp.run(transport="http", port=8000)
    mcp.run(transport="stdio")