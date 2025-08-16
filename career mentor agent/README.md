# Career Mentor Agent

## Overview
A multi-agent system that guides students through career exploration by recommending paths, skill development plans, and real-world job insights.

## Agent Architecture
1. **CareerAgent**  
   - Suggests career fields based on user interests  
   - Example: "Based on your love for problem-solving, consider Data Science or Cybersecurity"  
   - Tools: `get_career_roadmap()`  
   - Handoff: → SkillAgent  

2. **SkillAgent**  
   - Generates skill-building roadmaps for chosen careers  
   - Example: "For Data Science: Learn Python → Statistics → Machine Learning"  
   - Handoff: → JobAgent  

3. **JobAgent**  
   - Provides real-world job role descriptions and salary ranges  
   - Example: "Data Scientist @ TechCo: $120K, requires Python + SQL"  

## Tools
- `get_career_roadmap(wrapper: RunContextWrapper, input: CareerRoadmapInput) -> dict`
