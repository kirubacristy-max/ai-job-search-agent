import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from config import GROQ_API_KEY

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

apply_agent = Agent(
    role="Job Application Specialist",
    goal="Help candidates apply to jobs efficiently and track application status",
    backstory="""You are an expert job application assistant with years of experience 
    helping candidates navigate job portals, fill applications correctly, 
    and track their application status professionally.""",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

print("✅ Apply Agent created successfully!")