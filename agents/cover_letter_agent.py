import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from config import GROQ_API_KEY

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

cover_letter_agent = Agent(
    role="Professional Cover Letter Writer",
    goal="Write personalized and compelling cover letters for each job application",
    backstory="""You are an expert career coach and professional writer with 
    10+ years of experience helping candidates land their dream jobs. 
    You craft cover letters that are tailored, compelling and get interviews.""",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

print("✅ Cover Letter Agent created successfully!")