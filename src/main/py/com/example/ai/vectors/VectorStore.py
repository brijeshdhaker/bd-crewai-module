import os
from abc import ABC, abstractmethod
from typing import List, Any
from pathlib import Path
from sentence_transformers import SentenceTransformer
from com.example.ai.embedding.EmbeddingManager import EmbeddingManager

class VectorStore(ABC):
    
    def __init__(self, 
                 persist_dir: str = "chromadb",
                 embedding_model: str = "all-mpnet-base-v2", #all-MiniLM-L6-v2
                 chunk_size: int = 1000, 
                 chunk_overlap: int = 200):
        
        self.persist_directory = Path(f"{os.environ["WORK_DIR"]}/storage/{persist_dir}").resolve()
        self.metadata = []
        self.embedding_model = embedding_model
        self.model = SentenceTransformer(embedding_model)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddingManager = EmbeddingManager(model_name=self.embedding_model, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        #print(f"BaseMachine initialized: {self.model_name}")

    @abstractmethod
    def build_from_documents(self, documents: List[Any]):
        pass 

    @abstractmethod
    def query(self, query_text: str, top_k: int = 5):
        pass 

# class Dog(Animal):
#     def sound(self):
#         return "Bark"

# dog = Dog()
# print(dog.sound())