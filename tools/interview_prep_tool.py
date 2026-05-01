import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GROQ_API_KEY
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

def generate_interview_questions(job_title, company, skills, experience):
    prompt = f"""You are an expert interview coach.

Generate 10 interview questions with model answers for this candidate:

Job Title: {job_title}
Company: {company}
Candidate Skills: {skills}
Experience: {experience}

Return EXACTLY this format for each question:

Q1: [Technical or behavioral question]
A1: [A strong, concise model answer in 3-4 sentences]

Q2: ...
A2: ...

Cover:
- 4 Technical questions (specific to the job role)
- 3 Behavioral questions (STAR format hints)
- 2 Project-based questions (based on skills)
- 1 Salary/career goals question

Keep answers professional and tailored to the role."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )
    return response.choices[0].message.content


def parse_qa_pairs(raw_text):
    """Parse Q&A text into a list of dicts"""
    import re
    pairs = []
    questions = re.findall(r'Q\d+:\s*(.+?)(?=A\d+:)', raw_text, re.DOTALL)
    answers = re.findall(r'A\d+:\s*(.+?)(?=Q\d+:|$)', raw_text, re.DOTALL)
    for q, a in zip(questions, answers):
        pairs.append({
            "question": q.strip(),
            "answer": a.strip()
        })
    return pairs