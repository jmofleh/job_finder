


import streamlit as st
import requests
import urllib3

# This tells Python to ignore SSL warnings if your network is blocking the connection
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
SERP_API_KEY =st.secrets["SERP_API_KEY"]

def search_jobs(title, city):
    url = "https://serpapi.com/search.json"
    
    params = {
        "engine": "google_jobs",
        "q": f"{title} jobs in {city}",
        "gl": "de",
        "api_key": SERP_API_KEY
    }

    try:
        # 'verify=False' helps bypass local network/SSL blocks
        response = requests.get(url, params=params, verify=False)
        
        # DEBUG: Look at your PyCharm terminal. If you see 200, it worked!
        print(f"DEBUG: Response Code: {response.status_code}")
        
        data = response.json()
        if "error" in data:
            st.error(f"API Error: {data['error']}")
            return []
        return data.get("jobs_results", [])
    except Exception as e:
        st.error(f"Your computer blocked the connection: {e}")
        return []

# --- UI ---
st.title("📊 Germany Data Analyst Search")

job_input = st.text_input("Job Title", value="Data Analyst")
city_input = st.text_input("City", value="Berlin")

if st.button("Search"):
    results = search_jobs(job_input, city_input)
    if results:
        st.success(f"Found {len(results)} jobs!")
        for job in results:
            st.write(f"**{job.get('title')}** at {job.get('company_name')}")
    else:
        st.warning("If the dashboard still says 0, try turning off your VPN or Firewall briefly.")
