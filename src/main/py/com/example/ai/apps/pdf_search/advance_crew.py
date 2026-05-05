from crewai import Crew, Agent, Task, Process, LLM
from langchain_openai import ChatOpenAI
from com.example.ai.apps.pdf_search.basic_crew import retrieval_action, generation_action

def create_advanced_crew(vectorstore, status_callback=None):
    def retrieval_wrapper(question):
        if status_callback:
            status_callback("Searching for relevant passages in the research paper...")

        result = retrieval_action(question, vectorstore)

        if status_callback:
            status_callback("Found relevant passages for analysis")

        return result    

    def generation_wrapper(inputs):
        if status_callback:
            status_callback("Analyzing retrieved passages and generating comprehensive answer...")

        result = generation_action(inputs)

        if status_callback:
            status_callback("Generated detailed answer with citations")

        return result

    retriever = Agent(
        role="Research Retriever",
        goal="Retrieve relevant passages from research papers",
        backstory="You are an expert at finding relevant information in research papers",
        action=retrieval_wrapper,
        verbose=True
    )

    generator = Agent(
        role="Research Analyst", 
        goal="Generate comprehensive answers based on retrieved passages",
        backstory="You are an expert research analyst who provides detailed, citation-based answers",
        action=generation_wrapper,
        verbose=True
    )

    retrieval_task = Task(
        description="Retrieve relevant passages from the research paper for the user's question",
        agent=retriever,
        expected_output="Relevant passages from the research paper that can answer the user's question"
    )

    generation_task = Task(
        description="Generate a comprehensive answer with citations based on the retrieved passages from the research paper",
        agent=generator,
        expected_output="A detailed answer with numbered citations based on the research paper content",
        context=[retrieval_task]
    )

    crew = Crew(
        agents=[retriever, generator],
        tasks=[retrieval_task, generation_task],
        verbose=True
    )

    return crew