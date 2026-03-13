"""
Job Finder with auto-install
"""

import streamlit as st
import sys
import subprocess

st.set_page_config(page_title="Job Finder", layout="wide")

st.title("🔍 Job Finder for Germany")

# Function to install packages
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import, install if missing
try:
    from jobspy import scrape_jobs
    st.success("✅ jobspy already installed")
except ImportError:
    st.warning("⚠️ jobspy not found. Installing now...")
    with st.spinner("Installing python-jobspy..."):
        try:
            install_package("python-jobspy")
            from jobspy import scrape_jobs
            st.success("✅ jobspy installed successfully!")
        except Exception as e:
            st.error(f"❌ Installation failed: {e}")
            st.stop()

# Rest of your app continues here...
import pandas as pd
from datetime import datetime

st.sidebar.header("Search Parameters")

search_term = st.sidebar.text_input(
    "Job Title",
    value="Data Analyst OR Data Scientist"
)

location = st.sidebar.selectbox(
    "Location",
    ["Germany", "Berlin", "Munich", "Hamburg", "Remote"]
)

if st.sidebar.button("🔍 Search Jobs"):
    with st.spinner("Searching..."):
        try:
            jobs = scrape_jobs(
                site_name=["indeed", "glassdoor"],
                search_term=search_term,
                location=location,
                results_wanted=20,
                hours_old=72,
                country_indeed='Germany'
            )
            
            if jobs is not None and len(jobs) > 0:
                st.success(f"Found {len(jobs)} jobs!")
                st.dataframe(jobs[['title', 'company', 'location']])
                
                # Download button
                csv = jobs.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    f"jobs_{datetime.now().strftime('%Y%m%d')}.csv"
                )
            else:
                st.warning("No jobs found")
                
        except Exception as e:
            st.error(f"Search error: {e}")
