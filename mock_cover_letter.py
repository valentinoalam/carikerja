from datetime import datetime
from string import Template
import re
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

class CoverLetterGenerator:
    """
    A comprehensive cover letter generator that creates personalized cover letters
    based on vacancy details, user data, and customizable templates.
    """
    
    def __init__(self):
        self.templates = {
            'professional': """Dear $hiring_manager,

I am writing to express my strong interest in the $position_title position at $company_name. With $years_experience years of experience in $field and a proven track record of $key_achievement, I am confident that I would be a valuable addition to your team.

In my previous role as $previous_position at $previous_company, I successfully $major_accomplishment. My expertise in $key_skills aligns perfectly with the requirements outlined in your job posting, particularly your need for someone with $required_skill experience.

What excites me most about this opportunity at $company_name is $company_interest. I am particularly drawn to $specific_interest and believe my background in $relevant_background would contribute significantly to your team's success.

I would welcome the opportunity to discuss how my experience and passion for $industry can benefit $company_name. Thank you for considering my application.

Sincerely,
$full_name""",

            'creative': """Hello $hiring_manager,

When I discovered the $position_title opening at $company_name, I knew I had found my next career adventure! With $years_experience years of experience turning $challenge_area into opportunities, I'm excited to bring my unique blend of $skill_combination to your innovative team.

At $previous_company, I didn't just $previous_responsibility – I $creative_achievement. This experience taught me that $lesson_learned, a philosophy that aligns perfectly with $company_name's commitment to $company_value.

What truly resonates with me about this role is $personal_connection. Your recent $company_news caught my attention because $why_interested. I'm eager to contribute my expertise in $expertise_area while growing alongside a team that values $team_value.

I'd love to chat more about how my unconventional approach to $approach_area could add fresh perspective to your $department team. 

Looking forward to connecting,
$full_name""",

            'technical': """Dear $hiring_manager,

I am applying for the $position_title position at $company_name, as advertised on $job_source. With $years_experience years of hands-on experience in $technical_field and a strong background in $technical_skills, I am well-positioned to contribute to your technical team.

Technical Highlights:
• $technical_achievement_1
• $technical_achievement_2  
• $technical_achievement_3

My experience with $technology_stack has prepared me to tackle the challenges mentioned in your job description, particularly $specific_challenge. At $previous_company, I $technical_project, resulting in $project_outcome.

I am particularly interested in $company_name because of your work in $technical_area. Your commitment to $technical_value aligns with my professional values and career objectives in $career_goal.

I would appreciate the opportunity to discuss how my technical expertise and problem-solving abilities can contribute to your team's continued success.

Best regards,
$full_name"""
        }
    
    def generate_cover_letter(self, 
                            user_data: Dict[str, Any], 
                            vacancy_data: Dict[str, Any], 
                            template_name: str = 'professional',
                            custom_template: Optional[str] = None) -> str:
        """
        Generate a personalized cover letter based on user data and vacancy information.
        
        Args:
            user_data: Dictionary containing applicant information
            vacancy_data: Dictionary containing job vacancy details
            template_name: Name of predefined template ('professional', 'creative', 'technical')
            custom_template: Optional custom template string with placeholders
            
        Returns:
            Generated cover letter as string
        """
        
        # Use custom template if provided, otherwise use predefined template
        if custom_template:
            template_str = custom_template
        elif template_name in self.templates:
            template_str = self.templates[template_name]
        else:
            raise ValueError(f"Template '{template_name}' not found. Available templates: {list(self.templates.keys())}")
        
        # Merge and process data
        merged_data = self._merge_and_process_data(user_data, vacancy_data)
        
        # Create template and substitute values
        template = Template(template_str)
        
        try:
            cover_letter = template.substitute(merged_data)
        except KeyError as e:
            missing_key = str(e).strip("'")
            raise ValueError(f"Missing required data field: {missing_key}")
        
        return self._clean_output(cover_letter)
    
    def _merge_and_process_data(self, user_data: Dict[str, Any], vacancy_data: Dict[str, Any]) -> Dict[str, str]:
        """Merge user data and vacancy data, applying smart defaults and processing."""
        
        # Start with user data
        merged = user_data.copy()
        
        # Add vacancy data
        merged.update(vacancy_data)
        
        # Apply smart defaults and processing
        processed_data = {
            # Basic user information
            'full_name': merged.get('full_name', merged.get('first_name', '') + ' ' + merged.get('last_name', '')).strip(),
            'email': merged.get('email', ''),
            'phone': merged.get('phone', ''),
            
            # Professional information
            'years_experience': str(merged.get('years_experience', merged.get('experience_years', 'several'))),
            'field': merged.get('field', merged.get('industry', 'my field')),
            'previous_position': merged.get('previous_position', merged.get('current_position', 'my previous role')),
            'previous_company': merged.get('previous_company', merged.get('current_company', 'my previous company')),
            
            # Job-specific information
            'position_title': merged.get('position_title', merged.get('job_title', 'this position')),
            'company_name': merged.get('company_name', merged.get('employer', 'your company')),
            'hiring_manager': self._format_hiring_manager(merged.get('hiring_manager')),
            'job_source': merged.get('job_source', 'your website'),
            
            # Skills and achievements
            'key_skills': merged.get('key_skills', merged.get('skills', 'relevant skills')),
            'key_achievement': merged.get('key_achievement', 'delivering successful results'),
            'major_accomplishment': merged.get('major_accomplishment', 'achieved significant results'),
            
            # Company-specific
            'company_interest': merged.get('company_interest', "your company's innovative approach"),
            'specific_interest': merged.get('specific_interest', 'your team\'s mission'),
            'company_value': merged.get('company_value', 'innovation'),
            'company_news': merged.get('company_news', 'recent developments'),
            
            # Technical fields
            'technical_field': merged.get('technical_field', merged.get('field', 'technology')),
            'technical_skills': merged.get('technical_skills', merged.get('key_skills', 'technical skills')),
            'technology_stack': merged.get('technology_stack', 'relevant technologies'),
            'technical_area': merged.get('technical_area', 'technology'),
            'technical_value': merged.get('technical_value', 'technical excellence'),
            
            # Dynamic content
            'industry': merged.get('industry', merged.get('field', 'this industry')),
            'department': merged.get('department', 'your'),
            'career_goal': merged.get('career_goal', 'professional development'),
            'date': datetime.now().strftime('%B %d, %Y')
        }
        
        # Handle technical achievements
        for i in range(1, 4):
            key = f'technical_achievement_{i}'
            processed_data[key] = merged.get(key, f'Technical achievement {i}')
        
        # Handle missing fields with context-appropriate defaults
        self._apply_contextual_defaults(processed_data, merged)
        
        # Ensure all fields exist as strings to prevent template errors
        for key, value in processed_data.items():
            if value is None:
                processed_data[key] = ''
            else:
                processed_data[key] = str(value)
        
        return processed_data
    
    def _format_hiring_manager(self, hiring_manager: Optional[str]) -> str:
        """Format hiring manager name or provide default."""
        if not hiring_manager:
            return "Hiring Manager"
        
        # If just a name is provided, add appropriate title
        if hiring_manager and ',' not in hiring_manager and 'Dear' not in hiring_manager:
            return f"Mr./Ms. {hiring_manager}"
        
        return hiring_manager
    
    def _apply_contextual_defaults(self, processed_data: Dict[str, str], original_data: Dict[str, Any]) -> None:
        """Apply contextual defaults based on available information."""
        
        # Infer missing fields from available data
        if 'required_skill' not in processed_data:
            processed_data['required_skill'] = processed_data['key_skills'].split(',')[0].strip()
        
        if 'relevant_background' not in processed_data:
            processed_data['relevant_background'] = processed_data['field']
        
        # Creative template specific fields
        processed_data.setdefault('challenge_area', 'challenges')
        processed_data.setdefault('skill_combination', 'technical and creative skills')
        processed_data.setdefault('creative_achievement', 'exceeded expectations')
        processed_data.setdefault('lesson_learned', 'collaboration drives innovation')
        processed_data.setdefault('personal_connection', 'the opportunity to make an impact')
        processed_data.setdefault('why_interested', 'it aligns with my professional goals')
        processed_data.setdefault('expertise_area', processed_data['field'])
        processed_data.setdefault('team_value', 'innovation and collaboration')
        processed_data.setdefault('approach_area', processed_data['field'])
        processed_data.setdefault('previous_responsibility', 'manage projects')
        
        # Technical template specific fields
        processed_data.setdefault('specific_challenge', 'technical challenges mentioned')
        processed_data.setdefault('technical_project', 'led a technical project')
        processed_data.setdefault('project_outcome', 'improved system performance')
    
    def _clean_output(self, text: str) -> str:
        """Clean up the generated cover letter."""
        # Remove extra whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Fix common formatting issues
        text = text.replace(' ,', ',')
        text = text.replace(' .', '.')
        text = text.replace('  ', ' ')
        
        return text.strip()
    
    def add_custom_template(self, name: str, template: str) -> None:
        """Add a new custom template to the generator."""
        self.templates[name] = template
    
    def list_templates(self) -> list:
        """Return list of available template names."""
        return list(self.templates.keys())
    
    def get_template_placeholders(self, template_name: str) -> list:
        """Get list of placeholders used in a specific template."""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template_str = self.templates[template_name]
        placeholders = re.findall(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', template_str)
        return list(set(placeholders))
    @staticmethod
    def export_cover_letter_to_pdf(content: str, filename="cover_letter.pdf"):
        # Set up the canvas with A4 size and custom margins
        c = canvas.Canvas(f'proposal/{filename}', pagesize=A4)
        width, height = A4

        # Define margins and boundary width
        margin = 0.5 * inch
        boundary_width = 5

        # Draw boundaries
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(boundary_width)
        c.line(margin, margin, margin, height - margin)
        c.line(width - margin, margin, width - margin, height - margin)

        # Calculate the text area's width
        text_area_width = width - (2 * margin) - (2 * boundary_width) - 20

        # Define a paragraph style for the content
        content_style = ParagraphStyle(
            'Normal',
            fontName='Helvetica',
            fontSize=12,
            leading=14,
            leftIndent=10,
            rightIndent=10,
        )

        # Create a Paragraph object from the content
        p = Paragraph(content.replace('\n', '<br/>'), content_style)

        # Use the drawOn method to place the paragraph within the canvas
        # The x and y coordinates here define the lower-left corner of the drawing area for the paragraph.
        p.wrapOn(c, text_area_width, height)
        p.drawOn(c, margin + boundary_width, height - margin - p.height)
        
        # Save the PDF
        c.save()
        print(f"Cover letter created as '{filename}'")


# Example usage and demonstration
def demo_cover_letter_generator():
    """Demonstrate the cover letter generator with sample data."""
    
    generator = CoverLetterGenerator()
    
    # Sample user data
    user_data = {
        'full_name': 'Jane Smith',
        'email': 'jane.smith@email.com',
        'phone': '+1-555-0123',
        'years_experience': 5,
        'field': 'software development',
        'previous_position': 'Senior Developer',
        'previous_company': 'Tech Innovations Inc.',
        'key_skills': 'Python, JavaScript, React, API development',
        'key_achievement': 'leading successful product launches',
        'major_accomplishment': 'reduced system response time by 40%',
        'industry': 'technology'
    }
    
    # Sample vacancy data
    vacancy_data = {
        'position_title': 'Full Stack Developer',
        'company_name': 'Future Systems Ltd.',
        'hiring_manager': 'Sarah Johnson',
        'job_source': 'LinkedIn',
        'required_skill': 'Python',
        'company_interest': "your company's commitment to innovative solutions",
        'specific_interest': 'your agile development practices',
        'department': 'engineering'
    }
    
    # Generate cover letters with different templates
    templates_to_demo = ['professional', 'creative', 'technical']
    for template in templates_to_demo:
        print(f"\n{'='*50}")
        print(f"COVER LETTER - {template.upper()} TEMPLATE")
        print(f"{'='*50}")
        
        try:
            cover_letter = generator.generate_cover_letter(
                user_data=user_data,
                vacancy_data=vacancy_data,
                template_name=template
            )
            
            print(cover_letter)
            generator.export_cover_letter_to_pdf(cover_letter, f"cover_letter_{template}.pdf")
        except Exception as e:
            print(f"Error generating {template} template: {e}")
    
    # Show template placeholders
    print(f"\n{'='*50}")
    print("TEMPLATE PLACEHOLDERS")
    print(f"{'='*50}")
    
    for template in generator.list_templates():
        placeholders = generator.get_template_placeholders(template)
        print(f"\n{template.upper()} template placeholders:")
        for placeholder in sorted(placeholders):
            print(f"  - {placeholder}")


if __name__ == "__main__":
    # Run the demo
    demo_cover_letter_generator()
    
    # Example of creating a custom template
    generator = CoverLetterGenerator()
    
    custom_template = """Dear $hiring_manager,

I am excited to apply for the $position_title role at $company_name. 
My $years_experience years in $field make me an ideal candidate.

Key qualifications:
- $key_achievement
- $major_accomplishment
- Expertise in $key_skills

I look forward to contributing to $company_name's success.

Best regards,
$full_name"""
    
    generator.add_custom_template('brief', custom_template)
    print(f"\nAvailable templates: {generator.list_templates()}")