"""
Simplified Job Finder - With better error handling
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys

st.set_page_config(page_title="Job Finder", layout="wide")

st.title("🔍 Job Finder for Germany")
st.write(f"Python version: {sys.version}")

# Try importing jobspy with detailed error handling
try:
    from jobspy import scrape_jobs
    st.success("✅ jobspy imported successfully!")
    jobspy_available = True
except ImportError as e:
    st.error(f"❌ Failed to import jobspy: {e}")
    st.info("Checking installed packages...")
    
    # Show installed packages
    import subprocess
    result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                          capture_output=True, text=True)
    st.code(result.stdout)
    
    jobspy_available = False

if jobspy_available:
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
