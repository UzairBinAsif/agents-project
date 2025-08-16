from setup_config import model
from agents import Agent

job_agent = Agent(
    name='Job Agent',
    instructions=(
        "You suggest real-world job roles based on the user's skills or chosen field. If the field is 'web development', suggest jobs like Frontend Developer, Backend Developer, etc. Keep your response brief and specific."
    ),
    tools=[],
    model=model
)
