from crewai_tools import PDFSearchTool
from com.example.ai.config import create_rag_config, _llm_openai,_llm_ollama, _embedder_config_st

#
pdf_search_tool = PDFSearchTool(
    config=create_rag_config(),
    collection_name="pdf-documents"
)
#pdf_search_tool.add(pdf='documents/pdfs/esop_info.pdf')

#print(pdf_rag_search.run("How does exercise price determine for ESOP?"))