import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from config import GROQ_API_KEY

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

filter_agent = Agent(
    role="Job Matching Specialist",
    goal="Analyze and rank job listings based on candidate skills and preferences",
    backstory="""You are an AI-powered recruitment analyst with deep expertise 
    in matching candidates to the right opportunities. You evaluate job descriptions 
    and rank them by relevance, salary, growth potential and culture fit.""",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

print("✅ Filter Agent created successfully!")