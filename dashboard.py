import streamlit as st
import sys
import os
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
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Job Listings",
    "📄 Resume Upload",
    "✉️ Cover Letters",
    "📊 Application Tracker"
])

# Tab 1 - Job Listings
with tab1:
    st.header("🔍 Job Listings")
    if search_btn:
        with st.spinner("Searching real jobs..."):
            jobs = search_jobs(job_role, location)
            if jobs:
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
        st.markdown("**Extracted Skills:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Programming", "Python, SQL")
        with col2:
            st.metric("AI/ML", "LangChain, CrewAI")
        with col3:
            st.metric("Experience", "2 Years")

# Tab 3 - Cover Letters
with tab3:
    st.header("✉️ AI Generated Cover Letters")
    st.info("Cover letters will appear here after job search!")

    sample_cover = """Dear Hiring Manager at IBM,

I am excited to apply for the Python Developer position at IBM. 
With 2 years of experience in Python development and strong skills 
in AI, Machine Learning, LangChain, and CrewAI, I am confident 
I can contribute greatly to your team.

Sincerely,
John Doe"""

    st.text_area("Sample Cover Letter", value=sample_cover, height=200)
    st.download_button(
        "⬇️ Download Cover Letter",
        data=sample_cover,
        file_name="cover_letter.txt",
        mime="text/plain"
    )

# Tab 4 - Application Tracker
with tab4:
    st.header("📊 Application Tracker")
    import pandas as pd

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
        if val == "Shortlisted":
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

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Applied", "5")
    col2.metric("Shortlisted", "1")
    col3.metric("Pending", "2")

st.markdown("---")
st.markdown("Built with ❤️ using Python, CrewAI, LangChain & Streamlit")