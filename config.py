import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found!")

if not SERP_API_KEY:
    raise ValueError("SERP_API_KEY not found!")

print("✅ API Keys loaded successfully!")