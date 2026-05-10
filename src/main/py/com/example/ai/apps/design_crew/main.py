from datetime import datetime
from com.example.ai.apps.design_crew.design_development import DesignDevelopment


def trigger():
    """
    Run the crew.
    """
    run_date = datetime.now().strftime('%Y-%m-%d')
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f" DesignDevelopment Crew triggered on {run_date} with execution id {run_id}")
    inputs = {
        'topic': 'Microservice Design',
        'run_date': run_date,
        'run_id': run_id
    }
    crew_response = DesignDevelopment().crew().kickoff(inputs=inputs)
    print(crew_response)

# Example usage
if __name__ == "__main__":
    trigger()