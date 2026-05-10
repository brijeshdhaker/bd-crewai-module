import warnings
from com.example.ai.apps.rag_crew.tool_rag_crew import ToolRagCrew
from com.example.ai.apps.rag_crew.pdf_knowledge_crew import PDFKnowledgeCrew
from com.example.ai.apps.rag_crew.faiss_rag_crew import FAISSRagCrew
from dotenv import load_dotenv
from datetime import datetime
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def getRunDates():
    run_date = datetime.now().strftime('%Y-%m-%d')
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    return (run_date, run_id)


def runToolRagCrew(topic='All recipes with rice', pdf_path='knowledge/pdfs/Easy_recipes.pdf'):
    """
    Run the crew.
    """
    load_dotenv()
    run_dt = getRunDates()
    inputs = {
        "topic": topic,
        "run_date": run_dt[0],
        "run_id": run_dt[1]
    }
    try:
        print(f" ToolRagCrew Crew triggered on {run_dt[0]} with execution id {run_dt[1]}")
        output=ToolRagCrew(pdf_path).crew().kickoff(inputs=inputs)
        print(output.token_usage)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def runPDFKnowledgeCrew(topic='All recipes with rice',pdf_path='pdfs/Easy_recipes.pdf'):
    """
    Run the crew.
    """
    load_dotenv()
    run_dt = getRunDates()
    inputs = {
        "topic": topic,
        "run_date": run_dt[0],
        "run_id": run_dt[1]
    }

    try:
        output=PDFKnowledgeCrew(pdf_paths=[pdf_path]).crew().kickoff(inputs=inputs)
        print(output.token_usage)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def runFAISSRagCrew(topic='All recipes with rice ?', pdf_path='knowledge/pdfs/Easy_recipes.pdf'):
    run_dt = getRunDates()
    inputs = {
        "topic": topic,
        "run_date": run_dt[0],
        "run_id": run_dt[1]
    }
    output=FAISSRagCrew(pdf_path=pdf_path).crew().kickoff(inputs=inputs)
    print(output.token_usage)



def main():
    load_dotenv()
    #runFAISSRagCrew(topic='Recipes where rice is the main ingredient')
    runFAISSRagCrew()
    #runToolRagCrew(topic='Recipes where rice is the main ingredient')
    #runToolRagCrew()
    #runPDFKnowledgeCrew(topic='Recipes where rice is the main ingredient')
    #runPDFKnowledgeCrew()

if __name__ == "__main__":
    main()
