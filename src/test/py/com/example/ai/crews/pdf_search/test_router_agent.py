from crewai import Crew
from com.example.ai.apps.pdf_search.crew import (
    Router_Agent, router_task, 
    Retriever_Agent, retriever_task, 
    Grader_agent, grader_task, 
    hallucination_grader, hallucination_task,
    answer_grader, answer_task
)

#

def test_Router_Agent() :
    test_rag_crew = Crew(
        agents=[Router_Agent],
        tasks=[router_task],
        verbose=True,
    
    )
    inputs ={"question":"Does the ESOP supplement the salary of an employee?"}
    result = test_rag_crew.kickoff(inputs=inputs)
    print(result)

def test_Retriever_Agent() :
    rag_crew = Crew(
        agents=[Router_Agent,Retriever_Agent],
        tasks=[router_task,retriever_task],
        verbose=True,
    
    )
    inputs ={"question":"Does the ESOP supplement the salary of an employee?"}
    result = rag_crew.kickoff(inputs=inputs)
    print(result)

def test_Grader_agent() :
    rag_crew = Crew(
        agents=[Router_Agent,Retriever_Agent,Grader_agent],
        tasks=[router_task,retriever_task,grader_task],
        verbose=True,
    
    )
    inputs ={"question":"Does the ESOP supplement the salary of an employee?"}
    result = rag_crew.kickoff(inputs=inputs)
    print(result)

def test_Hallucination_grader() :
    rag_crew = Crew(
        agents=[Router_Agent,Retriever_Agent,Grader_agent,hallucination_grader],
        tasks=[router_task,retriever_task,grader_task,hallucination_task],
        verbose=True,
    
    )
    inputs ={"question":"Does the ESOP supplement the salary of an employee?"}
    result = rag_crew.kickoff(inputs=inputs)
    print(result)

def test_AnswerGraderAgent() :
    rag_crew = Crew(
        agents=[Router_Agent,Retriever_Agent,Grader_agent,hallucination_grader,answer_grader],
        tasks=[router_task,retriever_task,grader_task,hallucination_task,answer_task],
        verbose=True,
    
    )
    inputs ={"question":"Does the ESOP supplement the salary of an employee?"}
    result = rag_crew.kickoff(inputs=inputs)
    print(result)

def test_AgentForNonRelative() :
    rag_crew = Crew(
        agents=[Router_Agent, Retriever_Agent, Grader_agent, hallucination_grader, answer_grader],
        tasks=[router_task, retriever_task, grader_task, hallucination_task, answer_task],
        verbose=True,
    
    )
    #
    inputs = {"question":"What is Data Distributed Parallelism?"}
    result = rag_crew.kickoff(inputs=inputs)
    print(result)

def test_AgentForRelativeQuestion() :
    rag_crew = Crew(
        agents=[Router_Agent, Retriever_Agent, Grader_agent, hallucination_grader, answer_grader],
        tasks=[router_task, retriever_task, grader_task, hallucination_task, answer_task],
        verbose=True,
    
    )
    #
    inputs = {"question":"How does exercise price determine for ESOP?"}
    result = rag_crew.kickoff(inputs=inputs)
    print(result)