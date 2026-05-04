import os
from langchain_community.tools.tavily_search import TavilySearchResults
os.environ['TAVILY_API_KEY'] = userdata.get('TAVILY_API_KEY')

web_search_tool = TavilySearchResults(k=3)

# web_search_tool.run("How does exercise price determine for ESOP?")