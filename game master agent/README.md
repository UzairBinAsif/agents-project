# Game Master Agent  

## Overview  
A fantasy adventure game powered by AI agents that dynamically respond to player choices.  

## Agent Architecture  
1. **NarratorAgent**  
   - Drives story progression  
   - Example: "You enter a dark cave. A faint glow comes from the left."  
   - Tools: `generate_event()`  
   - Handoff: → MonsterAgent (if combat) or ItemAgent (if discovery)  

2. **MonsterAgent**  
   - Manages combat encounters  
   - Tools: `roll_dice()` for attack outcomes  
   - Example: "Goblin attacks! Roll STR 12+ to dodge"  

3. **ItemAgent**  
   - Handles inventory/rewards  
   - Example: "You found a +2 Sword! Added to inventory."  

## Tools  
- `roll_dice(sides: int = 20)`  
  Returns random number for game mechanics  
- `generate_event()`  
  Creates dynamic story branches  