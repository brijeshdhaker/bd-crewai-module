from datetime import datetime
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from com.example.ai.config import _rag_tool_config, _embedder_config_st
from com.example.ai.LLMManager import LLMManager
from com.example.ai.tools.ImageFetchTool import image_fetch_tool

from pydantic import BaseModel, Field
from typing import List, Dict

class ResearchPoint(BaseModel):
    topic: str = Field(description="The main topic or area being discussed")
    findings: str = Field(description="The key findings or insights about this topic")
    relevance: str = Field(description="Why this finding is relevant or important")
    sources: List[Dict[str, str]] = Field(
        description="Webpage information with title and url",
        default_factory=list
    )

class ResearchOutput(BaseModel):
    research_points: List[ResearchPoint] = Field(description="List of research findings")
    summary: str = Field(description="Brief summary of overall findings")

class ResearchImage(BaseModel):
    title: str = Field(description="The title of the image")
    url: str = Field(description="The url of the image")

class ResearchImageOutput(BaseModel):
    topic: str = Field(description="The details about primary topic")    
    images: List[ResearchImage] = Field(description="List of top images on topic")
    

class ExecutiveReportSection(BaseModel):
    section_emoji: str = Field(description="Section emoji (e.g., 🔍, 📊, 🎯)")
    section_title: str = Field(description="Section title")
    section_content: str = Field(description="Main content of the section")
    key_insights: List[str] = Field(description="Key insights from this section")
    recommendations: List[str] = Field(
        default_factory=list,
        description="Optional recommendations based on findings"
    )
    sources: List[Dict[str, str]] = Field(
        description="Sources with title and URL for this section",
        default_factory=list
    )

class ExecutiveReport(BaseModel):
    report_title: str = Field(description="Title of the report")
    generation_date: str = Field(description="Report generation date")
    executive_summary: str = Field(description="A concise executive summary")
    key_findings: List[Dict[str, str]] = Field(
        description="List of key findings with their sources",
        default_factory=list
    )
    report_sections: List[ExecutiveReportSection] = Field(
        description="Detailed report sections"
    )
    next_steps: List[str] = Field(description="Recommended next steps")
    sources: List[Dict[str, str]] = Field(
        description="All sources used in the report",
        default_factory=list
    )
    references : List[ResearchImage] = Field(description="References of top images on topic")


@CrewBase
class DesignDevelopment():
    """Latest AI Design Development Crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def content_researcher(self) -> Agent:
        return Agent(
            config = self.agents_config['content_researcher'],
            verbose = True,
            tools = [
                SerperDevTool(),
                ScrapeWebsiteTool()
                # DesignSearchTool()
            ],
            allow_delegation = False,
            #knowledge_sources=[text_kw_source],
            #embedder=_rag_tool_config['embedder'],
            #llm=LLMManager.create_llm()
        )
    
    @agent
    def images_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['images_extractor'],
            #knowledge_sources=[desing_images],
            verbose=True,
            tools=[image_fetch_tool],
            #embedder=_rag_tool_config['embedder'],
            #llm=LLMManager.create_llm()
        )
    
    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True,
            #llm=LLMManager.create_llm()
        )
    
    @agent
    def formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['formatter'],
            verbose=True,
            #llm=LLMManager.create_llm()
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], 
            output_json=ResearchOutput
        )


    @task
    def extract_images_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_images_task'],
            output_json=ResearchImageOutput,
            #context=[self.research_task()]
        )
    
    
    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_pydantic=ExecutiveReport
        )

    @task
    def formatting_task(self) -> Task:
        return Task(
            config=self.tasks_config['formatting_task']
        )

	
    @crew
    def crew(self) -> Crew:
        """Creates the DesignDevelopment Crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            embedder=_embedder_config_st
        )