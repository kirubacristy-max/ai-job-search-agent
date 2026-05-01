import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "jobs.db")

def get_driver():
    """Setup Chrome browser"""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def update_job_status(job_title, company, status):
    """Update job status in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE jobs SET status=? WHERE title=? AND company=?",
        (status, job_title, company)
    )
    conn.commit()
    conn.close()

def auto_apply_job(job_link, job_title, company, candidate_info):
    """
    Open job link in Chrome and assist with application
    """
    print(f"🚀 Opening job: {job_title} at {company}")
    driver = get_driver()

    try:
        # Open the job link
        driver.get(job_link)
        time.sleep(3)

        print(f"✅ Opened: {job_link}")
        print(f"📋 Please complete the application manually.")
        print(f"⏳ You have 5 minutes to apply...")

        # Wait for user to apply manually
        time.sleep(300)

        # Update status
        update_job_status(job_title, company, "applied")
        print(f"✅ Status updated to 'applied' for {job_title}")

    except Exception as e:
        print(f"❌ Error: {e}")
        update_job_status(job_title, company, "failed")
    finally:
        driver.quit()

def get_pending_jobs():
    """Get all jobs with 'found' status from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, company, location FROM jobs WHERE status='found' ORDER BY match_score DESC"
    )
    jobs = cursor.fetchall()
    conn.close()
    return jobs

if __name__ == "__main__":
    print("🔍 Checking pending jobs...")
    jobs = get_pending_jobs()
    if jobs:
        print(f"✅ Found {len(jobs)} jobs to apply:")
        for job in jobs:
            print(f"  {job[0]}. {job[1]} at {job[2]} — {job[3]}")
    else:
        print("❌ No pending jobs found. Search for jobs first!")