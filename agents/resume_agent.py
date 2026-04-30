import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from config import GROQ_API_KEY

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

resume_agent = Agent(
    role="Resume Parser and Analyzer",
    goal="Extract and analyze key information from resumes including skills, experience, and education",
    backstory="""You are an expert HR analyst with years of experience 
    reading and analyzing resumes. You can quickly identify key skills, 
    work experience, education, and suggest improvements.""",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

print("✅ Resume Agent created successfully!")