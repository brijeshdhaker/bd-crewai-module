from ast import match_case
import os
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS

import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
#from langchain_chroma import Chroma
import uuid
from typing import List, Dict, Any, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from com.example.ai.loader.LoadManager import LoadManager
from com.example.ai.embedding.EmbeddingManager import EmbeddingManager
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import VectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from pathlib import Path
from langchain_classic.storage import LocalFileStore
from langchain_core.documents import Document

class VectorStoreManager:
    """Manages document embeddings in a ChromaDB vector store"""
    
    def __init__(self, store_type: str = "chromadb", collectionOrIndexName: str = "sandbox_documents"):
        """
        Initialize the vector store
        Args:
            collectionOrIndexName: Name of the ChromaDB collection or faiss indexname
        """
        ## Create a simple txt file
        self.store_type = store_type
        self.collectionOrIndexName = collectionOrIndexName

        self.embeddings = HuggingFaceEmbeddings(
            model_name= "sentence-transformers/all-mpnet-base-v2",
            model_kwargs= {"device": "cpu"},
            encode_kwargs= {"normalize_embeddings": False}
        )
        self.vectorstore = VectorStoreManager.getVectorStore(
            type=store_type, 
            collectionOrIndexName=collectionOrIndexName, 
            embeddings=self.embeddings
        )
        
    
    #
    @classmethod
    def getVectorStore(cls, type: str = "chromadb", **kwargs) -> VectorStore :
        
        #
        embeddings = HuggingFaceEmbeddings(
            model_name= "sentence-transformers/all-mpnet-base-v2",
            model_kwargs= {"device": "cpu"},
            encode_kwargs= {"normalize_embeddings": False}
        )

        match type:
            case 'chromadb':
                
                # chroma run --path vectorstore/chroma
                folder = Path(f"{os.getenv("WORK_DIR")}/storage/chromadb")
                if not os.path.exists(folder):
                    os.makedirs(f"{os.getenv("WORK_DIR")}/storage/chromadb",exist_ok=True)
                #           
                client = chromadb.PersistentClient(path=f"{os.getenv("WORK_DIR")}/storage/chromadb")
                
                #
                vectorstore = Chroma(
                    client=client,
                    persist_directory=f"{os.getenv("WORK_DIR")}/storage/chromadb",
                    collection_name = "sandbox_documents",
                    embedding_function=embeddings
                )

            case 'faissdb':
                #
                document=Document(
                    page_content="this is the main text content I am using to create RAG",
                        metadata={
                            "source":"plain_text",
                            "pages":1,
                            "author":"Brijesh Dhaker",
                            "date_created":"2025-01-01"
                        }
                )
                index = faiss.IndexFlatL2(len(embeddings.embed_documents([document.page_content])))
                folder = Path(f"{os.getenv("WORK_DIR")}/storage/faissdb")
                # Check if it exists AND is a directory
                if folder.is_dir() and os.path.exists(folder):
                    vectorstore = FAISS.load_local(
                        index_name="faiss_index",
                        folder_path=str(folder),
                        embeddings=embeddings, 
                        allow_dangerous_deserialization=True
                    )
                else :
                    #from langchain.storage import LocalFileStore
                    vectorstore = FAISS.from_documents([document], embeddings)
                    # vectorstore = FAISS(
                    #     index=index,
                    #     docstore= InMemoryDocstore(),
                    #     embedding_function=embeddings,
                    #     index_to_docstore_id={}
                    # )
                    vectorstore.save_local(
                        folder_path=str(folder), 
                        index_name="faiss_index"
                    )
            case _:
                pass
        #
        return vectorstore
        
    
    #        
    def add_documents(self, documents: list[Document]):
        #
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_documents(documents=documents)
        #
        self.vectorstore.add_documents(documents=chunks)
        self.__save()

    #
    def __save(self):
        if isinstance(self.vectorstore, FAISS):
            folder = Path(f"{os.getenv("WORK_DIR")}/storage/faissdb")
            self.vectorstore.save_local(folder_path=str(folder), index_name=self.collectionOrIndexName)
        
        

# Example usage
if __name__ == "__main__":
    #
    document_dir = "docs"
    #load_manager = LoadManager(document_dir)
    douments = LoadManager.from_directory(document_dir)
    print(f"[*INFO] Total loaded documents: {len(douments)}")
    
    #Convert the text to embeddings
    vectorstore = VectorStoreManager()
    vectorstore.add_documents(douments)
        
    
