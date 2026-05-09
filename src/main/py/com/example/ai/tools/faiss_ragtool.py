from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field,PrivateAttr
from com.example.ai.vectors.VectorStoreManager import VectorStoreManager
from langchain_core.vectorstores import VectorStore
#
class DocumentQueryInput(BaseModel):
    query: str

#
class FAISSRagTool(BaseTool):
    """
    Retrieves informations using FAISS
    """
    name: str = "FAISS Rag Tool"
    description: str = "retrieves informations using FAISS"
    args_schema: Type[BaseModel] = DocumentQueryInput
    #vectorstore: VectorStore

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _run(self, query: str):
        #
        store_mgr = VectorStoreManager(store_type="faissdb", collectionOrIndexName="faiss_index")
        retriever = store_mgr.retriever(
            search_type="similarity",
            search_kwargs={
                "filter": {"source": "knowledge/pdfs/Easy_recipes.pdf"}, 
                "score_threshold": 0.8,
                "k": 5, 
                "fetch_k": 50
            }
        )
        documents = retriever.invoke(query)
        texts = [d.page_content for d in documents if d.page_content]
        return "\n\n".join(texts)

    def _arun(self, query: str):
        raise NotImplementedError("FAISSRagTool non supporta esecuzione asincrona.")