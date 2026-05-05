
from crewai.tools  import tool

@tool
def router_tool(question):
  """Router Function"""
  if 'ESOP' in question:
    return 'vectorstore'
  else:
    return 'web_search'