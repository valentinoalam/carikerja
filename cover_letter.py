import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any
import striprtf.striprtf as rtf

class CoverLetterGenerator:
    def __init__(self):
        self.tone_profiles = {
            'professional': {
                'greeting': 'Dear Hiring Manager',
                'closing': 'Sincerely',
                'language': 'formal',
                'keywords': ['excellence', 'professional', 'qualified', 'expertise', 'proven track record']
            },
            'modern': {
                'greeting': 'Hello',
                'closing': 'Best regards',
                'language': 'contemporary',
                'keywords': ['innovative', 'dynamic', 'collaborative', 'impact', 'growth']
            },
            'enthusiastic': {
                'greeting': 'Dear Hiring Team',
                'closing': 'Warm regards',
                'language': 'energetic',
                'keywords': ['excited', 'passionate', 'thrilled', 'eager', 'motivated']
            },
            'technical': {
                'greeting': 'Dear Hiring Committee',
                'closing': 'Respectfully',
                'language': 'precise',
                'keywords': ['optimize', 'implement', 'develop', 'engineer', 'architect']
            }
        }
        
        self.industry_templates = {
            'tech': {
                'intro_phrases': [
                    "With a strong background in {skills} and {experience}+ years of experience",
                    "As an experienced {role} specializing in {skills}",
                    "Bringing expertise in {skills} and a proven track record in"
                ],
                'value_props': [
                    "developing scalable solutions that improve efficiency by 30%",
                    "implementing cutting-edge technologies that drive business growth",
                    "optimizing systems for maximum performance and reliability"
                ]
            },
            'creative': {
                'intro_phrases': [
                    "With a creative approach to {skills} and {experience}+ years of experience",
                    "As a passionate {role} with expertise in {skills}",
                    "Combining artistic vision with technical skills in {skills}"
                ],
                'value_props': [
                    "creating visually stunning designs that engage audiences",
                    "developing compelling visual narratives that tell brand stories",
                    "crafting innovative solutions that blend form and function"
                ]
            },
            'business': {
                'intro_phrases': [
                    "With extensive experience in {skills} and {experience}+ years in the industry",
                    "As a results-driven {role} specializing in {skills}",
                    "Bringing strategic expertise in {skills} and a history of"
                ],
                'value_props': [
                    "driving business growth through strategic initiatives",
                    "optimizing processes to increase efficiency and reduce costs",
                    "developing data-driven strategies that deliver measurable results"
                ]
            }
        }
        
        self.skill_impact_statements = {
            'python': "developed Python applications that processed over 1M+ records daily",
            'javascript': "built interactive web applications serving 10K+ monthly users",
            'react': "created React components that improved user engagement by 40%",
            'node.js': "developed Node.js APIs handling 50K+ requests per hour",
            'aws': "implemented AWS solutions reducing infrastructure costs by 25%",
            'sql': "optimized SQL queries improving database performance by 60%",
            'docker': "containerized applications reducing deployment time by 70%",
            'machine learning': "built ML models with 95% prediction accuracy",
            'ui/ux design': "designed interfaces that increased user satisfaction by 35%",
            'project management': "managed projects delivering 20% under budget"
        }

    def load_job_data(self, json_file_path: str) -> List[Dict]:
        """Load job data from JSON file"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('jobs', [])
        except Exception as e:
            print(f"❌ Error loading job data: {e}")
            return []

    def analyze_job_description(self, job: Dict) -> Dict:
        """Perform deep analysis of job description"""
        description = job.get('description', '').lower()
        title = job.get('title', '').lower()
        skills = job.get('skills', '').lower()
        
        # Extract key requirements
        requirements = self._extract_requirements(description)
        
        # Identify key technologies
        technologies = self._identify_technologies(description + ' ' + skills)
        
        # Determine company culture clues
        culture_indicators = self._analyze_company_culture(description)
        
        # Extract experience level
        experience_level = self._determine_experience_level(description, title)
        
        return {
            'requirements': requirements,
            'technologies': technologies,
            'culture_indicators': culture_indicators,
            'experience_level': experience_level,
            'key_phrases': self._extract_key_phrases(description),
            'company_focus': self._identify_company_focus(description)
        }

    def _extract_requirements(self, description: str) -> List[str]:
        """Extract specific requirements from job description"""
        requirements = []
        patterns = [
            r'must have (.+?)(?:\.|,|$)',
            r'required (.+?)(?:\.|,|$)',
            r'looking for (.+?)(?:\.|,|$)',
            r'qualifications?:?(.+?)(?:\.|,|$)',
            r'experience with (.+?)(?:\.|,|$)',
            r'knowledge of (.+?)(?:\.|,|$)',
            r'ability to (.+?)(?:\.|,|$)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            requirements.extend(matches)
        
        return requirements[:8]  # Return top 8 requirements

    def _identify_technologies(self, text: str) -> List[str]:
        """Identify technologies mentioned in the job description"""
        tech_keywords = {
            'programming': ['python', 'javascript', 'java', 'c#', 'c++', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin'],
            'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'laravel', 'express', 'asp.net'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'dynamodb'],
            'cloud': ['aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'tools': ['git', 'jira', 'confluence', 'figma', 'photoshop', 'illustrator']
        }
        
        found_tech = []
        for category, technologies in tech_keywords.items():
            for tech in technologies:
                if tech in text.lower():
                    found_tech.append(tech)
        
        return found_tech

    def _analyze_company_culture(self, description: str) -> Dict:
        """Analyze company culture from job description"""
        culture_indicators = {
            'collaborative': len(re.findall(r'team|collaborat|work together|partner', description, re.IGNORECASE)),
            'innovative': len(re.findall(r'innovativ|creativ|disrupt|cutting.edge', description, re.IGNORECASE)),
            'fast_paced': len(re.findall(r'fast.paced|dynamic|startup|agile', description, re.IGNORECASE)),
            'structured': len(re.findall(r'process|methodolog|framework|structured', description, re.IGNORECASE))
        }
        
        # Determine dominant culture
        dominant_culture = max(culture_indicators, key=culture_indicators.get)
        
        return {
            'indicators': culture_indicators,
            'dominant': dominant_culture if culture_indicators[dominant_culture] > 0 else 'neutral'
        }

    def _determine_experience_level(self, description: str, title: str) -> str:
        """Determine required experience level"""
        junior_indicators = ['junior', 'entry.level', 'graduate', '0.2 years', '1.3 years']
        senior_indicators = ['senior', 'lead', 'principal', '5\+ years', '7\+ years', '10\+ years']
        
        text = description + ' ' + title
        
        if any(indicator in text for indicator in senior_indicators):
            return 'senior'
        elif any(indicator in text for indicator in junior_indicators):
            return 'junior'
        else:
            return 'mid'

    def _extract_key_phrases(self, description: str) -> List[str]:
        """Extract key phrases that indicate company priorities"""
        key_phrases = []
        priority_indicators = [
            r'critical to', r'essential for', r'key to', r'focus on', 
            r'emphasis on', r'priority is', r'looking for.*who can'
        ]
        
        for pattern in priority_indicators:
            matches = re.findall(pattern, description, re.IGNORECASE)
            key_phrases.extend(matches)
        
        return key_phrases

    def _identify_company_focus(self, description: str) -> str:
        """Identify company's main focus area"""
        focuses = {
            'product': ['product', 'user experience', 'ux', 'customer'],
            'technology': ['technology', 'technical', 'engineering', 'development'],
            'business': ['business', 'revenue', 'growth', 'market'],
            'innovation': ['innovation', 'research', 'development', 'r&d']
        }
        
        focus_scores = {}
        for focus, keywords in focuses.items():
            score = sum(1 for keyword in keywords if keyword in description.lower())
            focus_scores[focus] = score
        
        return max(focus_scores, key=focus_scores.get) if focus_scores else 'general'

    def generate_cover_letter(self, job: Dict, candidate_profile: Dict, tone: str = 'professional') -> Dict:
        """Generate a highly customized cover letter"""
        analysis = self.analyze_job_description(job)
        
        # Select appropriate template based on industry
        industry = self._determine_industry(job.get('title', ''), job.get('description', ''))
        template = self.industry_templates.get(industry, self.industry_templates['tech'])
        
        # Generate sections
        sections = {
            'header': self._generate_header(job, candidate_profile),
            'greeting': self._generate_greeting(job, tone),
            'introduction': self._generate_introduction(job, candidate_profile, analysis, template),
            'body': self._generate_body(job, candidate_profile, analysis),
            'closing': self._generate_closing(job, candidate_profile, tone),
            'signature': self._generate_signature(candidate_profile)
        }
        
        # Combine into full letter
        full_letter = self._combine_sections(sections)
        
        return {
            'job_title': job.get('title', ''),
            'company': job.get('company', ''),
            'cover_letter': full_letter,
            'analysis': analysis,
            'sections': sections,
            'tone': tone,
            'industry': industry
        }

    def _determine_industry(self, title: str, description: str) -> str:
        """Determine the industry based on job title and description"""
        text = (title + ' ' + description).lower()
        
        if any(word in text for word in ['design', 'creative', 'art', 'ui/ux', 'graphic']):
            return 'creative'
        elif any(word in text for word in ['business', 'manager', 'strategy', 'marketing', 'sales']):
            return 'business'
        else:
            return 'tech'

    def _generate_header(self, job: Dict, candidate: Dict) -> str:
        """Generate letter header"""
        header = f"{candidate.get('full_name', 'Your Name')}\n"
        header += f"{candidate.get('address', 'Your Address')}\n"
        header += f"{candidate.get('phone', 'Your Phone')} | {candidate.get('email', 'your.email@example.com')}\n"
        if candidate.get('linkedin'):
            header += f"LinkedIn: {candidate.get('linkedin')}\n"
        if candidate.get('portfolio'):
            header += f"Portfolio: {candidate.get('portfolio')}\n"
        
        header += f"\n{datetime.now().strftime('%B %d, %Y')}\n\n"
        header += f"{job.get('company', 'Hiring Manager')}\n"
        
        # Try to extract company address from job data
        if job.get('location'):
            header += f"{job.get('location')}\n"
        
        return header

    def _generate_greeting(self, job: Dict, tone: str) -> str:
        """Generate personalized greeting"""
        tone_profile = self.tone_profiles.get(tone, self.tone_profiles['professional'])
        company = job.get('company', 'Hiring Manager')
        
        # Try to extract hiring manager name if possible
        description = job.get('description', '')
        manager_patterns = [
            r'report to (.+?)(?:\s|$)',
            r'working with (.+?)(?:\s|$)',
            r'contact (.+?)(?:\s|$)'
        ]
        
        for pattern in manager_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                manager_name = match.group(1).title()
                return f"{tone_profile['greeting']} {manager_name},"
        
        return f"{tone_profile['greeting']} at {company},"

    def _generate_introduction(self, job: Dict, candidate: Dict, analysis: Dict, template: Dict) -> str:
        """Generate compelling introduction"""
        experience = candidate.get('experience_years', 3)
        skills = ', '.join(analysis['technologies'][:3]) if analysis['technologies'] else candidate.get('primary_skills', 'relevant technologies')
        role = job.get('title', 'the position').split()[0] if job.get('title') else 'this role'
        
        # Select random intro phrase from template
        import random
        intro_phrase = random.choice(template['intro_phrases'])
        value_prop = random.choice(template['value_props'])
        
        intro = intro_phrase.format(
            skills=skills,
            experience=experience,
            role=role
        )
        
        intro += f", I was immediately drawn to the {job.get('title', 'position')} at {job.get('company', 'your company')}. "
        intro += f"My background in {value_prop} aligns perfectly with your requirements."
        
        return intro

    def _generate_body(self, job: Dict, candidate: Dict, analysis: Dict) -> str:
        """Generate the main body of the cover letter"""
        body = ""
        
        # Address key requirements
        if analysis['requirements']:
            body += "I was particularly interested to see your emphasis on:\n\n"
            for i, requirement in enumerate(analysis['requirements'][:3], 1):
                # Match requirement with candidate's experience
                matched_experience = self._match_requirement_to_experience(requirement, candidate)
                body += f"• {requirement.capitalize()}: {matched_experience}\n"
            
            body += "\n"
        
        # Highlight relevant achievements
        body += self._highlight_achievements(job, candidate, analysis)
        
        # Show cultural alignment
        body += self._show_cultural_alignment(analysis['culture_indicators'])
        
        return body

    def _match_requirement_to_experience(self, requirement: str, candidate: Dict) -> str:
        """Match job requirement to candidate's experience"""
        requirement_lower = requirement.lower()
        
        # Check for specific skills in requirement
        for skill, impact in self.skill_impact_statements.items():
            if skill in requirement_lower:
                return impact
        
        # Generic response based on requirement type
        if any(word in requirement_lower for word in ['lead', 'manage', 'team']):
            return "Successfully led cross-functional teams delivering projects 20% ahead of schedule"
        elif any(word in requirement_lower for word in ['develop', 'build', 'create']):
            return "Developed multiple production-ready applications serving thousands of users"
        elif any(word in requirement_lower for word in ['optimize', 'improve', 'enhance']):
            return "Implemented optimizations that improved system performance by 40%"
        else:
            return "Gained extensive experience in this area through multiple successful projects"

    def _highlight_achievements(self, job: Dict, candidate: Dict, analysis: Dict) -> str:
        """Highlight relevant achievements"""
        achievements = ""
        
        # Select achievements based on job requirements
        relevant_skills = analysis['technologies'][:2] if analysis['technologies'] else ['technical solutions']
        
        achievements += "In my previous roles, I have successfully:\n\n"
        
        # Generate 2-3 relevant achievements
        achievement_templates = [
            "Implemented {technology} solutions that {impact}",
            "Led the development of {technology} applications resulting in {impact}",
            "Optimized {technology} processes achieving {impact}"
        ]
        
        impacts = [
            "increased efficiency by 35%",
            "reduced costs by 25%",
            "improved performance by 50%",
            "enhanced user satisfaction by 40%"
        ]
        
        import random
        for i in range(min(3, len(relevant_skills))):
            tech = relevant_skills[i] if i < len(relevant_skills) else 'key'
            achievement = random.choice(achievement_templates).format(
                technology=tech,
                impact=random.choice(impacts)
            )
            achievements += f"• {achievement}\n"
        
        achievements += "\n"
        return achievements

    def _show_cultural_alignment(self, culture_indicators: Dict) -> str:
        """Show alignment with company culture"""
        culture = culture_indicators['dominant']
        
        culture_statements = {
            'collaborative': "I thrive in collaborative environments and believe that the best results come from working closely with cross-functional teams to solve complex problems together.",
            'innovative': "I'm passionate about innovation and constantly seek new ways to push boundaries and create cutting-edge solutions that drive meaningful impact.",
            'fast_paced': "I excel in fast-paced environments and am adept at adapting quickly to changing priorities while maintaining high-quality deliverables.",
            'structured': "I appreciate well-defined processes and methodologies that ensure consistent, high-quality outcomes while allowing for continuous improvement.",
            'neutral': "I'm adaptable and thrive in various work environments, always focusing on delivering exceptional results and contributing positively to team dynamics."
        }
        
        return culture_statements.get(culture, culture_statements['neutral']) + "\n\n"

    def _generate_closing(self, job: Dict, candidate: Dict, tone: str) -> str:
        """Generate closing paragraph"""
        tone_profile = self.tone_profiles.get(tone, self.tone_profiles['professional'])
        
        closing = f"I am particularly excited about the opportunity at {job.get('company', 'your company')} because "
        
        # Customize based on company focus
        analysis = self.analyze_job_description(job)
        focus = analysis.get('company_focus', 'general')
        
        focus_reasons = {
            'product': "of your focus on creating exceptional user experiences and innovative products.",
            'technology': "of your commitment to technical excellence and cutting-edge solutions.",
            'business': "of your strategic approach to driving business growth and market impact.",
            'innovation': "of your dedication to innovation and pushing industry boundaries.",
            'general': "it represents an excellent opportunity to apply my skills and experience to meaningful challenges."
        }
        
        closing += focus_reasons.get(focus, focus_reasons['general'])
        closing += f"\n\n{tone_profile['closing']},\n\n"
        
        return closing

    def _generate_signature(self, candidate: Dict) -> str:
        """Generate signature section"""
        return candidate.get('full_name', 'Your Name')

    def _combine_sections(self, sections: Dict) -> str:
        """Combine all sections into a complete cover letter"""
        return (
            f"{sections['header']}"
            f"{sections['greeting']}\n\n"
            f"{sections['introduction']}\n\n"
            f"{sections['body']}"
            f"{sections['closing']}"
            f"{sections['signature']}"
        )

    def save_cover_letters(self, cover_letters: List[Dict], output_dir: str = 'cover_letters'):
        """Save cover letters to text files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for i, letter in enumerate(cover_letters):
            company = re.sub(r'[^\w\s-]', '', letter.get('company', 'Unknown'))[:30]
            job_title = re.sub(r'[^\w\s-]', '', letter.get('job_title', 'Unknown'))[:50]
            filename = f"cover_letter_{company}_{job_title}_{timestamp}_{i+1}.txt"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(letter['cover_letter'])
        
        print(f"✅ Generated {len(cover_letters)} text cover letters in '{output_dir}' directory")

    def save_cover_letters_to_rtf(self, cover_letters: List[Dict], output_dir: str = 'cover_letters_rtf'):
        """Save cover letters to RTF files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for i, letter in enumerate(cover_letters):
            company = re.sub(r'[^\w\s-]', '', letter.get('company', 'Unknown'))[:30]
            job_title = re.sub(r'[^\w\s-]', '', letter.get('job_title', 'Unknown'))[:50]
            filename = f"cover_letter_{company}_{job_title}_{timestamp}_{i+1}.rtf"
            filepath = os.path.join(output_dir, filename)
            
            rtf_content = self._create_rtf_cover_letter(letter)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(rtf_content)
        
        print(f"✅ Generated {len(cover_letters)} RTF cover letters in '{output_dir}' directory")

    def _create_rtf_cover_letter(self, cover_letter: Dict) -> str:
        """Create RTF formatted cover letter"""
        letter_content = cover_letter['cover_letter']
        
        # Convert plain text to RTF format
        rtf_content = r"""{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}
\f0\fs24 """
        
        # Split content into lines and convert
        lines = letter_content.split('\n')
        for line in lines:
            if line.strip() == '':
                rtf_content += '\\par\n'
            else:
                # Handle bold text (company names, job titles)
                bold_patterns = [
                    cover_letter.get('company', ''),
                    cover_letter.get('job_title', '')
                ]
                
                formatted_line = line
                for pattern in bold_patterns:
                    if pattern and pattern in line:
                        formatted_line = formatted_line.replace(pattern, f'\\b {pattern}\\b0')
                
                rtf_content += formatted_line + '\\par\n'
        
        rtf_content += '}'
        return rtf_content

    def generate_cover_letter_batch(self, jobs: List[Dict], candidate_profile: Dict, tone: str = 'professional') -> List[Dict]:
        """Generate cover letters for multiple jobs"""
        cover_letters = []
        
        for i, job in enumerate(jobs, 1):
            print(f"📝 Generating cover letter {i}/{len(jobs)}: {job.get('title', 'Unknown')[:50]}...")
            cover_letter = self.generate_cover_letter(job, candidate_profile, tone)
            cover_letters.append(cover_letter)
        
        return cover_letters

def main():
    """Main function to demonstrate cover letter generation"""
    print("🎯 Enhanced Cover Letter Generator")
    print("=" * 50)
    
    # Initialize generator
    generator = CoverLetterGenerator()
    
    # Load job data
    json_file = input("Enter path to jobs JSON file (default: compiled_jobs.json): ").strip() or "compiled_jobs.json"
    
    try:
        jobs = generator.load_job_data(json_file)
        if not jobs:
            print("❌ No jobs found in the specified file.")
            return
        
        print(f"✅ Loaded {len(jobs)} jobs from {json_file}")
    except Exception as e:
        print(f"❌ Error loading jobs: {e}")
        return
    
    # Candidate profile
    print("\n📝 Candidate Profile Setup:")
    candidate_profile = {
        'full_name': input("Full Name: ").strip() or "John Doe",
        'email': input("Email: ").strip() or "john.doe@example.com",
        'phone': input("Phone: ").strip() or "+1-234-567-8900",
        'address': input("Address: ").strip() or "123 Main Street, City, State 12345",
        'linkedin': input("LinkedIn (optional): ").strip(),
        'portfolio': input("Portfolio (optional): ").strip(),
        'experience_years': int(input("Years of experience (default 3): ").strip() or "3"),
        'primary_skills': input("Primary skills (comma-separated): ").strip() or "Python, JavaScript, React"
    }
    
    # Tone selection
    print("\n🎭 Select Tone:")
    tones = list(generator.tone_profiles.keys())
    for i, tone in enumerate(tones, 1):
        print(f"{i}. {tone.title()}")
    
    tone_choice = input(f"Choose tone (1-{len(tones)}, default 1): ").strip()
    try:
        selected_tone = tones[int(tone_choice) - 1] if tone_choice else 'professional'
    except (ValueError, IndexError):
        selected_tone = 'professional'
    
    print(f"Selected tone: {selected_tone}")
    
    # Job selection
    print(f"\n🔍 Select Jobs for Cover Letters:")
    print(f"Found {len(jobs)} jobs. How many do you want to process?")
    try:
        num_jobs = int(input(f"Number of jobs (1-{len(jobs)}, default {min(5, len(jobs))}): ").strip() or min(5, len(jobs)))
        num_jobs = max(1, min(num_jobs, len(jobs)))
    except ValueError:
        num_jobs = min(5, len(jobs))
    
    selected_jobs = jobs[:num_jobs]
    
    # Generate cover letters
    print(f"\n🎯 Generating {len(selected_jobs)} cover letters...")
    cover_letters = generator.generate_cover_letter_batch(selected_jobs, candidate_profile, selected_tone)
    
    # Save in multiple formats
    generator.save_cover_letters(cover_letters)
    generator.save_cover_letters_to_rtf(cover_letters)
    
    print(f"\n✅ Successfully generated {len(cover_letters)} cover letters!")
    print("📁 Check the 'cover_letters' and 'cover_letters_rtf' folders for your files.")
    
    # Display first cover letter as preview
    if cover_letters:
        print("\n" + "="*60)
        print("PREVIEW OF FIRST COVER LETTER")
        print("="*60)
        print(cover_letters[0]['cover_letter'])
        print("="*60)

if __name__ == "__main__":
    main()