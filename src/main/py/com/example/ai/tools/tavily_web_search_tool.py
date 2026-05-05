import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch

os.environ['TAVILY_API_KEY']
web_search_tool = TavilySearch(k=3)

#results = web_search_tool.run("How does exercise price determine for ESOP?")
#print(results)