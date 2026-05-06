from com.example.ai.loader.LoadManager import LoadManager
from com.example.ai.vectors.VectorStoreManager import VectorStoreManager
from langchain_text_splitters import RecursiveCharacterTextSplitter
from com.example.ai.LLMManager import LLMManager

class RAGSearch:
    
    #
    def __init__(self, collectionOrIndexName: str = "faiss_index"):
        
        #
        self.vectorstore = VectorStoreManager.getVectorStore(type="faissdb")
        
        #    
        self.llm = LLMManager.get_model()
        print(f"[INFO] LLM initialized: {self.llm.name}")

    #
    def load_documents(self) :

        douments = LoadManager.from_directory("documents/pdfs", inclusions=['pdf'])
        
        print(f"[*INFO] Total loaded documents: {len(douments)}")
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        #
        chunks = splitter.split_documents(douments)
        print(f"[*INFO] Total chunks: {len(chunks)} for  documents: {len(douments)}")
        #
        self.vectorstore.add_documents(documents=chunks)



    def search_and_summarize(self, topic: str, top_k: int = 5) -> str:

        documents = self.vectorstore.similarity_search(query=topic, k=top_k)
        texts = [d.page_content for d in documents if d.page_content]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found."
        prompt = f"""Summarize the following context for the query: '{query}'\n\nContext:\n{context}\n\nSummary:"""
        response = self.llm.invoke([prompt])
        return response.content


# Example usage
if __name__ == "__main__":
    rag_search = RAGSearch()
    query = "How does exercise price determine for ESOP ?"
    summary = rag_search.search_and_summarize(query, top_k=3)
    print("Summary:", summary)