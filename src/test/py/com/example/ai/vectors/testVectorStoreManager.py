from com.example.ai.loader.LoadManager import LoadManager
from com.example.ai.vectors.VectorStoreManager import VectorStoreManager
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from pathlib import Path
import os
from langchain_community.document_loaders import PDFPlumberLoader

#
store_mgr = VectorStoreManager(store_type="faissdb", collectionOrIndexName="faiss_index")
# store_mgr = VectorStoreManager(store_type="chromadb", collectionOrIndexName="sandbox-documents")

#
# loader = PDFPlumberLoader(file_path="knowledge/pdfs/Easy_recipes.pdf")
# documents = loader.load()

# # documents = LoadManager.from_directory("knowledge/pdfs", inclusions=['pdf'])

#
# store_mgr.add_documents(documents=documents)

# #
# results = store_mgr.vectorstore.similarity_search("All recipes with rice ?", k=5)
# #.search(query="How does exercise price determine for ESOP?", search_type='similarity')

# # Retrieve more documents with higher diversity
# # Useful if your dataset has many similar documents
# store_mgr.retriever(
#     search_type="mmr", search_kwargs={"k": 6, "lambda_mult": 0.25}
# )

# # Fetch more documents for the MMR algorithm to consider
# # But only return the top 5
# store_mgr.retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 50})

# # Only retrieve documents that have a relevance score
# # Above a certain threshold
# store_mgr.retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={"score_threshold": 0.8},
# )

# # Only get the single most similar document from the dataset
# store_mgr.vectorstore.as_retriever(search_kwargs={"k": 1})

# Use a filter to only retrieve documents from a specific paper
# similarity, similarity_score_threshold, mmr
retriever = store_mgr.retriever(
    search_type="similarity", 
    search_kwargs={
        "filter": {"source": "knowledge/pdfs/Easy_recipes.pdf"}, 
        "k": 5,
        # "score_threshold": 0.8,
        # "fetch_k": 50
    }
)

results = retriever.invoke(input="All recipes with rice ?")
print(len(results))
for d in results:
    print(d.page_content + "\n\n")
