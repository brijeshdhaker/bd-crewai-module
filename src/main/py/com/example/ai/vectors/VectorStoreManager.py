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
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
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
        
        # chroma run --path vectorstore/chroma
        self.folder = Path(f"{os.getenv("WORK_DIR")}/storage/{store_type}")
        if not os.path.exists(self.folder):
            os.makedirs(self.folder,exist_ok=True)
        
        #
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        #
        self.embeddings = HuggingFaceEmbeddings(
            model_name= "sentence-transformers/all-mpnet-base-v2",
            model_kwargs= {"device": "cpu"},
            encode_kwargs= {"normalize_embeddings": False}
        )
        
        #
        self._init_vectorstore()
    
    
    #    
    def _init_vectorstore(self) :
        #
        match self.store_type:
            case 'chromadb':
                #           
                client = chromadb.PersistentClient(path=str(self.folder))
                #
                self.vectorstore = Chroma(
                    client=client,
                    persist_directory=str(self.folder),
                    collection_name = self.collectionOrIndexName,
                    embedding_function=self.embeddings
                )

            case 'faissdb':
                #
                document=Document(
                    page_content="this is the main text content I am using to create RAG",
                    metadata={"source":"plain_text", "pages":1, "author":"Brijesh Dhaker", "date_created":"2025-01-01"}
                )
                # Check if it exists AND is a directory
                if os.path.exists(self.folder.joinpath(f"{self.collectionOrIndexName}.faiss")):
                    self.vectorstore = FAISS.load_local(
                        index_name = self.collectionOrIndexName,
                        folder_path = str(self.folder),
                        embeddings = self.embeddings, 
                        allow_dangerous_deserialization = True
                    )
                else :
                    #from langchain.storage import LocalFileStore
                    #vectorstore = FAISS.from_documents([document], self.embeddings)
                    index = faiss.IndexFlatL2(len(self.embeddings.embed_query(text="this is the main text content I am using to create RAG")))
                    self.vectorstore = FAISS(
                        index=index,
                        docstore= InMemoryDocstore(),
                        embedding_function=self.embeddings,
                        index_to_docstore_id={}
                    )
                    self.vectorstore.save_local(
                        folder_path=str(self.folder), 
                        index_name=self.collectionOrIndexName
                    )
            case _:
                pass
    
    #        
    def add_documents(self, documents: list[Document]):
        
        chunks = self.splitter.split_documents(documents=documents)
        print(f"[*INFO] Total {len(documents)} documents splitted into {len(chunks)} chunks.")
        #
        self.vectorstore.add_documents(documents=chunks)
        print(f"[*INFO] documents successfullu added to vectore store.")
        self.__save()
        print(f"[*INFO] documents successfullu persisted into local disk of vectorestore.")

    #
    def __save(self):
        if isinstance(self.vectorstore, FAISS):
            #
            self.vectorstore.save_local(folder_path=str(self.folder), index_name=self.collectionOrIndexName)
        
    #
    def retriever(self, **kwargs) -> VectorStoreRetriever :
        return self.vectorstore.as_retriever(**kwargs)
    

# Example usage
if __name__ == "__main__":
    #
    document_dir = "docs"
    #load_manager = LoadManager(document_dir)
    douments = LoadManager.from_directory(document_dir)
    print(f"[*INFO] Total loaded documents: {len(douments)}")
    
    #Convert the text to embeddings
    store_mgr = VectorStoreManager(store_type="faissdb", collectionOrIndexName="faiss_index")
    store_mgr.add_documents(douments)

    
        
    
