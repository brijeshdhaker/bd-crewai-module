#
# create a FAISS index and add our vector embeddings to the index
#

import faiss
import numpy as np

# Create a FAISS index
num_vectors = len(document_embeddings)
dim = len(document_embeddings[0])
faiss_index = faiss.IndexFlatIP(dim)  # Inner product for cosine similarity

# Add vectors to the FAISS index
faiss_index.add(np.array(document_embeddings, dtype=np.float32))

#
# 1. Similarity Search
#

# Load or generate a query vector
query_vector = model.encode(['This is a sample query text'])

k = 5  # Number of nearest neighbors to retrieve
distances, indices = faiss_index.search(np.array([query_vector], dtype=np.float32), k)

# Print the most similar documents
for i, index in enumerate(indices[0]):
    distance = distances[0][i]
    print(f"Nearest neighbor {i+1}: {documents[index]}, Distance {distance}")