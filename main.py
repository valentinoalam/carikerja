import pandas as pd
from get_jobs import *
import sys
import os
from datetime import datetime
import asyncio
def loop_input(ask_for, examples=None):
    """
    Prompts the user to enter a list of items and returns them.
    """
    result = []
    if examples:
        print(f"Examples: {', '.join(examples)}")
    
    while True:
        inp = input(f'Enter a {ask_for} (or press Enter to continue): ').strip()
        if inp == '':
            break
        result.append(inp)
    return result

def display_results(jobs, company, base_link):
    """Display job results in a formatted way"""
    if not jobs:
        print(f"No jobs found on {company.title()}")
        return
    
    print(f'-- {company.title()} ({len(jobs)} results) --')
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']}")
        if job['link']:
            # Handle relative and absolute URLs
            if job['link'].startswith('http'):
                print(f"   Link: {job['link']}")
            elif job['link'].startswith('/'):
                print(f"   Link: {base_link}{job['link']}")
            else:
                print(f"   Link: {base_link}/{job['link']}")
        print()

def save_results_to_file(all_results, job_keys, location):
    df = pd.DataFrame(all_results)

    # حفظ النتائج في ملف CSV
    df.to_csv(f'{job_keys}_jobs.csv', index=False)

    print(f"Links with dates saved in file {job_keys}_jobs.csv")

    """Save job search results to a text file with formatted output"""
    # Create filename based on skills and location
    skills_str = "_".join([key.replace(" ", "-").lower() for key in job_keys])
    location_str = location.replace(" ", "-").lower() if location else "global"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    filename = f"jobs_{skills_str}_{location_str}_{timestamp}.txt"
    
    # Create output directory if it doesn't exist
    os.makedirs("job_results", exist_ok=True)
    filepath = os.path.join("job_results", filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("=" * 60 + "\n")
        f.write("FREELANCE JOB SEARCH RESULTS\n")
        f.write("=" * 60 + "\n")
        f.write(f"Search Keywords: {', '.join(job_keys)}\n")
        f.write(f"Location: {location if location else 'Global'}\n")
        f.write(f"Search Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        total_jobs = len(all_results)
        
        # Write results for each platform
        for company_name, jobs in all_results.items():
            if jobs:
                f.write(f"--- {company_name.upper()} ({len(jobs)} jobs found) ---\n\n")
                
                for i, job in enumerate(jobs, 1):
                    f.write(f"{i}. {job['title']}\n")
                    
                    if job.get('company'):
                        f.write(f"   Company: {job['company']}\n")
                    
                    if job.get('skills'):
                        f.write(f"   Skills: {job['skills']}\n")
                    
                    if job.get('headquarters'):
                        f.write(f"   Headquarters: {job['headquarters']}\n")
                    
                    if job.get('descriptions'):
                        f.write(f"   Categories: {', '.join(job['descriptions'])}\n")
                    
                    if job.get('posted_date'):
                        f.write(f"   Posted: {job['posted_date']}\n")
                    
                    if job.get('location'):
                        f.write(f"   Location: {job['location']}\n")
                    if job.get('link'):
                        # Handle relative and absolute URLs
                        base_link = all_jobs[company_name]['link']
                        if job['link'].startswith('http'):
                            f.write(f"   Link: {job['link']}\n")
                        elif job['link'].startswith('/'):
                            f.write(f"   Link: {base_link}{job['link']}\n")
                        else:
                            f.write(f"   Link: {base_link}/{job['link']}\n")
                    
                    f.write("\n")
                
                total_jobs += len(jobs)
                f.write("\n")
            else:
                f.write(f"--- {company_name.upper()} ---\n")
                f.write("No jobs found\n\n")
        
        # Write summary
        f.write("=" * 60 + "\n")
        f.write("SEARCH SUMMARY\n")
        f.write("=" * 60 + "\n")
        f.write(f"Total Jobs Found: {total_jobs}\n")
        f.write(f"Platforms Searched: {len(all_jobs)}\n")
        f.write(f"Results saved to: {filepath}\n")
    
    return filepath

# Change main() to an async function
async def main():
    """Main function to run the freelance job scraper"""
    print("=== Freelance Job Scraper ===")
    print("Search for freelance opportunities across multiple platforms\n")
    
    job_keys = loop_input('skill/keyword', ['python', 'web development', 'graphic design', 'writing'])
    if not job_keys:
        print("No keywords provided. Exiting...")
        return
    
    print()
    locations = loop_input('location (optional)', ['united-states', 'united-kingdom', 'canada', 'germany'])
    location = locations[0] if locations else None
    
    print()
    print(f"Searching for '{', '.join(job_keys)}' jobs" + (f" in {location}" if location else " globally"))
    print("This may take a moment...\n")
    
    total_jobs_found = 0
    all_results = {}
    
    for company_name, company_info in all_jobs.items():
        print(f"Searching {company_name.title()}...")
        
        try:
            # Check if the function is async and handle it
            job_func = company_info['jobs']
            if asyncio.iscoroutinefunction(job_func):
                jobs = await job_func(job_keys, location)
            else:
                jobs = job_func(job_keys, location)

            all_results[company_name] = jobs
            
            if jobs:
                display_results(jobs, company_name, company_info['link'])
                total_jobs_found += len(jobs)
            else:
                print(f"No relevant jobs found on {company_name.title()}\n")
                
        except Exception as e:
            print(f"Error searching {company_name}: {e}\n")
            all_results[company_name] = []
        
        time.sleep(2)
    
    print(f"=== Search Complete ===")
    print(f"Total jobs found: {total_jobs_found}")
    
    if total_jobs_found > 0:
        try:
            filepath = save_results_to_file(all_results, job_keys, location)
            print(f"\nResults exported to: {filepath}")
        except Exception as e:
            print(f"Error saving results to file: {e}")
    
    if total_jobs_found == 0:
        print("\nTips for better results:")
        print("- Try different keywords or broader terms")
        print("- Check if the platforms are accessible from your location")
        print("- Some platforms may have changed their structure")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
