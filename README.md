# Freelance Job Scraper

An improved Python script that searches for freelance opportunities across multiple platforms:
- **Freelancer.com** - Global freelancing platform
- **Upwork.com** - Professional freelancing marketplace  
- **Toptal.com** - Elite talent network
- **Fiverr.com** - Digital services marketplace
- **TimesJobs.com** - Indian job portal
- **Indeed.com** - Global job search engine
- **Remote.co** - Remote work opportunities
- **AngelList/Wellfound** - Startup jobs
- **We Work Remotely** - Remote job board

## Features

- Search multiple platforms simultaneously
- Keyword-based job filtering
- Location-based filtering (where supported)
- Improved error handling and retry logic
- Respectful scraping with delays
- Clean, formatted output
- Export results to text files
- Job compilation and deduplication
- Automated proposal generation for compiled jobs

## Installation

1. Install required packages:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Usage

### Basic Job Search

Run the main script:
\`\`\`bash
python main.py
\`\`\`

Follow the prompts to:
1. Enter skills/keywords (e.g., "python", "web development")
2. Optionally specify a location
3. View results from all platforms
4. Results are automatically saved to `job_results/` directory

### Compile and Deduplicate Results

After running multiple searches, compile all results:
\`\`\`bash
python compile_jobs.py
\`\`\`

This will:
- Read all files from `job_results/` directory
- Remove duplicate jobs based on job links
- Group jobs by platform
- Save compiled results to `compiled_results/` directory

### Auto Proposal Generator

Generate customized proposals for compiled jobs:
\`\`\`bash
python auto_proposal.py
\`\`\`

Features:
- **Platform-specific proposals**: Tailored for Upwork, Freelancer, Fiverr, Toptal
- **Smart analysis**: Extracts job requirements, budget, timeline, complexity
- **Customized content**: Generates proposals based on your skills and experience
- **Rate suggestions**: Recommends hourly rates and project estimates
- **Bulk generation**: Creates proposals for multiple jobs simultaneously

The generator will:
1. Prompt for your profile (experience, rates, specialization)
2. Analyze compiled job requirements
3. Generate platform-optimized proposals
4. Save individual proposal files in `proposals/` directory
5. Create a summary report with key insights

**Important**: Always review and customize proposals before submitting. This tool generates templates that require manual review and personalization.

## File Structure

\`\`\`
freelance-scraper/
├── main.py                 # Main scraper script
├── get_jobs.py            # Platform-specific scraping functions
├── get_location_names.py  # Location mappings for platforms
├── compile_jobs.py        # Job compilation and deduplication
├── auto_proposal.py       # Automated proposal generator
├── requirements.txt       # Python dependencies
├── job_results/          # Individual search results
├── compiled_results/     # Compiled and deduplicated results
└── proposals/            # Generated proposal templates
\`\`\`

## Platform Details

### Freelance Platforms
- **Freelancer**: Project-based work, global reach
- **Upwork**: Professional services, hourly and fixed-price
- **Toptal**: Elite developers and designers
- **Fiverr**: Digital services marketplace

### Job Boards
- **TimesJobs**: Indian job market focus
- **Indeed**: Global job aggregator
- **Remote.co**: Remote work specialists
- **AngelList**: Startup ecosystem jobs
- **We Work Remotely**: Remote-first companies

## Anti-Detection Features

The scraper includes several measures to avoid being blocked:
- Realistic browser headers and user agents
- Human-like delays between requests
- Session management and cookie handling
- Retry logic with exponential backoff
- Fallback to simple requests when Selenium fails

## Troubleshooting

### Common Issues

1. **Chrome/Selenium errors**: Update ChromeDriver or use headless mode
2. **Authentication failures**: Some platforms may require login
3. **Rate limiting**: Increase delays between requests
4. **No results found**: Try different keywords or check platform availability

### Error Handling

The scraper includes comprehensive error handling:
- Network timeouts and connection errors
- Anti-bot detection and CAPTCHA challenges
- Platform structure changes
- Invalid search parameters

## Output Format

### Individual Search Results
\`\`\`
=== FREELANCE JOB SEARCH RESULTS ===
Search Keywords: python, web development
Location: united-states
Search Date: 2024-12-22 14:30:52

--- UPWORK (5 jobs found) ---
1. Python Developer Needed
   Company: Tech Startup Inc.
   Skills: Python, Django, PostgreSQL
   Location: Remote
   Link: https://upwork.com/jobs/...
\`\`\`

### Compiled Results
\`\`\`
=== COMPILED FREELANCE JOB RESULTS ===
Total Unique Jobs: 25
Duplicates Removed: 3
Platforms: 6

PLATFORM SUMMARY
UPWORK: 8 jobs
FREELANCER: 6 jobs
FIVERR: 4 jobs
...
\`\`\`

## Important Notes

- Web scraping may break if platforms change their HTML structure
- Some platforms have anti-scraping measures
- Always respect robots.txt and terms of service
- Consider using official APIs when available
- Add delays between requests to avoid being blocked
- Results are saved automatically for later compilation
- **Proposal Generator**: Review all generated proposals before submitting
- **Ethical Use**: Never submit identical proposals to multiple jobs
- **Platform Compliance**: Follow each platform's terms of service for applications
- **Personalization**: Customize proposals based on specific job requirements

## Legal Disclaimer

This tool is for educational purposes. Always check and comply with each platform's terms of service and robots.txt before scraping.
The proposal generator creates templates for manual review and customization - always personalize proposals before submission and follow platform guidelines for job applications.
