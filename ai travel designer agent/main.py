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
def get_flights():
    pass

@function_tool
def suggest_hotels():
    pass

def main():
    explore_agent = Agent(
        name='Explore Agent',
        instructions="You suggest different kinds of attractions and food spots to the user"
    )
    
    booking_agent = Agent(
        name='Booking Agent',
        instructions="You book the travel places for the user",
        handoffs=[explore_agent]
    )

    destination_agent = Agent(
        name='Destination Agent', 
        instructions=(
            "You help user find places to travel and then handoff to booking agent"
        ),
        handoffs=[booking_agent]
    )
    
    print("\n👋 Welcome to the Travel Designer Agent!")
    user_input = input("What country / city are you curious about?: ")
    
    result = Runner.run_sync(
        destination_agent,
        user_input,
        run_config=config,
        max_turns=6
    )
    
    print('\n', result.final_output)

if __name__ == '__main__':
    main()