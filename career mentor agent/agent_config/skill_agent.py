from setup_config import model
from agents import Agent, handoff
from tools.get_career_roadmap import get_career_roadmap
from agent_config.job_agent import job_agent

skill_agent = Agent(
    name='Skill Agent',
    instructions=(
        "You provide a skill-building roadmap using the `get_career_roadmap` tool. You MUST call the `get_career_roadmap` tool with the user's chosen field. summarize the output clearly, then pass the result to the Job Agent."
    ),
    tools=[get_career_roadmap],
    model=model,
    handoffs=[
        handoff(agent=job_agent)
    ]
)