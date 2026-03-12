"""
Simple Job Finder - Finds jobs and saves to Excel
Run this daily to get fresh job listings
"""

from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime


def find_jobs():
    """Search for jobs and save to Excel"""

    print("🔍 Starting job search...")

    try:
        # Configure your search
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "glassdoor"],  # Where to search
            search_term="Data Analyst OR Epidemiologist OR Data Scientist",  # Multiple job titles
            location="Germany",  # Your location
            results_wanted=50,  # Number of jobs to fetch
            hours_old=72,  # Jobs posted in last 72 hours
            country_indeed='Germany',  # Your country
            linkedin_fetch_description=True  # Get full job details
        )

        # Check if we got any jobs
        if jobs is not None and len(jobs) > 0:
            # Add timestamp
            jobs['date_found'] = datetime.now().strftime('%Y-%m-%d %H:%M')

            # Save to Excel with today's date
            filename = f"jobs_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            jobs.to_excel(filename, index=False)

            print(f"\n✅ Found {len(jobs)} jobs")
            print(f"📁 Saved to {filename}")

            # Show preview
            print("\n📊 Preview of found jobs:")
            preview_cols = ['title', 'company', 'location', 'job_type']
            available_cols = [col for col in preview_cols if col in jobs.columns]
            if available_cols:
                print(jobs[available_cols].head(10))
            else:
                print("Available columns:", jobs.columns.tolist())
                print(jobs.head())
        else:
            print("❌ No jobs found. Try different search terms or locations.")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("\n💡 Tips:")
        print("  - Make sure you have internet connection")
        print("  - Try different search terms")
        print("  - Check if the job sites are accessible")


if __name__ == "__main__":
    find_jobs()