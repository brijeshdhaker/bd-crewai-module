import os
from dotenv import load_dotenv
from com.example.ai.loader.LoadManager import LoadManager
from com.example.ai.vectors.VectorStoreManager import VectorStoreManager
from com.example.ai.LLMManager import LLMManager
from langchain_community.document_loaders import PDFPlumberLoader

#
class RAGSearch:
    
    #
    def __init__(self, collectionOrIndexName: str = "faiss_index"):
        #
        self.store_mgr = VectorStoreManager(store_type="faissdb", collectionOrIndexName="faiss_index")
        #    
        self.llm = LLMManager.get_model()
        #
        print(f"[INFO] LLM Initialized: {self.llm}")

    #
    def load_documents(self) :
        #
        loader = PDFPlumberLoader(file_path="documents/pdfs/esop_info.pdf")
        documents = loader.load()
        self.store_mgr.add_documents(documents=documents)


    def search_and_summarize(self, topic: str, top_k: int = 5) -> str:
        retriever = self.store_mgr.retriever(
            search_type="similarity", 
            search_kwargs={
                "filter": {"source": "documents/pdfs/esop_info.pdf"}, 
                "score_threshold": 0.8,
                "k": top_k, 
                "fetch_k": 50
            }
        )
        documents = retriever.invoke(input=topic)
        #documents = self.vectorstore.similarity_search(query=topic, k=top_k)
        texts = [d.page_content for d in documents if d.page_content]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found."
        prompt = f"""Summarize the following context for the query: '{topic}'\n\nContext:\n{context}\n\nSummary:"""
        response = self.llm.invoke([prompt])
        return response.content


def main():
    load_dotenv()
    rag_search = RAGSearch()
    query = "How does exercise price determine for ESOP ?"
    summary = rag_search.search_and_summarize(query, top_k=5)
    print("Summary:", summary)

# Example usage
if __name__ == "__main__":
    main()