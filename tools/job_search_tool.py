import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SERP_API_KEY
import requests

def search_jobs(query, location="Bangalore, India"):
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": SERP_API_KEY
    }

    url = "https://serpapi.com/search"
    response = requests.get(url, params=params)
    results = response.json()

    jobs = []
    if "jobs_results" in results:
        for job in results["jobs_results"][:5]:
            jobs.append({
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("location"),
                "description": job.get("description", "")[:300]
            })
    return jobs

if __name__ == "__main__":
    print("✅ API Keys loaded successfully!")
    print("🔍 Searching real jobs...")
    jobs = search_jobs("Python Developer")
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']} at {job['company']}")
        print(f"   📍 {job['location']}")
    print("\n✅ Job Search Tool working!")