import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent
from config import GROQ_API_KEY

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

tracking_agent = Agent(
    role="Application Tracking Specialist",
    goal="Track and manage all job applications and their current status",
    backstory="""You are an expert application tracker with experience 
    in managing job application pipelines. You keep detailed records 
    of application status, follow-ups, and interview schedules.""",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

print("✅ Tracking Agent created successfully!")