import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SERP_API_KEY
import requests
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "jobs.db")

def save_job_to_db(job, match_score=7.0):
    """Save a job to the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Check if job already exists
        cursor.execute("SELECT id FROM jobs WHERE title=? AND company=?",
                      (job['title'], job['company']))
        existing = cursor.fetchone()
        if not existing:
            cursor.execute('''INSERT INTO jobs 
                (title, company, location, description, match_score, status)
                VALUES (?, ?, ?, ?, ?, ?)''',
                (job['title'], job['company'], job['location'],
                 job['description'], match_score, 'found'))
            conn.commit()
            print(f"✅ Saved: {job['title']} at {job['company']}")
        conn.close()
    except Exception as e:
        print(f"❌ DB Error: {e}")

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
            apply_link = "N/A"
            related_links = job.get("related_links", [])
            if related_links:
                apply_link = related_links[0].get("link", "N/A")
            if apply_link == "N/A":
                apply_options = job.get("apply_options", [])
                if apply_options:
                    apply_link = apply_options[0].get("link", "N/A")
            job_data = {
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": location,
                "description": job.get("description", "")[:300],
                "link": apply_link
            }
            jobs.append(job_data)
            # ✅ Auto-save every job to database!
            save_job_to_db(job_data)
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
    # Show database contents
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, location, status FROM jobs")
    rows = cursor.fetchall()
    conn.close()
    print(f"\n📊 Database now has {len(rows)} jobs:")
    for row in rows:
        print(f"  {row[0]}. {row[1]} at {row[2]} — {row[4]}")