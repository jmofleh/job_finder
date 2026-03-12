"""
Streamlit Job Finder App
Run with: streamlit run streamlit_job_finder.py
"""

import streamlit as st
from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime
import os
import time
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Job Finder Germany",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .job-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .metric-card {
        background-color: #e6f3ff;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def download_excel(df):
    """Create download link for Excel file"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Jobs')
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="job_search_results.xlsx">📥 Download Excel File</a>'
    return href


def search_jobs(search_term, location, sites, results_wanted, hours_old):
    """Perform job search with caching"""
    try:
        jobs = scrape_jobs(
            site_name=sites,
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            hours_old=hours_old,
            country_indeed='Germany',
            verbose=False
        )
        return jobs
    except Exception as e:
        st.error(f"Error during search: {e}")
        return None


def main():
    # Header
    st.title("🔍 Job Finder for Germany")
    st.markdown("Find **Data Analyst**, **Epidemiologist**, and **Data Scientist** positions across Germany")

    # Sidebar for search configuration
    with st.sidebar:
        st.header("⚙️ Search Configuration")

        # Job titles with multi-select
        st.subheader("Job Titles")
        job_categories = st.multiselect(
            "Select job titles",
            ["Data Analyst", "Data Scientist", "Epidemiologist",
             "Business Analyst", "Research Analyst", "BI Analyst"],
            default=["Data Analyst", "Data Scientist", "Epidemiologist"]
        )

        # Build search term with OR operator
        search_terms = []
        for job in job_categories:
            if " " in job:
                search_terms.append(f'"{job}"')
            else:
                search_terms.append(job)
        search_term = " OR ".join(search_terms)

        # Exclude terms
        st.subheader("Exclude")
        exclude_terms = st.text_input(
            "Words to exclude (comma-separated)",
            value="senior, lead, manager"
        )
        if exclude_terms:
            for term in exclude_terms.split(','):
                search_term += f" -{term.strip()}"

        # Location
        st.subheader("Location")
        location = st.selectbox(
            "Search location",
            ["Germany", "Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Remote"]
        )

        # Job sites
        st.subheader("Job Platforms")
        sites = st.multiselect(
            "Select platforms to search",
            ["indeed", "linkedin", "glassdoor"],
            default=["indeed", "glassdoor"]
        )

        # Search parameters
        st.subheader("Search Parameters")
        col1, col2 = st.columns(2)
        with col1:
            results_wanted = st.number_input("Jobs to fetch", min_value=10, max_value=200, value=50, step=10)
        with col2:
            hours_old = st.number_input("Hours old", min_value=24, max_value=168, value=72, step=24)

        # Search button
        st.markdown("---")
        search_button = st.button("🔍 SEARCH JOBS", type="primary")

        # Show search term preview
        with st.expander("Preview search query"):
            st.code(search_term)

    # Main content area
    if search_button:
        if not sites:
            st.error("Please select at least one job platform!")
            return

        with st.spinner("🔍 Searching for jobs... This may take a moment."):
            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Update progress
            status_text.text("Searching job platforms...")
            progress_bar.progress(30)

            # Perform search
            jobs = search_jobs(
                search_term=search_term,
                location=location,
                sites=sites,
                results_wanted=results_wanted,
                hours_old=hours_old
            )

            progress_bar.progress(80)
            status_text.text("Processing results...")

            if jobs is not None and len(jobs) > 0:
                # Add metadata
                jobs['date_found'] = datetime.now().strftime('%Y-%m-%d %H:%M')

                progress_bar.progress(100)
                status_text.text("Complete!")
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()

                # Success message
                st.success(f"✅ Found {len(jobs)} jobs!")

                # Display metrics in columns
                st.markdown("## 📊 Search Results Summary")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Total Jobs", len(jobs))
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    if 'site' in jobs.columns:
                        sites_count = len(jobs['site'].unique())
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Platforms", sites_count)
                        st.markdown('</div>', unsafe_allow_html=True)

                with col3:
                    if 'location' in jobs.columns:
                        locations = jobs['location'].nunique()
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Locations", locations)
                        st.markdown('</div>', unsafe_allow_html=True)

                with col4:
                    if 'company' in jobs.columns:
                        companies = jobs['company'].nunique()
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.metric("Companies", companies)
                        st.markdown('</div>', unsafe_allow_html=True)

                # Platform breakdown
                if 'site' in jobs.columns:
                    st.markdown("### 📋 Jobs by Platform")
                    site_counts = jobs['site'].value_counts()
                    st.bar_chart(site_counts)

                # Download section
                st.markdown("### 💾 Download Results")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(download_excel(jobs), unsafe_allow_html=True)
                with col2:
                    csv = jobs.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"jobs_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )

                # Job listings with expandable cards
                st.markdown("### 📋 Job Listings")

                # Filters
                st.markdown("#### Filter Results")
                filter_col1, filter_col2, filter_col3 = st.columns(3)

                with filter_col1:
                    if 'site' in jobs.columns:
                        selected_sites = st.multiselect(
                            "Filter by platform",
                            options=jobs['site'].unique(),
                            default=jobs['site'].unique()
                        )
                        filtered_jobs = jobs[jobs['site'].isin(selected_sites)]
                    else:
                        filtered_jobs = jobs

                with filter_col2:
                    if 'location' in jobs.columns:
                        selected_locations = st.multiselect(
                            "Filter by location",
                            options=jobs['location'].unique()[:10],  # Show top 10 locations
                            default=[]
                        )
                        if selected_locations:
                            filtered_jobs = filtered_jobs[filtered_jobs['location'].isin(selected_locations)]

                with filter_col3:
                    search_filter = st.text_input("Search in titles", "")
                    if search_filter:
                        filtered_jobs = filtered_jobs[
                            filtered_jobs['title'].str.contains(search_filter, case=False, na=False)]

                # Display jobs
                st.markdown(f"**Showing {len(filtered_jobs)} of {len(jobs)} jobs**")

                for idx, row in filtered_jobs.head(20).iterrows():  # Show first 20
                    with st.expander(f"📌 {row['title']} @ {row['company']}"):
                        col1, col2 = st.columns([2, 1])

                        with col1:
                            st.markdown(f"**Company:** {row['company']}")
                            st.markdown(f"**Location:** {row['location']}")
                            if 'job_type' in row and pd.notna(row['job_type']):
                                st.markdown(f"**Job Type:** {row['job_type']}")
                            if 'description' in row and pd.notna(row['description']):
                                st.markdown("**Description:**")
                                st.markdown(row['description'][:300] + "...")

                        with col2:
                            if 'job_url' in row and pd.notna(row['job_url']):
                                st.markdown(f"[🔗 Apply Here]({row['job_url']})")
                            if 'site' in row:
                                st.markdown(f"**Source:** {row['site']}")
                            if 'date_posted' in row:
                                st.markdown(f"**Posted:** {row['date_posted']}")

                if len(filtered_jobs) > 20:
                    st.info(f"Showing 20 of {len(filtered_jobs)} jobs. Download the full list to see all results.")

            else:
                progress_bar.empty()
                st.warning("No jobs found. Try adjusting your search criteria.")

    else:
        # Welcome message when no search performed
        st.markdown("""
        ## 👋 Welcome to Job Finder!

        This tool helps you find job opportunities in Germany for:
        - 📊 **Data Analysts**
        - 🔬 **Epidemiologists**
        - 🤖 **Data Scientists**

        ### How to use:
        1. Configure your search in the **sidebar** 👈
        2. Click **"SEARCH JOBS"** button
        3. Review results and download as Excel/CSV
        4. Click job links to apply directly

        ### Features:
        - ✅ Multi-platform search (Indeed, LinkedIn, Glassdoor)
        - ✅ Exclude senior/lead positions
        - ✅ Filter by location
        - ✅ Download results
        - ✅ Interactive job cards
        """)


if __name__ == "__main__":
    main()