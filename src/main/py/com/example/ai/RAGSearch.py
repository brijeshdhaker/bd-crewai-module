import os
from dotenv import load_dotenv
from com.example.ai.vectors.FaissVectorStore import FaissVectorStore
from langchain_groq import ChatGroq

load_dotenv()
# model : gemma2-9b-it decommisioned.

class RAGSearch:
    def __init__(self, 
                 persist_dir: str = "faiss", 
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2", 
                 llm_model: str = "openai/gpt-oss-20b"):
        #
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        # Load or build vectorstore
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from com.example.ai.loader.LoadManager import LoadManager
            docs = LoadManager.from_directory("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        
        #    
        groq_api_key = os.environ["OPENAI_API_KEY"]
        self.llm = ChatGroq(groq_api_key=groq_api_key, model_name=llm_model)
        print(f"[INFO] Groq LLM initialized: {llm_model}")

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found."
        prompt = f"""Summarize the following context for the query: '{query}'\n\nContext:\n{context}\n\nSummary:"""
        response = self.llm.invoke([prompt])
        return response.content

# Example usage
if __name__ == "__main__":
    rag_search = RAGSearch()
    query = "list customer_ids"
    summary = rag_search.search_and_summarize(query, top_k=3)
    print("Summary:", summary)