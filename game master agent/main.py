import random, os
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
def roll_dice(sides: int = 20) -> int:
    """Rolls dice for game progression"""
    return random.randint(1, sides)

@function_tool
def generate_event():
    """Generates random game events (combat, treasure, or story)"""
    events = [
        "A ferocious dragon blocks your path!",
        "You discover a chest of glowing artifacts",
        "The path forks mysteriously ahead",
        "An ancient inscription reveals a clue"
    ]
    return random.choice(events)

def main():
    item_agent = Agent(
        name='ItemAgent',
        instructions="You manage the player's inventory and rewards. Describe items found and manage equipment.",
        model=model
    )
    
    monster_agent = Agent(
        name='MonsterAgent',
        instructions="You manage combat encounters. Describe monsters and resolve battle outcomes using dice rolls.",
        tools=[roll_dice],
        handoffs=[item_agent],
        model=model
    )

    narrator_agent = Agent(
        name='NarratorAgent', 
        instructions="""You narrate a fantasy adventure game. Set the scene, describe environments, 
                        and progress the story based on player choices. Use generate_event for surprises.
                        Hand off to MonsterAgent for combat or ItemAgent for treasure.""",
        tools=[generate_event],
        handoffs=[monster_agent],
        model=model
    )
    
    print("\n👋 Welcome to the Fantasy Adventure!")
    print("Type your actions (e.g., 'explore the cave', 'attack the monster', 'open chest')")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == 'quit':
            break
        
        result = Runner.run_sync(
            narrator_agent if 'combat' not in user_input.lower() else monster_agent,
            user_input,
            run_config=config,
            max_turns=10
        )
        
        print('\n', result.final_output, sep='')

if __name__ == '__main__':
    main()