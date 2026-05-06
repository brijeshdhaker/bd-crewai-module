from com.example.ai.loader.LoadManager import LoadManager
from com.example.ai.vectors.VectorStoreManager import VectorStoreManager
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from pathlib import Path
import os
vectorstore = VectorStoreManager.getVectorStore(type="faissdb")

# douments = LoadManager.from_directory("documents/pdfs", inclusions=['pdf'])
# print(f"[*INFO] Total loaded documents: {len(douments)}")

# splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000,
#             chunk_overlap=200,
#             length_function=len,
#         )

# #
# chunks = splitter.split_documents(douments)
# print(f"[*INFO] Total chunks: {len(chunks)} for  documents: {len(douments)}")

# #
# vectorstore.add_documents(documents=chunks)

# if isinstance(vectorstore, FAISS):
#     print("This is a LangChain FAISS vectorstore.")
#     folder = Path(f"{os.getenv("WORK_DIR")}/storage/faissdb")
#     vectorstore.save_local(folder_path=str(folder), index_name="faiss_index")
# else:
#     print("This is not a LangChain FAISS vectorstore.")

#
results = vectorstore.similarity_search("How does exercise price determine for ESOP?", k=5)
#.search(query="How does exercise price determine for ESOP?", search_type='similarity')
print(len(results))
for d in results:
    print(d.page_content + "\n\n")
