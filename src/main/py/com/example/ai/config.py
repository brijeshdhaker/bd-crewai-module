import os
from dotenv import load_dotenv

"""
"""
from crewai_tools.tools.rag import RagToolConfig, VectorDbConfig, ProviderSpec
from crewai.rag.embeddings.providers.openai.types import OpenAIProviderSpec
from crewai.rag.embeddings.providers.ollama.types import OllamaProviderSpec
from crewai.rag.embeddings.providers.huggingface.types import HuggingFaceProviderSpec
from crewai.rag.embeddings.providers.sentence_transformer.types import SentenceTransformerProviderSpec

load_dotenv()

#
# Embedders : 
#
_embedder_config_openai: OpenAIProviderSpec = {
    "provider": "openai",
    "config": {
        "model_name": os.environ["OPENAI_EMBEDDING_MODEL_ID"],
        "organization_id":"sandbox",
        "api_base":"http://localhost:11434/v1",
        "api_version":"v1",
        "api_key":"ollama",
        "api_type":"ollama",
        "dimensions":768,
        "default_headers":{"X-Custom-Header": "ollama"}
    }
}

_embedder_config_ollama: OllamaProviderSpec = {
    "provider": "ollama",
    "config": {
        "model_name": os.environ["OPENAI_EMBEDDING_MODEL_ID"],
        "url":"http://localhost:11434/v1"
    }
}

_embedder_config_st: SentenceTransformerProviderSpec = {
    "provider": "sentence-transformer",
    "config": {
        "model_name": "all-mpnet-base-v2",
        "device":"cpu",
        "normalize_embeddings": False
    }
}

_embedder_config_hf = {
    "provider": "huggingface", 
    "config": {
        "model_name": "sentence-transformers/all-mpnet-base-v2",
        "task_type": "retrieval_document",
        "title": "Embeddings"
    }
}

#
# Embedding Models 
#

_embedding_model_openai: OpenAIProviderSpec = {
    "provider": "openai",
    "config": {
        "model_name": os.environ["OPENAI_EMBEDDING_MODEL_ID"],
        "organization_id":"sandbox",
        "api_base":"http://localhost:11434/v1",
        "api_version":"v1",
        "api_key":"ollama",
        "api_type":"ollama",
        "dimensions":768,
        "default_headers":{"X-Custom-Header": "ollama"}
    }
}

_embedding_model_ollama: OllamaProviderSpec = {
    "provider": "ollama",
    "config": {
        "model_name": os.environ["OPENAI_EMBEDDING_MODEL_ID"],
        "url":"http://localhost:11434/v1"
    }
}

# all-MiniLM-L6-v
# all-mpnet-base-v2
_embedding_model_st: SentenceTransformerProviderSpec = {
    "provider": "sentence-transformer",
    "config": {
        "model_name": "all-mpnet-base-v2",
        "device":"cpu",
        "normalize_embeddings": False
    }
}

_embedding_model_hf: HuggingFaceProviderSpec = {
    "provider": "huggingface",
    "config": {
        "model": "sentence-transformers/all-mpnet-base-v2"
    }
}

_vectordb_chromadb = VectorDbConfig = {
    "provider": "chromadb",
    "config": {
        "collection_name": "sandbox_documents",
        "persist_directory":f"{os.environ["WORK_DIR"]}/storage/chromadb", 
        "allow_reset": False, 
        "is_persistent": True
    }
}

# LLMs
_llm_openai = dict(
    provider="openai",
    config=dict(
        model=os.environ["OPENAI_MODEL_NAME"],
        base_url="http://localhost:11434/v1",
        max_tokens=4096,
        temperature=0.3,
        timeout=300,
        # top_p=1,
        # stream=true,
    ),
)

_llm_ollama = dict(
    provider="ollama",
    config=dict(
        model=os.environ["OPENAI_MODEL_NAME"],
        base_url="http://localhost:11434",
        temperature=0.3,
        max_tokens=4096,
        timeout=300,
        # num_predict=256,
        # top_p=1,
        # stream=true,
    ),
)

def create_rag_config(type: str = 'openai') :
    #
    _tool_config = dict( chunk_size=1000, chunk_overlap=200, batch_size = 100,
        llm = _llm_ollama,
        embedder = _embedding_model_st,
        embedding_model = _embedding_model_st,
        vectordb= _vectordb_chromadb
    )
    #
    match type:
        case 'openai':
            _tool_config['llm'] = _llm_openai
            _tool_config['embedder'] = _embedding_model_st
            _tool_config['embedding_model'] = _embedding_model_st
        case 'ollama':
            _tool_config['llm'] = _llm_ollama
            _tool_config['embedder'] = _embedding_model_st
            _tool_config['embedding_model'] = _embedding_model_st
        case 'groq':
            _tool_config['llm'] = _llm_openai
            _tool_config['embedder'] = _embedding_model_st
            _tool_config['embedding_model'] = _embedding_model_st
        case _:
            pass

    return _tool_config


#
_tool_config = dict(
    chunk_size=1000, 
    chunk_overlap=200,
    batch_size = 100,
    llm= _llm_ollama,
    embedder = _embedding_model_st,
    embedding_model = _embedding_model_st,
    vectordb= _vectordb_chromadb
)

_rag_tool_config = dict(
    chunk_size=1000, 
    chunk_overlap=200,
    batch_size = 100,
    llm = _llm_openai,
    embedder = _embedding_model_openai,
    embedding_model = _embedding_model_st,
    vectordb = _vectordb_chromadb
)

## Memory
from com.example.ai.LLMManager import LLMManager
from crewai import Memory

def create_memory(type: str = 'openai') -> Memory :
    _llm = LLMManager.create_llm(type)
    _embedder = _embedding_model_openai
    # 
    if type == 'ollama' :
        _embedder = _embedding_model_ollama
    # 
    if type == 'hf' :
        _embedder = _embedding_model_hf
    
    return Memory(
        llm=_llm,
        embedder=_embedding_model_st
    )
