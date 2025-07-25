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
- `get_career_roadmap(field: str)`  
  Returns:  
  ```json
    {
        "web development": "1. HTML & CSS\n2. JavaScript\n3. Frontend Frameworks (React/Vue)\n4. Backend (Node.js, Django)\n5. Databases\n6. DevOps",
        "ai": "1. Python\n2. Math for ML (Linear Algebra, Stats)\n3. ML Basics (Scikit-learn)\n4. Deep Learning (TensorFlow, PyTorch)\n5. NLP & CV\n6. MLOps",
        "data science": "1. Python\n2. Pandas, NumPy\n3. Data Visualization\n4. Statistics\n5. ML Models\n6. SQL & Big Data",
        "cybersecurity": "1. Networking Basics\n2. Security Principles\n3. Tools (Wireshark, Nmap)\n4. Vulnerability Analysis\n5. Pen Testing\n6. Certifications"
    }