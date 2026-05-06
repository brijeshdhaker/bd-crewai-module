import os
import faiss
from pathlib import Path
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import numpy as np
import pickle
from typing import List, Any
from sentence_transformers import SentenceTransformer
from com.example.ai.embedding.EmbeddingManager import EmbeddingManager
from com.example.ai.loader.LoadManager import LoadManager
from com.example.ai.vectors.VectorStore import VectorStore
from langchain_core.vectorstores import VectorStore
import chromadb
from chromadb.config import Settings
import uuid

class ChromaVectorStore(VectorStore):
    """
    ChromaVectorStore
    """
    def __init__(self, collection_name: str = "sandbox_documents" , persist_dir: str = "chromadb"):
        
        super().__init__(persist_dir) 
        self.collection_name = collection_name
        self._initialize_store()

    #
    def _initialize_store(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create persistent ChromaDB client
            os.makedirs(self.persist_directory, exist_ok=True)
            # chroma run --path vectorstore/chroma
            #Chroma.from_documents(persist_directory=self.persist_directory)
            #OllamaEmbeddings(model="nomic-embed-text", url="http://localhost:11434/api/embed")
            #db = Chroma(persist_directory=self.persist_directory, embedding_function=OpenAIEmbeddings());
            _settings = Settings(allow_reset=False, is_persistent=True, anonymized_telemetry=False, persist_directory=str(self.persist_directory))
            self.client = chromadb.PersistentClient(path=str(self.persist_directory), settings=_settings)
            #self.client = chromadb.HttpClient(host="localhost", port=8000, ssl=False)

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Documents Embeddings for RAG"}
            )
            print(f"Vector store initialized. Collection: {self.collection_name}")
            print(f"Existing documents in collection: {self.collection.count()}")
            
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            raise
    
    #
    def build_from_documents(self, documents: List[Any]):
        print(f"[INFO] Building croma vector store from {len(documents)} raw documents...")
        chunks = self.embeddingManager.chunk_documents(documents)
        embeddings = self.embeddingManager.embed_chunks(chunks)
        if len(chunks) != len(embeddings):
            raise ValueError("Number of documents chunks must match number of embeddings")
        print(f"Adding {len(chunks)} documents to vector store...")
        
        # Prepare data for ChromaDB
        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []
        
        for i, (doc, embedding) in enumerate(zip(chunks, embeddings)):
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
    
    def search(self, query_text: str, top_k: int = 5):
        results = self.retrieve(query_text, top_k)
        return results

    def query(self, query_text: str, top_k: int = 5):
        print(f"[INFO] Querying vector store for: '{query_text}'")
        #query_embedding = self.embeddingManager.embed_query([query_text])[0]
        #query_embedding = self.model.encode([query_text]).astype('float32')
        return self.search(query_text, top_k=top_k)

    #
    def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.0):
        """
        Retrieve relevant documents for a query
        Args:
            query: The search query
            top_k: Number of top results to return
            score_threshold: Minimum similarity score threshold
        Returns:
            List of dictionaries containing retrieved documents and metadata
        """
        print(f"Retrieving documents for query: '{query}'")
        print(f"Top K: {top_k}, Score threshold: {score_threshold}")
        
        # Generate query embedding
        query_embedding = self.embeddingManager.embed_query([query])[0]
        
        # Search in vector store
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k
            )
            
            # Process results
            retrieved_docs = []
            
            if results['documents'] and results['documents'][0]:
                documents = results['documents'][0]
                metadatas = results['metadatas'][0]
                distances = results['distances'][0]
                ids = results['ids'][0]
                
                for i, (doc_id, document, metadata, distance) in enumerate(zip(ids, documents, metadatas, distances)):
                    # Convert distance to similarity score (ChromaDB uses cosine distance)
                    similarity_score = 1 - distance
                    
                    if similarity_score >= score_threshold:
                        retrieved_docs.append({
                            'id': doc_id,
                            'content': document,
                            'metadata': metadata,
                            'similarity_score': similarity_score,
                            'distance': distance,
                            'rank': i + 1
                        })
                
                print(f"Retrieved {len(retrieved_docs)} documents (after filtering)")
            else:
                print("No documents found")
            
            return retrieved_docs
            
        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []


# Example usage
if __name__ == "__main__":
    
    #
    #douments = LoadManager.from_directory("docs/text", inclusions=["txt"])
    #print(f"[*INFO] Total loaded documents: {len(douments)}")
    
    # Connect to knowledge store vectorstore.
    store = ChromaVectorStore()
    #store.build_from_documents(douments)
    print(store.query("What are benefits of microservices ?", top_k=10))