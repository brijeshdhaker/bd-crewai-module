import os
import shutil
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def cleanup_chroma_db():
    try:
        if os.path.exists(f"{os.environ['WORK_DIR']}/storage/chromadb"):
            shutil.rmtree(f"{os.environ['WORK_DIR']}/storage/chromadb")
    except Exception as e:
        print(f"Exception - Could not clean up ChromaDB directory: {str(e)}")

def process_document(text):
    try:
        cleanup_chroma_db()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
        )

        docs = splitter.create_documents([text])
        try:
            # all-MiniLM-L6-v2
            embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
            # embeddings = OpenAIEmbeddings()
            vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                collection_name="research_papers",
                persist_directory=f"{os.environ["WORK_DIR"]}/storage/chromadb"
            )
            return vectorstore

        except Exception as chroma_error:
            print(f"WARNING - ChromaDB failed, trying FAISS: {str(chroma_error)}")
            vectorstore = FAISS.from_documents(
                documents=docs,
                embedding=embeddings,
            )
            vectorstore.save_local(f"{os.environ["WORK_DIR"]}/storage/faissdb")
            return vectorstore            

    except Exception as e:
        print(f"Exception - Error processing document: {str(e)}")
        cleanup_chroma_db()
        return None