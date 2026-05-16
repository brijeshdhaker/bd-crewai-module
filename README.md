# AI Project : bd-crewai-module

Welcome to the bd-crewai-module project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://knowledge.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/main/py/com/example/ai/apps/crewai/config/agents.yaml` to define your agents
- Modify `src/main/py/com/example/ai/apps/crewai/config/tasks.yaml` to define your tasks
- Modify `src/main/py/com/example/ai/apps/crewai/crew.py` to add your own logic, tools and specific args
- Modify `src/main/py/com/example/ai/apps/crewai/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the bd-crewai-module, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The bd-crewai-module is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `src/main/py/com/example/ai/apps/crewai/config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `src/main/py/com/example/ai/apps/crewai/config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the BdCrewaiModule Crew or crewAI.
- Visit our [documentation](https://knowledge.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.

### RAG : RAG has two completely separate workflows that you need to understand:
![](./knowledge/images/rag_flow_steps.jpg)

𝗢𝗳𝗳𝗹𝗶𝗻𝗲 — the ingestion pipeline (runs once, or on schedule)
① Load your documents (PDFs, URLs, code repos, Word files)
② Split them into small, meaningful passages (chunking)
③ Convert each passage into a vector — a mathematical fingerprint — using an embedding model
④ Store all vectors in a vector database (ChromaDB, FAISS, Pinecone, etc.)

𝗢𝗻𝗹𝗶𝗻𝗲 — the query pipeline (runs every time a user asks something)
① Receive the user's question
② Embed the question using the exact same embedding model
③ Find the most relevant passages via similarity search (top-k retrieval)
④ Inject those passages into the LLM prompt as context
⑤ The LLM generates an answer grounded in YOUR data


### Desing Flow for Design Documente Creation
![](./knowledge/images/RAG_001.png)


### Gmail Server MCP Server

```
send an email notification with folloing details: 
--recipient 'brijeshdhaker@gmail.com'
--subject 'AI Notification Test - 2026-04-17#{id}'
--body 'Hello {name},\n\n This is automated AI message send using AI Tools #Message-{id}'
--params {"id":"2001", "name":"Brijesh"}
```
### SQL Server MCP Server

```
fetch results for provided complex sql query with parameters :
--template select `NAME`, `AGE`, `ADDRESS`, CONVERT(SALARY, FLOAT) AS `SALARY` from CUSTOMERS WHERE ID = {id}
--params {"id":"1"}
```
### Install Application

```
python -m pip install -e .
```

### Create Py Whl files
```
uv build
uv build --wheel
uv pip install dist/bd_crewai_module-0.1.0-py3-none-any.whl
```

###
```
pip install dist/bd_crewai_module-0.1.0-py3-none-any.whl
python -m pip install dist/bd_crewai_module-0.1.0-py3-none-any.whl
```