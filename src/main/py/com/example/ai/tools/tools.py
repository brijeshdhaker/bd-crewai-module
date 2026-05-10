
import os
from crewai_tools import TavilyExtractorTool
from crewai_tools import PDFSearchTool
from crewai_tools import ScrapeWebsiteTool
from com.example.ai.config import create_rag_config

def tavily_extractor(_urls: list[str]) :
    """
        Initialize with custom configuration
    """
    extractor_tool = TavilyExtractorTool(
        extract_depth='advanced',  # More comprehensive extraction
        include_images=True,       # Include image results
        timeout=90,                 # Custom timeout
        api_key=os.getenv("TAVILY_API_KEY")
    )

    # extractor_tool.run(urls=['https://www.sudhirshivaramphotography.com/'])
    return extractor_tool

#
def pdf_search_tool(query : str):
        """_summary
            Searches the pdf documents and returns results.
        """
        _tool_config = create_rag_config()
        pdf_tool = PDFSearchTool(
            pdf='/home/brijeshdhaker/IdeaProjects/bd-notebooks-module/knowledge/pdf/2026-04-01_BRIJESHD_PROFILE_MP.pdf',
            config=_tool_config
        )

        return pdf_tool.run(query)
#
#results = pdf_search_tool.run("Cloudera")
#results




# Instantiate Web Search Tool
#@tool
def scrap_website_tool():
    """
    scrap the content of the specified website.
    """
    # Initialize the tool with the website URL, 
    # so the agent can only scrap the content of the specified website
    _tool_config = create_rag_config()
    _scrap_tool = ScrapeWebsiteTool(
        website_url='https://www.sudhirshivaramphotography.com/',
        config=_tool_config
    )
    # Extract the text from the site
    #text = scrap_website_tool.run()
    #print(text)

    #
    return _scrap_tool.run()

from crewai.tools import tool
from crewai_tools import WebsiteSearchTool

# Instantiate Web Search Tool
#@tool
def web_search_tool(_query: str):
    """
    Searches the web and returns results.
    """
    _tool_config = create_rag_config()
    search_tool = WebsiteSearchTool(
        website='https://devendrayadav2494.medium.com/building-a-mini-vector-database-with-faiss-step-by-step-guide-e2b3a5a41a35',
        config=_tool_config
    )
    #
    return search_tool.run(_query)
#
# web_search_tool("FAISS")


from crewai_tools import DOCXSearchTool
# Instantiate Web Search Tool

#@tool
def docx_search_tool(_query: str):
    """
    read workd document and return document content.
    """
    _tool_config = create_rag_config()
	# Initialize the tool for semantic searches within a specific GitHub repository
    _doc_path = '/home/brijeshdhaker/IdeaProjects/bd-notebooks-module/knowledge/docx/Brijesh_Dhaker_ATS_Resume.docx'
    
    # Initialize the tool to search within any DOCX file's content
    docx_tool = DOCXSearchTool(config=_tool_config)
    docx_tool.add(docx=_doc_path)
    #
    return docx_tool.run(_query)

#
# docx_search_tool(_query="Cloudera")


import os
from crewai_tools import GithubSearchTool

#@tool
def github_search_tool(_query: str):
    _github_url =  'https://github.com'
    _repo = 'brijeshdhaker/docker-hadoop-cluster'
    _git_hub_token = os.getenv("GIT_HUB_TOKEN")
    _tool_config = create_rag_config()

    # Initialize the tool with your PAT
    _github_tool = GithubSearchTool(
        config=_tool_config,
        github_repo=f'{_github_url}/{_repo}',
        gh_token=_git_hub_token,
        content_types=['code', 'issue']
    )

    #github_search_tool.add(repo=_repo, content_types=['code', 'issue']) , github_repo="brijeshdhaker/docker-hadoop-cluster", content_types=['code', 'issue']
    return _github_tool.run(search_query=_query)


#github_search_tool(_query="hadoop")


from crewai_tools import CodeDocsSearchTool

#@tool
def codedoc_search_tool(_query: str):
    """
    read api documentation and return content.
    """
    _tool_config = create_rag_config()
    # by providing its URL:
    _search_tool = CodeDocsSearchTool(
        docs_url='https://knowledge.oracle.com/javase/8/knowledge/api/java/net/URL.html',
        config=_tool_config
    )
    #
    return _search_tool.run(_query)

#codedoc_search_tool(_query="Java")

from crewai_tools import ScrapeElementFromWebsiteTool
# Initialize tool with CSS selector for images
image_tool = ScrapeElementFromWebsiteTool(
    website_url="https://example.com",
    css_element="img"
)

from crewai_tools import ScrapflyScrapeWebsiteTool
# Initialize the tool
scrape_tool = ScrapflyScrapeWebsiteTool(api_key="your_scrapfly_api_key")