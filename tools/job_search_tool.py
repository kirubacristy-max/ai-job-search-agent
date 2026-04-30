import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SERP_API_KEY
import requests

def search_jobs(query, location="Chennai, India"):
    params = {
        "engine": "google_jobs",
        "q": f"{query} in {location}",
        "hl": "en",
        "gl": "in",
        "api_key": SERP_API_KEY
    }
    url = "https://serpapi.com/search"
    response = requests.get(url, params=params)
    results = response.json()
    jobs = []
    if "jobs_results" in results:
        for job in results["jobs_results"][:5]:
            # Get apply link
            apply_link = "N/A"
            related_links = job.get("related_links", [])
            if related_links:
                apply_link = related_links[0].get("link", "N/A")
            if apply_link == "N/A":
                detected_extensions = job.get("detected_extensions", {})
                apply_options = job.get("apply_options", [])
                if apply_options:
                    apply_link = apply_options[0].get("link", "N/A")

            jobs.append({
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": location,
                "description": job.get("description", "")[:300],
                "link": apply_link
            })
    return jobs

if __name__ == "__main__":
    print("✅ API Keys loaded successfully!")
    print("🔍 Searching real jobs...")
    jobs = search_jobs("Python Developer", "Chennai, India")
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']} at {job['company']}")
        print(f"   📍 {job['location']}")
        print(f"   🔗 {job['link']}")
    print("\n✅ Job Search Tool working!")
