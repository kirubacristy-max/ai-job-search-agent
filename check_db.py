import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "jobs.db")

def check_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 60)
    print("📊 AI JOB SEARCH AGENT — DATABASE REPORT")
    print("=" * 60)

    # Total jobs
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total = cursor.fetchone()[0]
    print(f"\n✅ Total Jobs Found: {total}")

    # Jobs by location
    print("\n📍 Jobs by Location:")
    cursor.execute("SELECT location, COUNT(*) FROM jobs GROUP BY location")
    for row in cursor.fetchall():
        print(f"   {row[0]} → {row[1]} jobs")

    # Jobs by status
    print("\n🔖 Jobs by Status:")
    cursor.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status")
    for row in cursor.fetchall():
        print(f"   {row[0]} → {row[1]} jobs")

    # All jobs
    print("\n💼 All Saved Jobs:")
    print("-" * 60)
    cursor.execute("SELECT id, title, company, location, match_score, status, created_at FROM jobs ORDER BY id DESC")
    jobs = cursor.fetchall()
    for job in jobs:
        print(f"\n  🆔 ID     : {job[0]}")
        print(f"  📌 Title  : {job[1]}")
        print(f"  🏢 Company: {job[2]}")
        print(f"  📍 Location: {job[3]}")
        print(f"  ⭐ Score  : {job[4]}/10")
        print(f"  🔖 Status : {job[5]}")
        print(f"  📅 Saved  : {job[6]}")

    # Applications
    cursor.execute("SELECT COUNT(*) FROM applications")
    total_apps = cursor.fetchone()[0]
    print(f"\n\n📨 Total Applications: {total_apps}")

    if total_apps > 0:
        print("\n📋 Application Details:")
        print("-" * 60)
        cursor.execute("""
            SELECT a.id, j.title, j.company, a.status, a.applied_at 
            FROM applications a 
            JOIN jobs j ON a.job_id = j.id
            ORDER BY a.id DESC
        """)
        for app in cursor.fetchall():
            print(f"\n  🆔 ID      : {app[0]}")
            print(f"  📌 Job     : {app[1]}")
            print(f"  🏢 Company : {app[2]}")
            print(f"  🔖 Status  : {app[3]}")
            print(f"  📅 Applied : {app[4]}")

    print("\n" + "=" * 60)
    print("✅ Database check complete!")
    print("=" * 60)

    conn.close()

if __name__ == "__main__":
    check_database()