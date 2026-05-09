from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from com.example.ai.tools.faiss_ragtool import FAISSRagTool
from langchain_community.document_loaders import PDFPlumberLoader
from com.example.ai.vectors.VectorStoreManager import VectorStoreManager

@CrewBase
class FAISSRagCrew:

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self,pdf_path):
        self.pdf_path=pdf_path
        self.vectorstore= None
        self.search_tool=FAISSRagTool()

    def prepare_rag(self):
        loader = PDFPlumberLoader(file_path=self.pdf_path)
        documents = loader.load()
        #self.vectorstore = VectorStoreManager(store_type="faissdb", collectionOrIndexName="faiss_index")
        #self.vectorstore.add_documents(documents)   

    @agent
    def pdf_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_researcher'],  # type: ignore[index]
            verbose=True,
            tools=[self.search_tool]
        )

    @agent
    def content_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['content_analyst'],  # type: ignore[index]
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],  # type: ignore[index]
        )

    @task
    def content_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_task'],  # type: ignore[index]
            output_file='outputs/rag_crew/FAISSRagCrewReport.md'
        )

    @crew
    def crew(self) -> Crew:
        self.prepare_rag()
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,

        )
