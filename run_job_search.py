"""
Complete Job Finder for jobspy v1.1.82
Run this script to find jobs in Germany
"""

from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime


def main():
    """Main function to search and save jobs"""

    print("=" * 60)
    print("🔍 JOB FINDER - Starting Search")
    print("=" * 60)

    # Get current time for filename
    start_time = datetime.now()
    print(f"📅 Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # ===== CONFIGURE YOUR SEARCH HERE =====
        jobs = scrape_jobs(
            site_name=["indeed", "glassdoor"],  # LinkedIn often blocks, start with Indeed & Glassdoor
            search_term='"Data Analyst" OR Epidemiologist OR "Data Scientist" -senior -lead',
            # Exclude senior/lead roles
            location="Germany",
            results_wanted=30,  # Start with fewer jobs to test
            hours_old=72,  # Jobs from last 3 days
            country_indeed='Germany',
            verbose=True  # Show progress messages
        )

        # Check results
        if jobs is not None and len(jobs) > 0:
            # Add metadata
            jobs['date_found'] = datetime.now().strftime('%Y-%m-%d %H:%M')

            # Save to Excel
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"german_jobs_{timestamp}.xlsx"
            jobs.to_excel(filename, index=False)

            # Print summary
            print("\n" + "=" * 60)
            print("✅ SEARCH COMPLETE")
            print("=" * 60)
            print(f"📊 Total jobs found: {len(jobs)}")
            print(f"💾 Saved to: {filename}")

            # Show job sources breakdown
            if 'site' in jobs.columns:
                print("\n📋 Jobs by platform:")
                print(jobs['site'].value_counts().to_string())

            # Show job types breakdown
            if 'job_type' in jobs.columns:
                print("\n📋 Jobs by type:")
                print(jobs['job_type'].value_counts().to_string())

            # Preview first 5 jobs
            print("\n👀 Preview (first 5 jobs):")
            preview_cols = ['title', 'company', 'location', 'site']
            available_cols = [col for col in preview_cols if col in jobs.columns]
            if available_cols:
                print(jobs[available_cols].head().to_string(index=False))

            # Show file location
            import os
            full_path = os.path.abspath(filename)
            print(f"\n📁 File location: {full_path}")

        else:
            print("\n❌ No jobs found. Try:")
            print("  • Different search terms")
            print("  • Broader location")
            print("  • More sites (add 'linkedin')")

    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

    # Show runtime
    end_time = datetime.now()
    runtime = end_time - start_time
    print(f"\n⏱️  Total runtime: {runtime.total_seconds():.1f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()