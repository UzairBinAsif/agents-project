from setup_config import model
from agents import Agent, handoff
from agent_config.skill_agent import skill_agent
from agent_config.job_agent import job_agent

career_agent = Agent(
    name='Career Agent', 
    instructions=(
        """You help the user explore career fields.
        If the user mentions a specific field like 'web development', 'AI', or 'data science',
        handoff the request to the Skill Agent.
        If the user is asking about job opportunities, handoff to the Job Agent.
        Otherwise, help them pick a field of interest"""
    ),
    tools=[],
    model=model,
    handoffs=[
        handoff(agent=skill_agent),
        handoff(agent=job_agent)
    ]
)