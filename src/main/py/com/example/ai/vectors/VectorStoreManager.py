import os
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
class VectorStoreManager:
    """Manages document embeddings in a ChromaDB vector store"""
    
    def __init__(self, 
                 collection_name: str = "sandbox_documents", 
                 persist_directory: str = "chromadb"):
        """
        Initialize the vector store
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the vector store
        """
        ## Create a simple txt file
        work_dir = os.getenv("WORK_DIR")
        os.makedirs(f"{work_dir}/storage/chromadb",exist_ok=True)
        self.collection_name = collection_name
        self.persist_directory = f"{work_dir}/storage/{persist_directory}"
        self.client = None
        self.collection = None
        self._initialize_store()
    
    #
    def _initialize_store(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create persistent ChromaDB client
            os.makedirs(self.persist_directory, exist_ok=True)
            # chroma run --path vectorstore/chroma
            #Chroma.from_documents(persist_directory=self.persist_directory)
            #self.client = chromadb.PersistentClient(path=self.persist_directory)
            #db = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings());
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            #self.client = chromadb.HttpClient(host="localhost", port=8000, ssl=False)

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Document Embeddings for RAG"}
            )
            print(f"Vector store initialized. Collection: {self.collection_name}")
            print(f"Existing documents in collection: {self.collection.count()}")
            
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            raise



    #        
    def add_documents(self, documents: List[Any], embeddings: np.ndarray):
        """
        Add documents and their embeddings to the vector store
        Args:
            documents: List of LangChain documents
            embeddings: Corresponding embeddings for the documents
        """
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings")
        
        print(f"Adding {len(documents)} documents to vector store...")
        
        # Prepare data for ChromaDB
        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []
        
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            # Generate unique ID
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)
            
            # Prepare metadata
            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['content_length'] = len(doc.page_content)
            metadatas.append(metadata)
            
            # Document content
            documents_text.append(doc.page_content)
            
            # Embedding
            embeddings_list.append(embedding.tolist())
        
        # Add to collection
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings_list,
                metadatas=metadatas,
                documents=documents_text
            )
            print(f"Successfully added {len(documents)} documents to vector store")
            print(f"Total documents in collection: {self.collection.count()}")
            
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            raise

# Example usage
if __name__ == "__main__":
    #
    document_dir = "docs"
    #load_manager = LoadManager(document_dir)
    douments = LoadManager.from_directory(document_dir)
    print(f"[*INFO] Total loaded documents: {len(douments)}")
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    chunks = splitter.split_documents(douments)

    #
    embedding_manager=EmbeddingManager()
    embeddings = embedding_manager.embed_documents(chunks)
    
    #Convert the text to embeddings
    vectorstore = VectorStoreManager()
    vectorstore.add_documents(chunks,embeddings)
        
    
