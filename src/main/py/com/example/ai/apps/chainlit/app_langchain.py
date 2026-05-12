from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_core.runnables import RunnableConfig
from typing import cast
from com.example.ai.LLMManager import LLMManager
import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    #model = ChatOpenAI(streaming=True)
    model = LLMManager.get_model(streaming=True) 
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions."),
        ("human", "{question}"),
    ])
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cast(Runnable, cl.user_session.get("runnable"))  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()