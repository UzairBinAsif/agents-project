import os
from agents import function_tool, RunContextWrapper
from dotenv import load_dotenv, find_dotenv
from typing import TypedDict
from setup_config import model, config, external_client

load_dotenv(find_dotenv())

class CareerRoadmapInput(TypedDict):
    career_field: str

@function_tool
async def get_career_roadmap(wrapper: RunContextWrapper, input: CareerRoadmapInput) -> dict:
    """Generate a career skill roadmap for a specified career field."""
    try:
        prompt = (
            f"I'm interested in becoming a {input['career_field']},\n"
            "Please provide step by stepskill roadmap that included beginner, intermediate and advanced level skills,\n"
            "Format the response clearly using bullet points or numbered steps."
        )
        
        response = await external_client.chat.completions.create(
            model="gemini-2.5-flash",
            message=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"error in get_career_roadmap tool: {str(e)}"