#
# pip install composio crewai crewai-tools[mcp] python-dotenv
#
#
from crewai import Agent, Task, Crew, LLM
from crewai_tools import MCPServerAdapter
from composio import Composio
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
COMPOSIO_USER_ID = os.getenv("COMPOSIO_USER_ID")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in the environment.")
if not COMPOSIO_API_KEY:
    raise ValueError("COMPOSIO_API_KEY is not set in the environment.")
if not COMPOSIO_USER_ID:
    raise ValueError("COMPOSIO_USER_ID is not set in the environment.")

# Initialize Composio and create a session
composio = Composio(api_key=COMPOSIO_API_KEY)
session = composio.create(
    user_id=COMPOSIO_USER_ID,
    toolkits=["gmail"],
)
url = session.mcp.url

# Configure LLM
llm = LLM(
    model="gpt-5",
    api_key=os.getenv("OPENAI_API_KEY"),
)

server_params = {
    "url": url,
    "transport": "streamable-http",
    "headers": {"x-api-key": COMPOSIO_API_KEY},
}

with MCPServerAdapter(server_params) as tools:
    agent = Agent(
        role="Search Assistant",
        goal="Help users with internet searches",
        backstory="You are an expert assistant with access to Composio Search tools.",
        tools=tools,
        llm=llm,
        verbose=False,
        max_iter=10,
    )

    print("Chat started! Type 'exit' or 'quit' to end.\n")

    conversation_context = ""

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        conversation_context += f"\nUser: {user_input}\n"
        print("\nAgent is thinking...\n")

        task = Task(
            description=(
                f"Conversation history:\n{conversation_context}\n\n"
                f"Current request: {user_input}"
            ),
            expected_output="A helpful response addressing the user's request",
            agent=agent,
        )

        crew = Crew(agents=[agent], tasks=[task], verbose=False)
        result = crew.kickoff()
        response = str(result)

        conversation_context += f"Agent: {response}\n"
        print(f"Agent: {response}\n")