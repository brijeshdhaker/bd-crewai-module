#
# python src/main/py/com/example/agentic/mcp/mcp-client.py
#

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv

"""

"""
async def main():
    #
    client = MultiServerMCPClient({
                
        "weather-mcp-client":{
            "url":"http://127.0.0.1:8011/mcp",                                  # Ensure Server is Running Here
            "transport":"streamable_http"
        },

        "email-mcp-client":{
            "url":"http://127.0.0.1:8000/mcp",  # Ensure Server is Running Here
            "transport":"streamable_http"
        },
        
        "mysql-mcp-client":{
            "command":"python",
            "args":["src/main/py/com/example/agentic/mcp/mysqlserver.py"],           # Put absolute path here
            "transport":"stdio",
            "env":{
                "WORK_DIR":"/home/brijeshdhaker/IdeaProjects/bd-notebooks-module",
                "PYTHONPATH": "/home/brijeshdhaker/IdeaProjects/bd-notebooks-module/src/main/py"
            },
            "cwd":"/home/brijeshdhaker/IdeaProjects/bd-notebooks-module"
        },

        "math-mcp-client":{
            "command":"python",
            "args":["src/main/py/com/example/agentic/mcp/mathserver.py"],           # Put absolute path here
            "transport":"stdio",
            "env":{
                "EMAIL_USER": "",
                "PYTHONPATH": "/home/brijeshdhaker/IdeaProjects/bd-notebooks-module/src/main/py"
            },
            "cwd":"/home/brijeshdhaker/IdeaProjects/bd-notebooks-module"
        },
    })

    #
    import os
    import getpass
    from langchain.chat_models import init_chat_model

    #
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

    #
    _tools = await client.get_tools()

    #
    model=init_chat_model(model="groq:openai/gpt-oss-20b")

    #
    agent = create_agent(model, _tools)
    
    #
    _messages = [
        "What is (3 + 5)*12 ?",
        "What is weather in 'Mumbia' ?",
        """
        send an email with folloing details: 
        --recipient 'brijeshdhaker@gmail.com'
        --subject 'AI Notification Test'
        --body 'This is automated AI message send using AI Tools.'
        """,
        "Hello, Good Morning !!"
    ]

    for _m in _messages:
        _response = await agent.ainvoke({"messages":[{ "role":"user", "content":_m }]})
        print("email_response : " + _response["messages"][-1].content)

# To call async method 
asyncio.run(main())

    



