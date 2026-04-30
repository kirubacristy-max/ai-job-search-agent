import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "jobs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        description TEXT,
        match_score REAL,
        status TEXT DEFAULT 'found',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER,
        cover_letter TEXT,
        status TEXT DEFAULT 'pending',
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    )''')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()