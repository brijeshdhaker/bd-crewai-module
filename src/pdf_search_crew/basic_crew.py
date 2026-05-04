from crewai import Crew, Agent, Task, Process, LLM
from langchain_openai import ChatOpenAI

def retrieval_action(question, vectorstore):
    results = vectorstore.similarity_search(question, k=5)
    return "\n\n".join([f"Passage {i+1}: {doc.page_content}" for i, doc in enumerate(results)])

def generation_action(inputs):
    if isinstance(inputs, dict):
        question = inputs.get("user", "")
        context = inputs.get("Retriever", "")
    else:
        question = "User question not found in inputs"
        context = str(inputs)
    prompt = (
        "You are an expert research analyst. You have been given a specific research paper and asked a question about it. "
        "Based on the retrieved passages from the research paper, provide a detailed answer with numbered citations. "
        "Use only the information from the provided passages to answer the question.\n\n"
        f"USER QUESTION: {question}\n\n"
        f"RELEVANT PASSAGES FROM THE RESEARCH PAPER:\n{context}\n\n"
        "INSTRUCTIONS:\n"
        "1. Answer the question based ONLY on the provided passages from the research paper\n"
        "2. Use numbered citations [1], [2], etc. for each key point you reference\n"
        "3. If the passages don't contain enough information to answer, say so clearly\n"
        "4. Be specific and reference the actual content from the paper\n"
        "5. Focus on the key findings, results, and conclusions mentioned in the passages\n"
        "6. If asked about key findings, look for results, outcomes, discoveries, or conclusions\n\n"
        "ANSWER:"
    )    
    
    llm = ChatOpenAI(
        model=os.environ['OPENAI_MODEL_NAME'],
        base_url='http://localhost:11434/v1/',
        api_key='ollama', # Required by SDK but ignored locally
        temperature=0.2, 
        max_tokens=1500
    )
    return llm.invoke(prompt)

def create_crew(vectorstore, status_callback=None):

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
        role="Retriever",
        goal="Retrieve relevant passages from the research paper",
        backstory="You are an expert at finding relevant information in research papers",
        action=retrieval_wrapper,
        verbose=True
    )

    generator = Agent(
        role="Generator", 
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