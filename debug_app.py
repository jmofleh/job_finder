"""
Debug version to diagnose import issues
"""

import streamlit as st
import sys
import subprocess

st.set_page_config(page_title="Debug App", layout="wide")

st.title("🔍 Debug Mode - Checking Dependencies")

# Show Python version
st.subheader("🐍 Python Information")
st.code(f"Python version: {sys.version}")

# Try to import jobspy
st.subheader("📦 Testing Imports")

# Method 1: Direct import
try:
    from jobspy import scrape_jobs
    st.success("✅ Method 1: 'from jobspy import scrape_jobs' SUCCESS")
    st.write(f"jobspy location: {scrape_jobs.__module__}")
except ImportError as e:
    st.error(f"❌ Method 1 failed: {e}")

# Method 2: Try different import
try:
    import jobspy
    st.success("✅ Method 2: 'import jobspy' SUCCESS")
    st.write(f"jobspy location: {jobspy.__file__}")
    if hasattr(jobspy, 'scrape_jobs'):
        st.success("✅ scrape_jobs attribute exists")
    else:
        st.warning("⚠️ scrape_jobs attribute not found")
        st.write("Available attributes:", dir(jobspy)[:20])
except ImportError as e:
    st.error(f"❌ Method 2 failed: {e}")

# Check installed packages
st.subheader("📋 Installed Packages")
try:
    result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                          capture_output=True, text=True)
    st.code(result.stdout)
except Exception as e:
    st.error(f"Error getting package list: {e}")

# Try to install if missing
st.subheader("🔧 Installation Attempt")
if st.button("Try to install python-jobspy"):
    with st.spinner("Installing..."):
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "python-jobspy", "--verbose"],
            capture_output=True, text=True
        )
        st.code(result.stdout)
        if result.stderr:
            st.error(result.stderr)
