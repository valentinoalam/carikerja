import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any
import striprtf.striprtf as rtf

class ProposalGenerator:
    def __init__(self):
        self.platform_configs = {
            'upwork': {
                'max_proposal_length': 1000,
                'connects_cost': 2,
                'key_sections': ['introduction', 'experience', 'approach', 'timeline', 'closing'],
                'tone': 'professional'
            },
            'freelancer': {
                'max_proposal_length': 800,
                'bid_required': True,
                'key_sections': ['greeting', 'understanding', 'solution', 'experience', 'timeline'],
                'tone': 'confident'
            },
            'fiverr': {
                'max_proposal_length': 500,
                'custom_offer': True,
                'key_sections': ['hook', 'value_proposition', 'portfolio', 'call_to_action'],
                'tone': 'friendly'
            },
            'toptal': {
                'max_proposal_length': 1200,
                'screening_required': True,
                'key_sections': ['expertise', 'problem_solving', 'methodology', 'results'],
                'tone': 'expert'
            },
            'linkedin': {
                'max_proposal_length': 1200,
                'key_sections': ['introduction', 'understanding', 'solution', 'experience', 'closing'],
                'tone': 'professional'
            },
            'indeed': {
                'max_proposal_length': 1000,
                'key_sections': ['introduction', 'qualifications', 'experience', 'closing'],
                'tone': 'professional'
            }
        }
        
        self.skill_templates = {
            'web development': {
                'keywords': ['responsive', 'modern', 'scalable', 'user-friendly', 'SEO-optimized'],
                'technologies': ['React', 'Node.js', 'Python', 'JavaScript', 'HTML5', 'CSS3'],
                'deliverables': ['fully functional website', 'responsive design', 'clean code', 'documentation']
            },
            'mobile development': {
                'keywords': ['native', 'cross-platform', 'user experience', 'performance', 'app store'],
                'technologies': ['React Native', 'Flutter', 'Swift', 'Kotlin', 'iOS', 'Android'],
                'deliverables': ['mobile app', 'app store submission', 'testing', 'maintenance']
            },
            'data science': {
                'keywords': ['insights', 'analytics', 'machine learning', 'visualization', 'predictive'],
                'technologies': ['Python', 'R', 'SQL', 'Pandas', 'Scikit-learn', 'TensorFlow'],
                'deliverables': ['data analysis', 'reports', 'models', 'visualizations']
            },
            'graphic design': {
                'keywords': ['creative', 'brand identity', 'visual appeal', 'modern design', 'professional'],
                'technologies': ['Adobe Creative Suite', 'Figma', 'Sketch', 'Canva', 'Illustrator'],
                'deliverables': ['design concepts', 'final files', 'revisions', 'brand guidelines']
            }
        }

    def load_compiled_jobs(self, filename: str = 'compiled_jobs.json') -> List[Dict]:
        """Load compiled job data from JSON file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"❌ File {filename} not found. Please run compile_jobs.py first.")
                return []
        except Exception as e:
            print(f"❌ Error loading jobs: {e}")
            return []

    def extract_job_requirements(self, job: Dict) -> Dict:
        """Extract key requirements from job description"""
        description = job.get('description', '').lower()
        title = job.get('title', '').lower()
        skills = job.get('skills', '').lower()
        
        # Extract budget information
        budget_match = re.search(r'\$(\d+(?:,\d+)?(?:\.\d+)?)', job.get('budget', ''))
        budget = budget_match.group(1) if budget_match else 'Not specified'
        
        # Extract timeline
        timeline_keywords = ['urgent', 'asap', 'immediate', 'week', 'month', 'days']
        timeline = 'Standard'
        for keyword in timeline_keywords:
            if keyword in description or keyword in title:
                timeline = 'Urgent' if keyword in ['urgent', 'asap', 'immediate'] else 'Flexible'
                break
        
        # Identify skill category
        skill_category = self.identify_skill_category(title + ' ' + skills + ' ' + description)
        
        # Extract key requirements
        requirements = []
        requirement_patterns = [
            r'must have (.+?)(?:\.|,|$)',
            r'required (.+?)(?:\.|,|$)',
            r'experience with (.+?)(?:\.|,|$)',
            r'knowledge of (.+?)(?:\.|,|$)'
        ]
        
        for pattern in requirement_patterns:
            matches = re.findall(pattern, description)
            requirements.extend(matches)
        
        return {
            'budget': budget,
            'timeline': timeline,
            'skill_category': skill_category,
            'requirements': requirements[:5],  # Top 5 requirements
            'complexity': self.assess_complexity(description, title)
        }

    def identify_skill_category(self, text: str) -> str:
        """Identify the main skill category from job text"""
        text = text.lower()
        
        categories = {
            'web development': ['website', 'web', 'html', 'css', 'javascript', 'react', 'vue', 'angular'],
            'mobile development': ['mobile', 'app', 'ios', 'android', 'flutter', 'react native'],
            'data science': ['data', 'analytics', 'machine learning', 'python', 'analysis', 'statistics'],
            'graphic design': ['design', 'logo', 'branding', 'photoshop', 'illustrator', 'creative'],
            'writing': ['content', 'writing', 'copywriting', 'blog', 'article', 'seo'],
            'marketing': ['marketing', 'social media', 'advertising', 'promotion', 'campaign']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'general'

    def assess_complexity(self, description: str, title: str) -> str:
        """Assess project complexity based on description"""
        text = (description + ' ' + title).lower()
        
        complex_indicators = ['complex', 'advanced', 'enterprise', 'scalable', 'integration', 'api']
        simple_indicators = ['simple', 'basic', 'quick', 'small', 'minor', 'easy']
        
        complex_score = sum(1 for indicator in complex_indicators if indicator in text)
        simple_score = sum(1 for indicator in simple_indicators if indicator in text)
        
        if complex_score > simple_score:
            return 'Complex'
        elif simple_score > complex_score:
            return 'Simple'
        else:
            return 'Medium'

    def generate_proposal(self, job: Dict, user_profile: Dict) -> Dict:
        """Generate a customized proposal for a specific job"""
        platform = job.get('platform', '').lower()
        requirements = self.extract_job_requirements(job)
        
        if platform not in self.platform_configs:
            platform = 'freelancer'  # Default platform
        
        config = self.platform_configs[platform]
        skill_template = self.skill_templates.get(requirements['skill_category'], self.skill_templates['web development'])
        
        # Generate proposal sections
        proposal_sections = self.create_proposal_sections(job, requirements, user_profile, config, skill_template)
        
        # Combine sections into full proposal
        full_proposal = self.combine_proposal_sections(proposal_sections, config)
        
        return {
            'job_id': job.get('link', ''),
            'job_title': job.get('title', ''),
            'platform': platform,
            'company': job.get('company', ''),
            'proposal': full_proposal,
            'estimated_time': self.estimate_project_time(requirements),
            'suggested_rate': self.suggest_rate(requirements, user_profile),
            'key_points': proposal_sections.get('key_points', []),
            'requirements_analysis': requirements
        }

    def create_proposal_sections(self, job: Dict, requirements: Dict, user_profile: Dict, config: Dict, skill_template: Dict) -> Dict:
        """Create individual sections of the proposal"""
        sections = {}
        
        # Get company name for personalization
        company_name = job.get('company', 'the company')
        job_title = job.get('title', 'project')
        
        # Introduction/Greeting - Personalized with company name
        if config['tone'] == 'professional':
            sections['introduction'] = f"Dear Hiring Manager at {company_name},\n\nI am excited to submit my proposal for your {job_title} position."
        elif config['tone'] == 'friendly':
            sections['introduction'] = f"Hi {company_name} team! 👋\n\nI'd love to help you with your {job_title} project!"
        else:
            sections['introduction'] = f"Hello {company_name} team,\n\nI'm interested in your {job_title} and believe I'm the right fit."
        
        # Understanding/Problem Analysis - Tailored to job description
        job_description = job.get('description', '')
        if 'urgent' in job_description.lower():
            urgency_note = "I understand this is time-sensitive and can prioritize accordingly."
        else:
            urgency_note = ""
            
        sections['understanding'] = f"I've reviewed your requirements and understand you need {', '.join(skill_template['deliverables'][:2])}. {urgency_note}"
        if requirements['complexity'] == 'Complex':
            sections['understanding'] += " This appears to be a comprehensive project requiring attention to detail and advanced technical skills."
        else:
            sections['understanding'] += " This project aligns perfectly with my expertise and experience."
        
        # Solution/Approach - Customized based on job requirements
        sections['approach'] = f"My approach to your {job_title} will include:\n"
        sections['approach'] += f"• Utilizing {', '.join(skill_template['technologies'][:3])} for optimal results\n"
        sections['approach'] += f"• Ensuring {', '.join(skill_template['keywords'][:2])} outcomes\n"
        sections['approach'] += f"• Delivering {', '.join(skill_template['deliverables'][:2])}\n"
        
        # Add specific solutions based on job description keywords
        if 'responsive' in job_description.lower():
            sections['approach'] += "• Implementing fully responsive design for all devices\n"
        if 'scalable' in job_description.lower():
            sections['approach'] += "• Building scalable architecture for future growth\n"
        if 'api' in job_description.lower():
            sections['approach'] += "• Developing robust API integrations\n"
        
        # Experience - Personalized with years and relevant skills
        experience_years = user_profile.get('experience_years', 3)
        sections['experience'] = f"With {experience_years}+ years of experience in {requirements['skill_category']}, "
        sections['experience'] += f"I have successfully completed similar projects for companies like yours using {', '.join(skill_template['technologies'][:2])}."
        
        # Timeline
        if requirements['timeline'] == 'Urgent':
            sections['timeline'] = f"I understand this is urgent for {company_name} and can start immediately with daily updates to ensure timely delivery."
        else:
            sections['timeline'] = f"I can complete this {job_title} within {self.estimate_project_time(requirements)} with regular progress updates for the {company_name} team."
        
        # Portfolio/Examples
        sections['portfolio'] = f"I'd be happy to share relevant portfolio examples that demonstrate my expertise in {requirements['skill_category']}, specifically tailored to {company_name}'s needs."
        
        # Closing - Personalized
        if config['tone'] == 'friendly':
            sections['closing'] = f"Looking forward to the opportunity to work with {company_name}! Feel free to message me with any questions. 😊"
        else:
            sections['closing'] = f"I look forward to discussing how I can contribute to {company_name}'s success. Thank you for your consideration."
        
        # Key selling points
        sections['key_points'] = [
            f"{experience_years}+ years experience in {requirements['skill_category']}",
            f"Expert in technologies mentioned in your job description",
            "Proven track record with similar companies",
            "Quick response time and clear communication",
            "Quality-focused approach with attention to detail"
        ]
        
        return sections

    def combine_proposal_sections(self, sections: Dict, config: Dict) -> str:
        """Combine proposal sections based on platform requirements"""
        key_sections = config['key_sections']
        max_length = config['max_proposal_length']
        
        proposal_parts = []
        
        for section_key in key_sections:
            if section_key in sections:
                proposal_parts.append(sections[section_key])
        
        full_proposal = '\n\n'.join(proposal_parts)
        
        # Trim if too long
        if len(full_proposal) > max_length:
            full_proposal = full_proposal[:max_length-50] + "...\n\nLooking forward to your response!"
        
        return full_proposal

    def estimate_project_time(self, requirements: Dict) -> str:
        """Estimate project completion time"""
        complexity = requirements['complexity']
        
        time_estimates = {
            'Simple': '3-5 days',
            'Medium': '1-2 weeks',
            'Complex': '2-4 weeks'
        }
        
        return time_estimates.get(complexity, '1-2 weeks')

    def suggest_rate(self, requirements: Dict, user_profile: Dict) -> Dict:
        """Suggest appropriate rates based on project complexity"""
        base_rate = user_profile.get('hourly_rate', 25)
        complexity = requirements['complexity']
        
        multipliers = {
            'Simple': 0.8,
            'Medium': 1.0,
            'Complex': 1.3
        }
        
        suggested_hourly = int(base_rate * multipliers.get(complexity, 1.0))
        
        # Estimate total project cost
        time_estimates = {'Simple': 20, 'Medium': 40, 'Complex': 80}  # hours
        estimated_hours = time_estimates.get(complexity, 40)
        project_total = suggested_hourly * estimated_hours
        
        return {
            'hourly_rate': suggested_hourly,
            'estimated_hours': estimated_hours,
            'project_total': project_total
        }

    def save_proposals(self, proposals: List[Dict], output_dir: str = 'proposals'):
        """Save generated proposals to text files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save individual proposals
        for i, proposal in enumerate(proposals):
            platform = proposal['platform']
            job_title = re.sub(r'[^\w\s-]', '', proposal['job_title'])[:50]
            company = re.sub(r'[^\w\s-]', '', proposal.get('company', 'Unknown'))[:30]
            filename = f"{platform}_{company}_{job_title}_{timestamp}_{i+1}.txt"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"PROPOSAL FOR: {proposal['job_title']}\n")
                f.write(f"COMPANY: {proposal.get('company', 'Not specified')}\n")
                f.write(f"PLATFORM: {proposal['platform'].upper()}\n")
                f.write(f"ESTIMATED TIME: {proposal['estimated_time']}\n")
                f.write(f"SUGGESTED RATE: ${proposal['suggested_rate']['hourly_rate']}/hr\n")
                f.write(f"PROJECT TOTAL: ${proposal['suggested_rate']['project_total']}\n")
                f.write("="*60 + "\n\n")
                f.write(proposal['proposal'])
                f.write("\n\n" + "="*60 + "\n")
                f.write("KEY POINTS TO HIGHLIGHT:\n")
                for point in proposal['key_points']:
                    f.write(f"• {point}\n")
                f.write("\n" + "="*60 + "\n")
                f.write("REQUIREMENTS ANALYSIS:\n")
                f.write(f"Budget: {proposal['requirements_analysis']['budget']}\n")
                f.write(f"Timeline: {proposal['requirements_analysis']['timeline']}\n")
                f.write(f"Complexity: {proposal['requirements_analysis']['complexity']}\n")
                f.write(f"Category: {proposal['requirements_analysis']['skill_category']}\n")
        
        # Save summary report
        summary_file = os.path.join(output_dir, f'proposal_summary_{timestamp}.txt')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"PROPOSAL GENERATION SUMMARY\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total proposals: {len(proposals)}\n\n")
            
            # Platform breakdown
            platform_counts = {}
            for proposal in proposals:
                platform = proposal['platform']
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
            
            f.write("PLATFORM BREAKDOWN:\n")
            for platform, count in platform_counts.items():
                f.write(f"• {platform.upper()}: {count} proposals\n")
            
            f.write("\nPROPOSAL FILES GENERATED:\n")
            for i, proposal in enumerate(proposals):
                platform = proposal['platform']
                job_title = re.sub(r'[^\w\s-]', '', proposal['job_title'])[:50]
                company = re.sub(r'[^\w\s-]', '', proposal.get('company', 'Unknown'))[:30]
                filename = f"{platform}_{company}_{job_title}_{timestamp}_{i+1}.txt"
                f.write(f"• {filename}\n")
        
        print(f"✅ Generated {len(proposals)} text proposals in '{output_dir}' directory")
        print(f"📄 Summary report: {summary_file}")

    def save_proposals_to_rtf(self, proposals: List[Dict], output_dir: str = 'proposals_rtf'):
        """Save generated proposals to RTF files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for i, proposal in enumerate(proposals):
            platform = proposal['platform']
            job_title = re.sub(r'[^\w\s-]', '', proposal['job_title'])[:50]
            company = re.sub(r'[^\w\s-]', '', proposal.get('company', 'Unknown'))[:30]
            filename = f"{platform}_{company}_{job_title}_{timestamp}_{i+1}.rtf"
            filepath = os.path.join(output_dir, filename)
            
            # Create RTF content
            rtf_content = self._create_rtf_content(proposal)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(rtf_content)
        
        print(f"✅ Generated {len(proposals)} RTF proposals in '{output_dir}' directory")

    def _create_rtf_content(self, proposal: Dict) -> str:
        """Create RTF formatted content for a proposal"""
        rtf_header = r"""{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}
        \f0\fs24 """
        
        # Header section
        header = f"""
        \\b PROPOSAL FOR: {proposal['job_title']}\\b0\\par
        COMPANY: {proposal.get('company', 'Not specified')}\\par
        PLATFORM: {proposal['platform'].upper()}\\par
        ESTIMATED TIME: {proposal['estimated_time']}\\par
        SUGGESTED RATE: ${proposal['suggested_rate']['hourly_rate']}/hr\\par
        PROJECT TOTAL: ${proposal['suggested_rate']['project_total']}\\par
        \\line\\par
        """
        
        # Proposal content
        proposal_content = proposal['proposal'].replace('\n', '\\par ') + '\\par\\par'
        
        # Key points section
        key_points = "\\b KEY POINTS TO HIGHLIGHT:\\b0\\par"
        for point in proposal['key_points']:
            key_points += f"• {point}\\par"
        
        key_points += "\\par\\line\\par"
        
        # Requirements analysis
        requirements = "\\b REQUIREMENTS ANALYSIS:\\b0\\par"
        requirements += f"Budget: {proposal['requirements_analysis']['budget']}\\par"
        requirements += f"Timeline: {proposal['requirements_analysis']['timeline']}\\par"
        requirements += f"Complexity: {proposal['requirements_analysis']['complexity']}\\par"
        requirements += f"Category: {proposal['requirements_analysis']['skill_category']}\\par"
        
        # Combine all sections
        full_rtf = rtf_header + header + proposal_content + key_points + requirements + "}"
        
        return full_rtf

def main():
    """Main function to generate proposals for compiled jobs"""
    print("🤖 Auto Proposal Generator")
    print("=" * 50)
    
    # User profile setup
    print("\n📝 Setting up your profile...")
    user_profile = {
        'experience_years': int(input("Years of experience (default 3): ") or "3"),
        'hourly_rate': int(input("Preferred hourly rate in USD (default 25): ") or "25"),
        'specialization': input("Main specialization (e.g., web development): ") or "web development"
    }
    
    # Load compiled jobs
    generator = ProposalGenerator()
    jobs = generator.load_compiled_jobs()
    
    if not jobs:
        print("❌ No jobs found. Please run compile_jobs.py first.")
        return
    
    print(f"\n📊 Found {len(jobs)} jobs to process")
    
    # Filter options
    print("\n🔍 Filter options:")
    print("1. Generate proposals for all jobs")
    print("2. Filter by platform")
    print("3. Filter by skill category")
    print("4. Filter by complexity")
    
    choice = input("\nEnter your choice (1-4, default 1): ") or "1"
    
    filtered_jobs = jobs
    
    if choice == "2":
        platforms = list(set(job.get('platform', '').lower() for job in jobs))
        print("\nAvailable platforms:", ', '.join(platforms))
        selected_platform = input("Enter platform name: ").lower()
        filtered_jobs = [job for job in jobs if job.get('platform', '').lower() == selected_platform]
    
    elif choice == "3":
        categories = list(set(generator.identify_skill_category(job.get('title', '') + ' ' + job.get('description', '')) for job in jobs))
        print("\nAvailable categories:", ', '.join(categories))
        selected_category = input("Enter category: ").lower()
        filtered_jobs = [job for job in jobs if generator.identify_skill_category(job.get('title', '') + ' ' + job.get('description', '')) == selected_category]
    
    elif choice == "4":
        complexities = ['Simple', 'Medium', 'Complex']
        print("\nAvailable complexities:", ', '.join(complexities))
        selected_complexity = input("Enter complexity: ").capitalize()
        filtered_jobs = [job for job in jobs if generator.assess_complexity(job.get('description', ''), job.get('title', '')) == selected_complexity]
    
    print(f"\n🎯 Generating proposals for {len(filtered_jobs)} jobs...")
    
    # Generate proposals
    proposals = []
    for i, job in enumerate(filtered_jobs, 1):
        print(f"📝 Generating proposal {i}/{len(filtered_jobs)}: {job.get('title', 'Unknown')[:50]}...")
        proposal = generator.generate_proposal(job, user_profile)
        proposals.append(proposal)
    
    # Save proposals
    generator.save_proposals(proposals)
    generator.save_proposals_to_rtf(proposals)
    
    print(f"\n✅ Successfully generated {len(proposals)} proposals!")
    print("📁 Check the 'proposals' and 'proposals_rtf' folders for your files.")
    
    print(f"\n✅ Successfully generated {len(proposals)} proposals!")
    print("📁 Check the 'proposals' directory for your customized proposals.")
    print("\n⚠️  IMPORTANT REMINDERS:")
    print("• Review each proposal before submitting")
    print("• Customize proposals further based on specific job requirements")
    print("• Follow each platform's terms of service")
    print("• Never submit identical proposals to multiple jobs")

if __name__ == "__main__":
    main()