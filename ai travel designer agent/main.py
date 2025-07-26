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
def get_flights(destination: str):
    """Get available flights to a destination"""
    flights = {
        "New York": [
            {"airline": "Delta", "price": 450, "duration": "6h 30m", "departure": "08:00"},
            {"airline": "United", "price": 420, "duration": "7h 15m", "departure": "12:30"},
        ],
        "Paris": [
            {"airline": "Air France", "price": 650, "duration": "7h 45m", "departure": "09:15"},
            {"airline": "Lufthansa", "price": 590, "duration": "8h 30m", "departure": "14:00"},
        ],
        "Tokyo": [
            {"airline": "ANA", "price": 1200, "duration": "13h 20m", "departure": "10:45"},
            {"airline": "JAL", "price": 1150, "duration": "14h 00m", "departure": "11:30"},
        ]
    }
    return flights.get(destination, [])

@function_tool
def suggest_hotels(destination: str):
    """Suggest hotels in a destination"""
    hotels = {
        "New York": [
            {"name": "The Plaza", "price": 350, "rating": 4.8, "location": "Midtown"},
            {"name": "Soho Grand Hotel", "price": 275, "rating": 4.5, "location": "Soho"},
        ],
        "Paris": [
            {"name": "Hôtel Ritz Paris", "price": 800, "rating": 4.9, "location": "Place Vendôme"},
            {"name": "Le Meurice", "price": 650, "rating": 4.7, "location": "Rue de Rivoli"},
        ],
        "Tokyo": [
            {"name": "The Ritz-Carlton", "price": 500, "rating": 4.8, "location": "Roppongi"},
            {"name": "Park Hotel Tokyo", "price": 300, "rating": 4.6, "location": "Shiodome"},
        ]
    }
    return hotels.get(destination, [])

def main():
    explore_agent = Agent(
        name='ExploreAgent',
        instructions="You suggest different kinds of attractions and food spots to the user"
    )
    
    booking_agent = Agent(
        name='BookingAgent',
        instructions="You book the travel places for the user. Use the tools available to find flights and hotels.",
        tools=[get_flights, suggest_hotels],
        handoffs=[explore_agent]
    )

    destination_agent = Agent(
        name='DestinationAgent', 
        instructions=(
            "You help user find places to travel and then handoff to booking agent. "
            "Ask questions to understand their preferences and suggest suitable destinations."
        ),
        handoffs=[booking_agent]
    )
    
    print("\n👋 Welcome to the Travel Designer Agent!")
    
    while True:
        user_input = input("What kind of trip are you looking for? (e.g., beach vacation, city tour, adventure): ")
        
        if user_input.lower() == 'quit':
            break
        
        result = Runner.run_sync(
            destination_agent,
            user_input,
            run_config=config,
            max_turns=10
        )
        
        print('\n', result.final_output)

if __name__ == '__main__':
    main()