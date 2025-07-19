import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool
def get_career_roadmap(field: str) -> str:
    """Generate a basic career skill roadmap based on a user's chosen field."""
    roadmaps = {
        "web development": "1. HTML & CSS\n2. JavaScript\n3. Frontend Frameworks (React/Vue)\n4. Backend (Node.js, Django)\n5. Databases\n6. DevOps",
        "ai": "1. Python\n2. Math for ML (Linear Algebra, Stats)\n3. ML Basics (Scikit-learn)\n4. Deep Learning (TensorFlow, PyTorch)\n5. NLP & CV\n6. MLOps",
        "data science": "1. Python\n2. Pandas, NumPy\n3. Data Visualization\n4. Statistics\n5. ML Models\n6. SQL & Big Data",
        "cybersecurity": "1. Networking Basics\n2. Security Principles\n3. Tools (Wireshark, Nmap)\n4. Vulnerability Analysis\n5. Pen Testing\n6. Certifications"
    }
    field = field.lower()
    return roadmaps.get(field, "Skill roadmap not available for this field.")

def main():
    job_agent = Agent(
        name='Job Agent',
        instructions=(
            "You suggest real-world job roles based on the user's skills or chosen field. If the field is 'web development', suggest jobs like Frontend Developer, Backend Developer, etc. Keep your response brief and specific."
        ),
    )
    
    skill_agent = Agent(
        name='Skill Agent',
        instructions=(
            "You provide a skill-building roadmap using the `get_career_roadmap` tool. You MUST call the `get_career_roadmap` tool with the user's chosen field. summarize the output clearly, then pass the result to the Job Agent."
        ),
        handoffs=[job_agent],
        tools=[get_career_roadmap]
    )

    career_agent = Agent(
        name='Career Agent', 
        instructions=(
            """You help the user explore career fields.
            If the user mentions a specific field like 'web development', 'AI', or 'data science',
            you pass the request to the Skill Agent.
            If the user is asking about job opportunities, pass it to the Job Agent.
            Otherwise, help them pick a field of interest"""
        ),
        handoffs=[skill_agent, job_agent]
    )
    
    print("\n👋 Welcome to the Career Mentor Agent!")
    user_input = input("What career option are you curious about? (e.g., AI, web development, cybersecurity): ")
    
    result = Runner.run_sync(
        career_agent,
        user_input,
        run_config=config,
        max_turns=6
    )
    
    print('\n', result.final_output)

if __name__ == '__main__':
    main()