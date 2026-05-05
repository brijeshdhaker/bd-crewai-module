import os
from crewai import Crew, Agent, Task, Process, LLM
from langchain_ollama import ChatOllama
from com.example.ai.LLMManager import LLMManager
from langchain.messages import SystemMessage, HumanMessage, AIMessage

# agent = LLMManager.get_agent()
# print(agent)
# aresponse=agent.invoke({"messages":HumanMessage(content="What's the weather like in Pune ?")})
# print(aresponse)
# print(aresponse['messages'][-1])

llm = LLMManager.get_model(temperature=0.3, max_tokens=1000)
print(llm)
  
# response=llm.invoke("Hello How are you ?")
# print(response)