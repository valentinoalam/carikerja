import pandas as pd
import json
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

def save_results_to_csv(all_results, job_keys, location):
    """Save results to CSV file"""
    flat_jobs = []
    for company, jobs in all_results.items():
        for job in jobs:
            job['platform'] = company
            flat_jobs.append(job)

    if not flat_jobs:
        print("No results to save.")
        return None

    df = pd.DataFrame(flat_jobs)
    filename = f'{job_keys}_jobs.csv'
    df.to_csv(filename, index=False)
    print(f"Links with dates saved in file {filename}")
    return filename

def save_results_to_json(all_results, job_keys, location):
    """Save job search results to a JSON file"""
    flat_jobs = []
    for company, jobs in all_results.items():
        for job in jobs:
            job['platform'] = company
            # Add search metadata to each job
            job['search_keywords'] = job_keys
            job['search_location'] = location
            job['search_date'] = datetime.now().isoformat()
            flat_jobs.append(job)

    if not flat_jobs:
        print("No results to save.")
        return None

    # Create filename based on skills and location
    skills_str = "_".join([key.replace(" ", "-").lower() for key in job_keys])
    location_str = location.replace(" ", "-").lower() if location else "global"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    filename = f"jobs_{skills_str}_{location_str}_{timestamp}.json"
    
    # Create output directory if it doesn't exist
    os.makedirs("job_results", exist_ok=True)
    filepath = os.path.join("job_results", filename)
    
    # Prepare data for JSON export
    export_data = {
        "metadata": {
            "search_keywords": job_keys,
            "location": location,
            "search_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_jobs": len(flat_jobs),
            "platforms_searched": list(all_results.keys())
        },
        "jobs": flat_jobs
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"JSON results saved to: {filepath}")
    return filepath

def save_results_to_text(all_results, job_keys, location):
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
        
        total_jobs = 0
        
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

def select_jobs_for_proposals(all_results):
    """Allow user to select jobs for proposal generation"""
    flat_jobs = []
    for company, jobs in all_results.items():
        for job in jobs:
            job['platform'] = company
            flat_jobs.append(job)
    
    if not flat_jobs:
        print("No jobs available for selection.")
        return []
    
    print("\n" + "="*60)
    print("SELECT JOBS FOR PROPOSAL GENERATION")
    print("="*60)
    
    for i, job in enumerate(flat_jobs, 1):
        print(f"{i}. [{job['platform'].upper()}] {job['title']}")
        if job.get('company'):
            print(f"   Company: {job['company']}")
        if job.get('skills'):
            print(f"   Skills: {job['skills']}")
        print()
    
    print("Enter the numbers of jobs you want to generate proposals for (comma-separated)")
    print("Or type 'all' to select all jobs")
    
    while True:
        selection = input("Your selection: ").strip()
        
        if selection.lower() == 'all':
            return flat_jobs
        
        try:
            selected_indices = [int(idx.strip()) - 1 for idx in selection.split(',')]
            selected_jobs = [flat_jobs[i] for i in selected_indices if 0 <= i < len(flat_jobs)]
            
            if selected_jobs:
                print(f"\nSelected {len(selected_jobs)} jobs for proposal generation.")
                return selected_jobs
            else:
                print("No valid jobs selected. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas or 'all'.")

def generate_cover_letters_interactive(all_results, job_keys, location):
    """Interactive cover letter generation after job search"""
    from cover_letter import CoverLetterGenerator
    
    flat_jobs = []
    for company, jobs in all_results.items():
        for job in jobs:
            job['platform'] = company
            flat_jobs.append(job)
    
    if not flat_jobs:
        print("No jobs available for cover letter generation.")
        return
    
    print("\n" + "="*60)
    print("COVER LETTER GENERATION")
    print("="*60)
    
    # Let user select jobs
    selected_jobs = select_jobs_for_proposals(all_results)
    if not selected_jobs:
        return
    
    # Get candidate profile
    print("\n📝 Setting up your candidate profile...")
    candidate_profile = {
        'full_name': input("Full Name: ").strip() or "Your Name",
        'email': input("Email: ").strip() or "your.email@example.com",
        'phone': input("Phone: ").strip() or "+1-234-567-8900",
        'address': input("Address: ").strip() or "123 Main Street, City, State 12345",
        'linkedin': input("LinkedIn (optional): ").strip(),
        'portfolio': input("Portfolio (optional): ").strip(),
        'experience_years': int(input("Years of experience (default 3): ").strip() or "3"),
        'primary_skills': input("Primary skills (comma-separated): ").strip() or "Python, JavaScript, React"
    }
    
    # Select tone
    print("\n🎭 Select cover letter tone:")
    print("1. Professional (Recommended)")
    print("2. Modern")
    print("3. Enthusiastic")
    print("4. Technical")
    
    tone_choice = input("Choose tone (1-4, default 1): ").strip() or "1"
    tone_map = {'1': 'professional', '2': 'modern', '3': 'enthusiastic', '4': 'technical'}
    selected_tone = tone_map.get(tone_choice, 'professional')
    
    # Generate cover letters
    generator = CoverLetterGenerator()
    print(f"\n🎯 Generating {len(selected_jobs)} cover letters...")
    cover_letters = generator.generate_cover_letter_batch(selected_jobs, candidate_profile, selected_tone)
    
    # Save cover letters
    generator.save_cover_letters(cover_letters)
    generator.save_cover_letters_to_rtf(cover_letters)
    
    print(f"\n✅ Successfully generated {len(cover_letters)} cover letters!")
    print("📁 Check the 'cover_letters' and 'cover_letters_rtf' folders.")

def compile_jobs_from_json(json_file_path: str = None):
    """Compile job data from JSON files into a single file"""
    
    if json_file_path is None:
        # Look for JSON files in job_results directory
        json_files = []
        if os.path.exists('job_results'):
            for file in os.listdir('job_results'):
                if file.endswith('.json'):
                    json_files.append(os.path.join('job_results', file))
        
        if not json_files:
            print("❌ No JSON files found in 'job_results' directory")
            return None
    else:
        json_files = [json_file_path]
    
    all_jobs = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                jobs = data.get('jobs', [])
                all_jobs.extend(jobs)
                print(f"✅ Loaded {len(jobs)} jobs from {json_file}")
        except Exception as e:
            print(f"❌ Error loading {json_file}: {e}")
    
    if not all_jobs:
        print("❌ No jobs found in JSON files")
        return None
    
    # Create compiled data structure
    compiled_data = {
        "metadata": {
            "compilation_date": datetime.now().isoformat(),
            "total_jobs": len(all_jobs),
            "source_files": json_files,
            "platforms": list(set(job.get('platform', 'Unknown') for job in all_jobs))
        },
        "jobs": all_jobs
    }
    
    # Save compiled jobs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"compiled_jobs_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(compiled_data, f, indent=2, ensure_ascii=False)
    
    # Also create a default compiled_jobs.json for easy access
    with open("compiled_jobs.json", 'w', encoding='utf-8') as f:
        json.dump(compiled_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully compiled {len(all_jobs)} jobs into {output_file}")
    print(f"📁 Also saved as compiled_jobs.json for easy access")
    
    return compiled_data

# if __name__ == "__main__":
#     print("🔄 Job Data Compiler")
#     print("=" * 40)
    
#     # Ask user if they want to specify a file
#     use_specific = input("Use specific JSON file? (y/n, default n): ").strip().lower()
    
#     if use_specific == 'y':
#         file_path = input("Enter JSON file path: ").strip()
#         if not os.path.exists(file_path):
#             print("❌ File not found!")
#         else:
#             compile_jobs_from_json(file_path)
#     else:
#         compile_jobs_from_json()

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
            # Save to multiple formats
            csv_file = save_results_to_csv(all_results, job_keys, location)
            json_file = save_results_to_json(all_results, job_keys, location)
            txt_file = save_results_to_text(all_results, job_keys, location)
            
            print(f"\nResults exported to:")
            if csv_file: print(f"  CSV: {csv_file}")
            if json_file: print(f"  JSON: {json_file}")
            if txt_file: print(f"  Text: {txt_file}")
            
            # Ask if user wants to generate proposals
            print("\n" + "="*50)
            generate_proposals = input("Do you want to generate proposals for these jobs? (y/n): ").strip().lower()
            
            if generate_proposals == 'y':
                selected_jobs = select_jobs_for_proposals(all_results)
                if selected_jobs:
                    # Import and use the proposal generator
                    from auto_proposal import ProposalGenerator
                    
                    print("\nSetting up proposal generation...")
                    user_profile = {
                        'experience_years': int(input("Years of experience (default 3): ") or "3"),
                        'hourly_rate': int(input("Preferred hourly rate in USD (default 25): ") or "25"),
                        'specialization': input("Main specialization (e.g., web development): ") or "web development"
                    }
                    
                    generator = ProposalGenerator()
                    proposals = []
                    
                    for i, job in enumerate(selected_jobs, 1):
                        print(f"Generating proposal {i}/{len(selected_jobs)}: {job['title'][:50]}...")
                        proposal = generator.generate_proposal(job, user_profile)
                        proposals.append(proposal)
                    
                    # Save proposals in multiple formats
                    generator.save_proposals(proposals)
                    generator.save_proposals_to_rtf(proposals)
            print("\n" + "="*50)
            generate_cover_letters = input("Do you want to generate cover letters for these jobs? (y/n): ").strip().lower()

            if generate_cover_letters == 'y':
                generate_cover_letters_interactive(all_results, job_keys, location)
        except Exception as e:
            print(f"Error saving results: {e}")
    
    if total_jobs_found == 0:
        print("\nTips for better results:")
        print("- Try different keywords or broader terms")
        print("- Check if the platforms are accessible from your location")
        print("- Some platforms may have changed their structure")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())