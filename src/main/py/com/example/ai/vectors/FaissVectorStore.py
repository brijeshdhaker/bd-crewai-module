import os
import faiss
from pathlib import Path
import numpy as np
import pickle
from typing import List, Any
from sentence_transformers import SentenceTransformer
from com.example.ai.embedding.EmbeddingManager import EmbeddingManager
from com.example.ai.loader.LoadManager import LoadManager
from com.example.ai.vectors.VectorStore import VectorStore
import uuid

#
class FaissVectorStore(VectorStore):
    """
    FaissVectorStore : Facebook AI Similarity Search
    """
    def __init__(self, persist_dir: str = "faissdb"):
        #        
        super().__init__(persist_dir)
        #
        self.faiss_path = os.path.join(self.persist_directory, "faiss.index")
        self.meta_path = os.path.join(self.persist_directory, "metadata.pkl")
        self.index = None
        self.metadata = []
        self._initialize_store()

    #
    def _initialize_store(self):
        """Initialize FaissVector Store"""
        try:
            # Create persistent ChromaDB client
            os.makedirs(self.persist_directory, exist_ok=True)
            #
            self.index = faiss.read_index(str(self.faiss_path))
            #
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)
            print(f"[INFO] Loaded Faiss index and metadata from {self.persist_directory}")

        except Exception as e:
            print(f"Error initializing vector store: {e}")
            raise        
    
    #
    def build_from_documents(self, documents: List[Any]):
        print(f"[INFO] Building vector store from {len(documents)} raw documents...")
        chunks = self.embeddingManager.chunk_documents(documents)
        embeddings = self.embeddingManager.embed_chunks(chunks)

        # Prepare data for Faiss Vector Store
        ids = []
        metadatas = []
        embeddings_list = []
        
        for i, (doc, embedding) in enumerate(zip(chunks, embeddings)):
            # Generate unique ID
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)
            
            # Prepare metadata
            metadata = dict(doc.metadata)
            metadata['doc_index'] = doc_id
            metadata['content_length'] = len(doc.page_content)
            metadata['content'] = doc.page_content
            metadatas.append(metadata)
            
            # Embedding
            embeddings_list.append(embedding.tolist())

        # Add to Vector Store
        try:
            self._add_embeddings(np.array(embeddings_list).astype('float32'), metadatas)
            self._save()
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            raise
        print(f"[INFO] Vector store built and saved to {self.persist_directory}")
        print(f"Successfully added {len(documents)} documents to vector store")

    #
    def _add_embeddings(self, embeddings: np.ndarray, metadatas: List[Any] = None):
        dim = embeddings.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        if metadatas:
            self.metadata.extend(metadatas)
        print(f"[INFO] Added {embeddings.shape[0]} vectors to Faiss index.")

    #
    def _save(self):
        faiss.write_index(self.index, str(self.faiss_path))
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
        print(f"[INFO] Saved Faiss index and metadata to {self.persist_directory}")

    #
    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        # D → distances, 
        # I → indices of matching chunks.
        D, I = self.index.search(query_embedding, top_k)
        results = []
        for i, (idx, distance) in enumerate(zip(I[0], D[0])):
            metadata = self.metadata[idx] if idx < len(self.metadata) else None
            similarity_score = 1 - distance
            results.append({
                "id": metadata['doc_index'],
                "content": metadata['content'],
                "content_length": metadata['content_length'], 
                "distance": distance,
                "similarity_score": similarity_score, 
                "metadata": metadata,
                "rank": i + 1
            })
        return results

    def query(self, query_text: str, top_k: int = 5):
        print(f"[INFO] Querying vector store for: '{query_text}'")
        qm_embedding = self.embeddingManager.embed_query([query_text])
        qt_embedding = self.model.encode([query_text]).astype('float32')
        return self.search(qt_embedding, top_k=top_k)

# Example usage
if __name__ == "__main__":
    
    #
    #douments = LoadManager.from_directory("docs/text", inclusions=["txt"])
    #print(f"[*INFO] Total loaded documents: {len(douments)}")
    store = FaissVectorStore("faissdb")
    #store.build_from_documents(douments)
    #store.load()
    print(store.query("What are benefits of microservices ?", top_k=3))