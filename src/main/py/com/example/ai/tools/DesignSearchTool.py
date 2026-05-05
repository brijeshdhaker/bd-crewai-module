import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import chromadb
from chromadb.config import Settings
from com.example.ai.vectors.ChromaVectorStore import ChromaVectorStore

class DesignInput(BaseModel):
    """Input schema for DesignlocateTool."""
    topic: str = Field(..., description="The topic to scan in custom knowledge store.")


class DesignSearchTool(BaseTool):
    name: str = "Designlocate"
    description: str = "Scan relavent documents in custom knowledge store."
    args_schema: type[BaseModel] = DesignInput

    def _run(self, topic: str) -> str:
        try:
            # Process results
            store = ChromaVectorStore()
            retrieved_documents = store.query(topic, top_k=10)
            return retrieved_documents
        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []


    #    
    def validate_content(self, articles: list) -> str:
        """Format articles into readable text."""
        formatted = "Design Articles:\n\n"
        for article in articles:
            formatted += f"""
                Title: {article['title']}
                Published: {article['published_at']}
                Summary: {article['summary']}
                Design Reference: {article['news_site']}
                URL: {article['url']}
                -------------------"""
        return formatted

        
# Example usage
if __name__ == "__main__":
    
    tool = DesignSearchTool()     
    results = tool.run("What are benefits of microservices ?")
    print("[INFO] Total Documents:", results if len(results) > 0 else None)