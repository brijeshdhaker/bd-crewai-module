from crewai import Crew
from pdf_search_crew.crew import Router_Agent, router_task

#

test_rag_crew = Crew(
    agents=[Router_Agent],
    tasks=[router_task],
    verbose=True,
 
)
inputs ={"question":"Does the ESOP supplement the salary of an employee?"}
result = test_rag_crew.kickoff(inputs=inputs)

