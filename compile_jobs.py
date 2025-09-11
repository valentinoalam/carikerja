import os
import re
from datetime import datetime
from collections import defaultdict
import glob
def parse_job_file(filepath):
    """Parse a job results file and extract job data"""
    jobs = []
    current_platform = None
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Split content by platform sections
    platform_sections = re.split(r'---\s+([A-Z\s]+)\s+\(\d+\s+jobs\s+found\)\s+---\n|---\s+([A-Z\s]+)\s+---\s+No jobs found\n', content)
    platform_sections.pop(0)
    platform_sections = [entry for entry in platform_sections if entry]

    for index, platform_section in enumerate(platform_sections):
        platform_content = platform_section
        
        # Parse individual jobs from platform content
        job_entries = re.split(r'\n\s*\n', platform_content)
        job_entries = [entry.strip() for entry in job_entries if entry.strip() and 'Link:' in entry]
        
        for job_entry in job_entries:
            job_data = parse_single_job(job_entry)
            if job_data:
                jobs.append(job_data)
    return jobs

def extract_platform_name(url):
    # Initialize clean_url to the original URL
    clean_url = url

    # Remove protocol prefixes
    if clean_url.startswith('https://www.'):
        clean_url = clean_url.replace("https://www.", "", 1)
    elif clean_url.startswith('http://www.'):
        clean_url = clean_url.replace("http://www.", "", 1)
    elif clean_url.startswith('https://'):
        clean_url = clean_url.replace("https://", "", 1)
    elif clean_url.startswith('http://'):
        clean_url = clean_url.replace("http://", "", 1)

    # Split the string by the dot and take the first part
    # This handles both "example.com" and "example.com/page"
    platform_name = clean_url.split('.')[0]
    return platform_name

def parse_single_job(job_text):
    """Parse a single job entry from text"""
    lines = job_text.strip().split('\n')
    if not lines:
        return None
    
    job_data = {
        'platform': None,
        'title': lines[0].strip(),
        'company': None,
        'skills': None,
        'location': None,
        'posted_date': None,
        'link': None,
        'headquarters': None,
        'categories': None
    }
    
    # Parse job details from subsequent lines
    for line in lines[1:]:
        line = line.strip()
        if line.startswith('Company:'):
            job_data['company'] = line.replace('Company:', '').strip()
        elif line.startswith('Skills:'):
            job_data['skills'] = line.replace('Skills:', '').strip()
        elif line.startswith('Location:'):
            job_data['location'] = line.replace('Location:', '').strip()
        elif line.startswith('Posted:'):
            job_data['posted_date'] = line.replace('Posted:', '').strip()
        elif line.startswith('Link:'):
            job_data['link'] = line.replace('Link:', '').strip()
        elif line.startswith('Headquarters:'):
            job_data['headquarters'] = line.replace('Headquarters:', '').strip()
        elif line.startswith('Categories:'):
            job_data['categories'] = line.replace('Categories:', '').strip()
    job_data['platform'] = extract_platform_name(job_data['link'])
    pattern = r"^\d\.+"
    job_data['title'] = re.sub(pattern, '', job_data['title'])
    return job_data

def remove_duplicates(jobs):
    """Remove duplicate jobs based on job links"""
    seen_links = set()
    unique_jobs = []
    
    for job in jobs:
        job_link = job.get('link')
        if job_link and job_link not in seen_links:
            seen_links.add(job_link)
            unique_jobs.append(job)
        elif not job_link:  # Keep jobs without links but mark them
            job['duplicate_warning'] = 'No link available - potential duplicate'
            unique_jobs.append(job)
    
    return unique_jobs

def group_by_platform(jobs):
    """Group jobs by platform"""
    grouped = defaultdict(list)
    
    for job in jobs:
        platform = job['platform']
        grouped[platform].append(job)
    
    return dict(grouped)

def save_compiled_results(grouped_jobs, total_jobs, duplicates_removed):
    """Save compiled and deduplicated results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"compiled_jobs_{timestamp}.txt"
    
    # Create output directory if it doesn't exist
    os.makedirs("compiled_results", exist_ok=True)
    filepath = os.path.join("compiled_results", filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write("=" * 70 + "\n")
        f.write("COMPILED FREELANCE JOB RESULTS\n")
        f.write("=" * 70 + "\n")
        f.write(f"Compilation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Unique Jobs: {len([job for jobs in grouped_jobs.values() for job in jobs])}\n")
        f.write(f"Duplicates Removed: {duplicates_removed}\n")
        f.write(f"Platforms: {len(grouped_jobs)}\n")
        f.write("=" * 70 + "\n\n")
        
        # Write platform summary
        f.write("PLATFORM SUMMARY\n")
        f.write("-" * 30 + "\n")
        for platform, jobs in grouped_jobs.items():
            f.write(f"{platform.upper()}: {len(jobs)} jobs\n")
        f.write("\n")
        
        # Write detailed results for each platform
        for platform, jobs in grouped_jobs.items():
            f.write("=" * 50 + "\n")
            f.write(f"{platform.upper()} - {len(jobs)} JOBS\n")
            f.write("=" * 50 + "\n\n")
            
            for i, job in enumerate(jobs, 1):
                f.write(f"{i}. {job['title']}\n")
                
                if job.get('company'):
                    f.write(f"   Company: {job['company']}\n")
                
                if job.get('skills'):
                    f.write(f"   Skills: {job['skills']}\n")
                
                if job.get('location'):
                    f.write(f"   Location: {job['location']}\n")
                
                if job.get('headquarters'):
                    f.write(f"   Headquarters: {job['headquarters']}\n")
                
                if job.get('categories'):
                    f.write(f"   Categories: {job['categories']}\n")
                
                if job.get('posted_date'):
                    f.write(f"   Posted: {job['posted_date']}\n")
                
                if job.get('link'):
                    f.write(f"   Link: {job['link']}\n")
                
                if job.get('duplicate_warning'):
                    f.write(f"   ⚠️  {job['duplicate_warning']}\n")
                
                f.write("\n")
            
            f.write("\n")
        
        # Write final summary
        f.write("=" * 70 + "\n")
        f.write("COMPILATION SUMMARY\n")
        f.write("=" * 70 + "\n")
        f.write(f"Total Files Processed: {total_jobs}\n")
        f.write(f"Unique Jobs After Deduplication: {len([job for jobs in grouped_jobs.values() for job in jobs])}\n")
        f.write(f"Duplicates Removed: {duplicates_removed}\n")
        f.write(f"Platforms Represented: {', '.join(grouped_jobs.keys())}\n")
        f.write(f"Results saved to: {filepath}\n")
    
    return filepath

def main():
    """Main function to compile job results"""
    print("=== Job Results Compiler ===")
    print("Compiling and deduplicating job search results...\n")
    
    # Find all job result files
    job_files = glob.glob("job_results/*.txt")
    
    if not job_files:
        print("No job result files found in 'job_results' directory.")
        print("Please run the main scraper first to generate job results.")
        return
    
    print(f"Found {len(job_files)} job result files to process:")
    for file in job_files:
        print(f"  - {os.path.basename(file)}")
    print()
    
    # Parse all job files
    all_jobs = []
    for filepath in job_files:
        print(f"Processing {os.path.basename(filepath)}...")
        try:
            jobs = parse_job_file(filepath)
            all_jobs.extend(jobs)
            print(f"  Extracted {len(jobs)} jobs")
        except Exception as e:
            print(f"  Error processing file: {e}")
    
    print(f"\nTotal jobs extracted: {len(all_jobs)}")
    
    # Remove duplicates
    print("Removing duplicates based on job links...")
    original_count = len(all_jobs)
    unique_jobs = remove_duplicates(all_jobs)
    duplicates_removed = original_count - len(unique_jobs)
    
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Unique jobs remaining: {len(unique_jobs)}")
    
    # Group by platform
    print("Grouping jobs by platform...")
    grouped_jobs = group_by_platform(unique_jobs)
    
    print("\nPlatform breakdown:")
    for platform, jobs in grouped_jobs.items():
        print(f"  {platform.upper()}: {len(jobs)} jobs")
    
    # Save compiled results
    print("\nSaving compiled results...")
    try:
        filepath = save_compiled_results(grouped_jobs, len(job_files), duplicates_removed)
        print(f"✅ Compiled results saved to: {filepath}")
        
        # Display summary
        print(f"\n=== Compilation Complete ===")
        print(f"📁 Files processed: {len(job_files)}")
        print(f"🔍 Total jobs found: {original_count}")
        print(f"🗑️  Duplicates removed: {duplicates_removed}")
        print(f"✨ Unique jobs: {len(unique_jobs)}")
        print(f"🏢 Platforms: {len(grouped_jobs)}")
        
    except Exception as e:
        print(f"❌ Error saving compiled results: {e}")

if __name__ == "__main__":
    main()
