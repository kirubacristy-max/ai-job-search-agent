import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from config import GROQ_API_KEY

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

search_agent = Agent(
    role="Job Search Specialist",
    goal="Find the most relevant job listings based on the user's skills and preferences",
    backstory="""You are an expert job market researcher with years of experience 
    finding the perfect job matches. You know how to search effectively and 
    identify the best opportunities.""",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

print("✅ Search Agent created successfully!")