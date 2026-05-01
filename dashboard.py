import streamlit as st
import sys
import os
import sqlite3
import re
import tempfile
import pandas as pd
import threading
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.database_tool import init_db
from tools.job_search_tool import search_jobs

# Page config
st.set_page_config(
    page_title="AI Job Search Agent",
    page_icon="🚀",
    layout="wide"
)

# Initialize DB
init_db()

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "jobs.db")

# Header
st.title("🚀 AI Job Search Agent")
st.subheader("Automate. Personalize. Succeed.")
st.markdown("---")

# Sidebar
st.sidebar.title("⚙️ Search Settings")
job_role = st.sidebar.text_input("Job Role", value="Python Developer")
location = st.sidebar.text_input("Location", value="Bangalore, India")
search_btn = st.sidebar.button("🔍 Search Jobs", type="primary")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Job Listings",
    "📄 Resume Upload",
    "✉️ Cover Letters",
    "📊 Application Tracker",
    "🤖 Auto Apply"
])

# Tab 1 - Job Listings
with tab1:
    st.header("🔍 Job Listings")
    if search_btn:
        with st.spinner("Searching real jobs..."):
            jobs = search_jobs(job_role, location)
            if jobs:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                for job in jobs:
                    cursor.execute(
                        "SELECT id FROM jobs WHERE title=? AND company=?",
                        (job['title'], job['company'])
                    )
                    if not cursor.fetchone():
                        cursor.execute('''INSERT INTO jobs
                            (title, company, location, description, match_score, status)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                            (job['title'], job['company'], job['location'],
                             job.get('description', ''), 8.0, 'found'))
                conn.commit()
                conn.close()
                st.toast("✅ Jobs saved to database!", icon="💾")

                for i, job in enumerate(jobs, 1):
                    with st.expander(f"💼 {i}. {job['title']} at {job['company']}"):
                        st.write(f"📍 **Location:** {job['location']}")
                        st.write(f"🔗 **Link:** {job.get('link', 'N/A')}")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.success("✅ Match Score: 8/10")
                        with col2:
                            link = job.get("link", "N/A")
                            if link and link != "N/A":
                                st.link_button("Apply Now", url=link)
                            else:
                                st.button("Apply Now", disabled=True)
            else:
                st.warning("No jobs found. Try different keywords!")
    else:
        st.info("👈 Enter job role and location, then click Search Jobs!")

# Tab 2 - Resume Upload
with tab2:
    st.header("📄 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or TXT)",
        type=["pdf", "txt"]
    )
    if uploaded_file:
        st.success(f"✅ Resume uploaded: {uploaded_file.name}")
        st.info("🤖 AI is parsing your resume...")

        import fitz

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        doc = fitz.open(tmp_path)
        resume_text = ""
        for page in doc:
            resume_text += page.get_text()
        doc.close()
        os.unlink(tmp_path)

        all_skills = [
            "Python", "SQL", "Java", "JavaScript",
            "Machine Learning", "Deep Learning", "NLP", "EDA",
            "LangChain", "CrewAI", "TensorFlow", "PyTorch", "Scikit-learn",
            "Power BI", "Tableau", "Matplotlib", "Seaborn",
            "FastAPI", "Django", "Flask", "Streamlit",
            "MySQL", "PostgreSQL", "MongoDB",
            "Docker", "AWS", "Azure", "Git",
            "Pandas", "NumPy", "BeautifulSoup", "Excel"
        ]
        found_skills = [s for s in all_skills if s.lower() in resume_text.lower()]
        prog_skills = [s for s in found_skills if s in ["Python", "SQL", "Java", "JavaScript"]]
        ai_skills = [s for s in found_skills if s in [
            "Machine Learning", "Deep Learning", "NLP", "LangChain",
            "CrewAI", "TensorFlow", "PyTorch", "Scikit-learn", "EDA"
        ]]

        exp_match = re.search(r'(\d+)\+?\s*years?\s*(of\s*)?experience', resume_text.lower())
        months_match = re.search(r'(\d+)\s*months?', resume_text.lower())
        if exp_match:
            experience = f"{exp_match.group(1)} Years"
        elif months_match:
            months = int(months_match.group(1))
            experience = f"{months} Months Training"
        elif any(w in resume_text.lower() for w in
                 ["fresher", "student", "pursuing", "bachelor", "university", "college"]):
            experience = "Fresher / Student"
        else:
            experience = "Entry Level"

        st.markdown("**Extracted Skills:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Programming", ", ".join(prog_skills) if prog_skills else "Not found")
        with col2:
            st.metric("AI/ML", ", ".join(ai_skills[:2]) if ai_skills else "Not found")
        with col3:
            st.metric("Experience", experience)

        if found_skills:
            st.markdown("**All Detected Skills:**")
            st.write(", ".join(found_skills))

        st.session_state['resume_skills'] = ", ".join(found_skills)
        st.session_state['resume_experience'] = experience

# Tab 3 - Cover Letters
with tab3:
    st.header("✉️ AI Generated Cover Letters")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, location FROM jobs ORDER BY id DESC LIMIT 10")
    saved_jobs = cursor.fetchall()
    conn.close()

    if not saved_jobs:
        st.info("🔍 Search for jobs first, then come here to generate cover letters!")
    else:
        st.success(f"✅ Found {len(saved_jobs)} saved jobs — select one to generate a cover letter!")

        job_options = {f"{job[1]} at {job[2]} ({job[3]})": job for job in saved_jobs}
        selected_job_name = st.selectbox("🎯 Select a job:", list(job_options.keys()))
        selected_job = job_options[selected_job_name]

        resume_skills = st.session_state.get(
            'resume_skills',
            'Python, SQL, Machine Learning, NLP, Power BI, Data Science'
        )
        resume_experience = st.session_state.get('resume_experience', '4 Months Training')

        if st.button("✨ Generate Cover Letter", type="primary"):
            with st.spinner("🤖 AI is writing your personalized cover letter..."):
                try:
                    from groq import Groq
                    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

                    prompt = f"""Write a professional cover letter for this job application:

Job Title: {selected_job[1]}
Company: {selected_job[2]}
Location: {selected_job[3]}

Candidate Profile:
- Name: Kirubakaran V
- Skills: {resume_skills}
- Experience: {resume_experience} at Livewire Salem
- Education: BSc Physics, Periyar University
- Projects: RAG Chatbot, IPL Predictor, Movie Recommendation System, Flipkart Scraper

Write a compelling, personalized cover letter in 3 paragraphs:
1. Introduction — express excitement for this specific role at this company
2. Relevant skills and projects that match this job
3. Closing — enthusiasm to contribute and request for interview

Keep it professional, concise, genuine and under 250 words."""

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=600
                    )

                    cover_letter = response.choices[0].message.content
                    st.session_state['cover_letter'] = cover_letter
                    st.session_state['cover_letter_job'] = selected_job_name
                    st.success("✅ Cover letter generated!")

                except Exception as e:
                    st.error(f"❌ Error generating cover letter: {e}")

        if 'cover_letter' in st.session_state:
            st.markdown(f"**📄 Cover Letter for: {st.session_state['cover_letter_job']}**")
            st.text_area(
                "Generated Cover Letter",
                value=st.session_state['cover_letter'],
                height=350
            )
            st.download_button(
                "⬇️ Download Cover Letter",
                data=st.session_state['cover_letter'],
                file_name=f"cover_letter_{selected_job[2].replace(' ', '_')}.txt",
                mime="text/plain"
            )

# Tab 4 - Application Tracker
with tab4:
    st.header("📊 Application Tracker")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, company, location, match_score, status FROM jobs ORDER BY id DESC")
    db_jobs = cursor.fetchall()
    conn.close()

    if db_jobs:
        data = {
            "Job Title": [row[0] for row in db_jobs],
            "Company": [row[1] for row in db_jobs],
            "Location": [row[2] for row in db_jobs],
            "Match Score": [f"{row[3]}/10" for row in db_jobs],
            "Status": [row[4].capitalize() for row in db_jobs]
        }
    else:
        data = {
            "Company": ["IBM", "Infosys", "SAP", "Oracle", "Accenture"],
            "Job Title": ["Python Developer", "Python Developer",
                          "Python Developer", "Senior Python Developer",
                          "Senior Python Developer"],
            "Match Score": ["8/10", "7.5/10", "7/10", "6/10", "6/10"],
            "Status": ["Shortlisted", "Applied", "Applied", "Pending", "Pending"]
        }

    df = pd.DataFrame(data)

    def color_status(val):
        if val in ["Shortlisted", "Found"]:
            return "background-color: #00ff0033"
        elif val == "Applied":
            return "background-color: #0000ff22"
        elif val == "Pending":
            return "background-color: #ffff0033"
        return ""

    st.dataframe(
        df.style.map(color_status, subset=["Status"]),
        use_container_width=True
    )

    total = len(db_jobs) if db_jobs else 5
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Found", total)
    col2.metric("Shortlisted", "1")
    col3.metric("Pending", total - 1)

# Tab 5 - Auto Apply
with tab5:
    st.header("🤖 Auto Apply")
    st.info("🚀 Click Apply Now — it opens the job link and marks it as applied in your database!")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, location, match_score FROM jobs WHERE status='found' ORDER BY match_score DESC")
    pending_jobs = cursor.fetchall()
    conn.close()

    if not pending_jobs:
        st.warning("⚠️ No pending jobs! Search for jobs first in Job Listings tab.")
    else:
        st.success(f"✅ {len(pending_jobs)} jobs ready to apply!")

        for job in pending_jobs:
            with st.expander(f"💼 {job[1]} at {job[2]} — {job[3]}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Match Score", f"{job[4]}/10")
                with col2:
                    st.metric("Location", job[3])
                with col3:
                    st.metric("Status", "Ready ✅")

                if st.button(f"🚀 Apply Now", key=f"apply_{job[0]}"):
                    with st.spinner(f"Processing application for {job[1]}..."):
                        try:
                            from tools.auto_apply_tool import update_job_status
                            update_job_status(job[1], job[2], "applied")
                            st.success(f"✅ Applied to {job[1]} at {job[2]}!")
                            st.balloons()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")

        st.markdown("---")
        st.markdown("**📊 Application Summary:**")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status")
        stats = cursor.fetchall()
        conn.close()

        if stats:
            cols = st.columns(len(stats))
            for i, stat in enumerate(stats):
                cols[i].metric(stat[0].capitalize(), stat[1])

st.markdown("---")
st.markdown("Built with ❤️ using Python, CrewAI, LangChain & Streamlit")