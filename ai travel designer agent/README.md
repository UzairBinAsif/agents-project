# AI Travel Designer Agent  

## Overview  
Coordinates specialized agents to plan complete travel experiences from destination selection to activity planning.  

## Agent Architecture  
1. **DestinationAgent**  
   - Recommends locations based on mood/interests  
   - Example: "For relaxation: Bali | For adventure: Patagonia"  
   - Handoff: → BookingAgent  

2. **BookingAgent**  
   - Simulates flight/hotel bookings using mock data  
   - Tools:  
     - `get_flights(destination)`  
     - `suggest_hotels(budget)`  
   - Handoff: → ExploreAgent  

3. **ExploreAgent**  
   - Suggests attractions and local cuisine  
   - Example: "In Bali: Visit Uluwatu Temple → Try Babi Guling"  

## Tools  
- `get_flights(destination: str)`  
  Returns mock flight data with prices/timings  
- `suggest_hotels(destination: str)`  
  Returns filtered hotel options  