#
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from crewai import LLM

#
#
class LLMManager:
    """
    """
    @classmethod
    def get_agent(cls, provider: str = 'openai', **kwarg):
        load_dotenv()
        # Initialize models
        return create_agent(
            model=f"{provider}:{os.environ["OPENAI_MODEL_NAME"]}",
            system_prompt="You are a helpful assistant.",
            **kwarg
        )
    
    @classmethod
    def get_model(cls, provider: str = 'openai', **kwargs):
        # Initialize models
        return init_chat_model(
            #model_provider=provider, 
            model=f"{provider}:{os.environ["OPENAI_MODEL_NAME"]}", 
            **kwargs
        )
    
    #
    @classmethod
    def create_llm(cls, type: str = 'openai', **kwargs) -> LLM :
        load_dotenv()
        # Ollama llm client
        if type == 'ollama' :
            # LLM setup using litellm additional_params={"num_ctx":16384},
            return LLM(
                model=f"ollama/{os.environ["OPENAI_MODEL_NAME"]}", 
                base_url=os.environ["OLLAMA_URL"], 
                temperature=0.3,     # Controls randomness in output (0.0 to 1.0)
                max_tokens=4096,     # Maximum number of tokens to generate
                timeout=300,         # timeout for llm
                #seed=21,            # Ensures consistent outputs
                #top_p=0.9           # Controls diversity of output (0.0 to 1.0)
                **kwargs
            )
        # Groq llm client
        if type == 'groq' :
            return LLM(
                model=f"groq/{os.environ["GROQ_MODEL_NAME"]}", 
                base_url=os.environ["GROQ_ENDPOINT"],
                **kwargs
            )
        # OpenAI llm client
        if type == 'openai' or type == 'hf':
            return LLM(
                model=f"openai/{os.environ["OPENAI_MODEL_NAME"]}", 
                base_url=os.environ["OPENAI_API_BASE"],
                temperature=0.3,     # Controls randomness in output (0.0 to 1.0)
                max_tokens=4096,     # Maximum number of tokens to generate
                timeout=300,         # timeout for llm
                #seed=21,            # Ensures consistent outputs
                #top_p=0.9           # Controls diversity of output (0.0 to 1.0)
                **kwargs
            )