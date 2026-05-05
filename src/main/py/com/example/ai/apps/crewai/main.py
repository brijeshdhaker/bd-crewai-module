#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from com.example.ai.apps.crewai.crew import BdCrewaiModule

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
from datetime import datetime

run_date = datetime.now().strftime('%Y-%m-%d')
run_id   = datetime.now().strftime("%Y%m%d_%H%M%S")
print(f" Crew triggered on {run_date} with execution id {run_id}")

def run():
    """
    Run the crew.
    """
    inputs = {
        "topic": "AI RAG Using Crewai",
        "current_year": str(datetime.now().year),
        "run_date": run_date,
        "run_id": run_id
    }

    try:
        BdCrewaiModule().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI RAG Using Crewai",
        "current_year": str(datetime.now().year),
        "run_date": run_date,
        "run_id": run_id
    }
    try:
        BdCrewaiModule().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        BdCrewaiModule().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI RAG Using Crewai",
        "current_year": str(datetime.now().year),
        "run_date": run_date,
        "run_id": run_id
    }

    try:
        BdCrewaiModule().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    from datetime import datetime

    run_date = datetime.now().strftime('%Y-%m-%d')
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f" DesignDevelopment Crew triggered on {run_date} with execution id {run_id}")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "AI RAG Using Crewai",
        "current_year": str(datetime.now().year),
        "run_date": run_date,
        "run_id": run_id
    }

    try:
        result = BdCrewaiModule().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
