import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from config import GROQ_API_KEY

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

interview_prep_agent = Agent(
    role="Interview Coach",
    goal="Generate likely interview questions and model answers based on job descriptions",
    backstory="""You are an expert interview coach with 10+ years of experience 
    helping candidates crack interviews at top tech companies. You analyze job 
    descriptions and generate the most relevant technical and behavioral questions.""",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

print("✅ Interview Prep Agent created successfully!")