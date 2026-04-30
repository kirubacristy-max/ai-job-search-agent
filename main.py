import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crewai import Crew, Task
from agents.search_agent import search_agent
from agents.filter_agent import filter_agent
from agents.cover_letter_agent import cover_letter_agent
from agents.resume_agent import resume_agent
from agents.tracking_agent import tracking_agent
from tools.database_tool import init_db

# Initialize Database
init_db()

print("🚀 Starting AI Job Search Agent...")

# Define Tasks
search_task = Task(
    description="""Search for Python Developer jobs in Bangalore, India. 
    Find at least 5 relevant job listings with company name, 
    job title, and key requirements.""",
    agent=search_agent,
    expected_output="A list of 5 Python Developer job listings with details"
)

resume_task = Task(
    description="""Parse this candidate profile and extract key skills:
    - Name: John Doe
    - Skills: Python, AI, Machine Learning, LangChain, CrewAI
    - Experience: 2 years
    - Education: B.Tech Computer Science""",
    agent=resume_agent,
    expected_output="Structured resume data with skills and experience"
)

filter_task = Task(
    description="""Analyze the job listings and rank them from most 
    to least relevant for a Python + AI + ML candidate.""",
    agent=filter_agent,
    expected_output="Top 3 ranked jobs with match score and reasoning"
)

cover_letter_task = Task(
    description="""Write a professional cover letter for the top ranked job. 
    Candidate is a Python developer skilled in AI, LangChain and CrewAI.""",
    agent=cover_letter_agent,
    expected_output="A complete personalized cover letter"
)

tracking_task = Task(
    description="""Create an application tracking summary for all jobs found. 
    List each job with status as 'Applied', 'Pending' or 'Shortlisted'.""",
    agent=tracking_agent,
    expected_output="Application tracking table with job status"
)

# Create Crew
crew = Crew(
    agents=[search_agent, resume_agent, filter_agent, cover_letter_agent, tracking_agent],
    tasks=[search_task, resume_task, filter_task, cover_letter_task, tracking_task],
    verbose=True
)

# Run
result = crew.kickoff()

print("\n✅ Job Search Complete!")
print("\n📄 Final Output:")
print(result)