from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
import os
import json
from datetime import datetime

class ResumeGenerator:
    def __init__(self, template_data=None):
        self.template_data = template_data or self.get_default_template()
        self.setup_styles()
    
    def get_default_template(self):
        """Default template with comprehensive fields"""
        return {
            "personal_info": {
                "full_name": "Valentino Noor Alam",
                "title": "Passionate Software Developer",
                "email": "ichikyube@email.com",
                "phone": "+61 XXX XXX XXX",
                "location": "Melbourne, VIC, Australia",
                "linkedin": "linkedin.com/in/rachit-sharma-0b9b44117",
                "github": "github.com/valentinoalam",
                "website": "www.tinokarya.com",
                "portfolio": "tinokarya.com/portfolio"
            },
            "career_objective": {
                "text": "Ambitious software developer with a strong foundation in Java, .NET, JavaScript, SQL, and C# and experience in full-stack development and backend integration. Seeking a challenging role in a dynamic team to apply technical skills and contribute to impactful projects, with a vision to grow as a technology expert and problem solver."
            },
            "skills": {
                "categories": [
                    {
                        "name": "Programming Languages",
                        "items": ["Java", "JavaScript", "C#", "Python", "C++", "PHP", "ASP.NET", "SQL", "HTML", "CSS", "TypeScript"]
                    },
                    {
                        "name": "Frameworks & Technologies", 
                        "items": [".NET Core", "React", "Node.js", "Spring Boot", "Angular", "RESTful API", "Bootstrap", "MVC", "DevOps"]
                    },
                    {
                        "name": "Database Management",
                        "items": ["SQL Server", "MongoDB", "PostgreSQL", "MySQL", "Redis", "Oracle"]
                    },
                    {
                        "name": "AI & Machine Learning",
                        "items": ["Prompt Engineering", "Open-source AI Server Maintenance", "TensorFlow", "scikit-learn"]
                    },
                    {
                        "name": "Tools & Platforms",
                        "items": ["AWS", "Docker", "GitHub", "Jira", "Jenkins", "Kubernetes", "Agile Methodologies"]
                    },
                    {
                        "name": "Soft Skills",
                        "items": ["Problem Solving", "Team Leadership", "Project Management", "Communication", "Mentoring"]
                    }
                ]
            },
            "education": [
                {
                    "degree": "Master of Business Analytics",
                    "institution": "Melbourne Institute of Technology",
                    "location": "Melbourne, VIC",
                    "dates": "Mar 2023 - Present",
                    "gpa": "3.8/4.0",
                    "relevant_coursework": ["Data Mining", "Statistical Analysis", "Machine Learning", "Business Intelligence"],
                    "achievements": ["Dean's List", "Graduate Research Assistant"]
                },
                {
                    "degree": "Bachelor of Computer Science Engineering",
                    "institution": "Alkademi University",
                    "location": "Indonesia",
                    "dates": "Mar 2015 - Nov 2019",
                    "gpa": "3.6/4.0",
                    "relevant_coursework": ["Web Development", "Database Systems", "Software Engineering", "Data Structures"],
                    "achievements": ["Department Topper in Web Development", "Tech Club President"]
                }
            ],
            "experience": [
                {
                    "title": "Software Developer",
                    "company": "Office Choice",
                    "location": "Melbourne, VIC",
                    "dates": "Jan 2024 – Oct 2024",
                    "employment_type": "Full-time",
                    "responsibilities": [
                        "Provided comprehensive technical support and maintenance for server and client-side applications, improving uptime by 25% and efficiency.",
                        "Developed comprehensive documentation and troubleshooting guides to enhance support consistency across the team, reducing resolution time by 40%.",
                        "Assisted in configuring network and endpoint security, promoting a secure IT environment and achieving 99.9% security compliance."
                    ],
                    "technologies": ["Java", "Spring Boot", ".NET", "SQL Server", "AWS"],
                    "achievements": ["Employee of the Month - June 2024", "Led migration project for 50+ applications"]
                },
                {
                    "title": "Software Developer",
                    "company": "Quinnox (Client: Kotak Mahindra Bank)",
                    "location": "Bangalore, Indonesia", 
                    "dates": "Jan 2020 - Dec 2022",
                    "employment_type": "Full-time",
                    "responsibilities": [
                        "Managed upgrade of Calypso from version 14.0.1 to 16.0.59, enhancing API functionality and streamlining client operations for 10,000+ users.",
                        "Implemented and maintained custom-client code updates, ensuring 100% compatibility with the upgraded Calypso libraries.",
                        "Developed and monitored DevOps pipelines for streamlined code deployment, reducing deployment time by 60% and service management within the client's distributed architecture."
                    ],
                    "technologies": ["Java", "Calypso", "Jenkins", "Docker", "Oracle DB"],
                    "achievements": ["Successfully delivered critical upgrade ahead of schedule", "Mentored 3 junior developers"]
                },
                {
                    "title": "Software Development Intern",
                    "company": "MIT Melbourne",
                    "location": "Melbourne, VIC",
                    "dates": "Jul 2023 – Nov 2023",
                    "employment_type": "Internship",
                    "responsibilities": [
                        "Collaborated within an Agile team to develop .NET applications using C#, .NET Core, and MVC frameworks, enhancing web application functionality and performance by 30%.",
                        "Implemented test-driven development (TDD) strategies, including unit testing, achieving 95% code coverage and ensuring reliable and scalable code.",
                        "Engaged in frontend development using HTML, CSS, JavaScript, and Bootstrap to create intuitive, responsive user interfaces used by 500+ students."
                    ],
                    "technologies": ["C#", ".NET Core", "JavaScript", "Bootstrap", "SQL Server"],
                    "achievements": ["Received excellent performance review", "Contributed to 3 major feature releases"]
                }
            ],
            "projects": [
                {
                    "name": "E-Commerce Platform",
                    "description": "Full-stack e-commerce solution with real-time inventory management",
                    "technologies": ["React", "Node.js", "MongoDB", "AWS"],
                    "dates": "Jan 2024 - Mar 2024",
                    "highlights": ["Handled 1000+ concurrent users", "Integrated payment gateway", "Real-time notifications"],
                    "github": "github.com/rachitsharma/ecommerce-platform"
                },
                {
                    "name": "AI-Powered Resume Analyzer",
                    "description": "Machine learning application to analyze and optimize resumes",
                    "technologies": ["Python", "TensorFlow", "Flask", "React"],
                    "dates": "Sep 2023 - Dec 2023",
                    "highlights": ["90% accuracy in skill matching", "Used by 200+ students", "Featured in university newsletter"],
                    "github": "github.com/rachitsharma/resume-analyzer"
                }
            ],
            "certifications": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "issuer": "Amazon Web Services",
                    "date": "2024",
                    "credential_id": "AWS-SAA-123456"
                },
                {
                    "name": "Microsoft Certified: Azure Developer Associate",
                    "issuer": "Microsoft",
                    "date": "2023",
                    "credential_id": "MS-AZ-789012"
                },
                {
                    "name": "Python Programming",
                    "issuer": "Udemy",
                    "date": "2020",
                    "credential_id": "UC-PYTHON-345"
                },
                {
                    "name": "SQL Fundamentals (Oracle 11g)",
                    "issuer": "NIIT Limited",
                    "date": "2017",
                    "credential_id": "NIIT-SQL-678"
                }
            ],
            "languages": [
                {"name": "English", "proficiency": "Native/Bilingual"},
                {"name": "Indonesi", "proficiency": "Native"},
                {"name": "Spanish", "proficiency": "Intermediate"}
            ],
            "volunteer_work": [
                {
                    "role": "Code Mentor",
                    "organization": "Code for Community",
                    "dates": "2022 - Present",
                    "description": "Mentor underprivileged students in programming fundamentals and career guidance"
                }
            ],
            "awards": [
                {
                    "name": "Best Innovation Award",
                    "issuer": "MIT Melbourne",
                    "date": "2023",
                    "description": "For developing AI-powered student assistance tool"
                },
                {
                    "name": "Outstanding Graduate",
                    "issuer": "S.R.M. University", 
                    "date": "2019",
                    "description": "Top 5% of graduating class"
                }
            ]
        }
    
    def setup_styles(self):
        """Setup enhanced styles for better visual appeal"""
        self.styles = getSampleStyleSheet()
        
        # Header styles
        self.name_style = ParagraphStyle(
            'NameStyle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2C3E50'),
            alignment=TA_CENTER,
            spaceAfter=2,
            fontName="Helvetica-Bold"
        )
        
        self.title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#34495E'),
            alignment=TA_CENTER,
            spaceAfter=8,
            fontName="Helvetica-Oblique"
        )
        
        self.contact_style = ParagraphStyle(
            'ContactStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            spaceAfter=2
        )
        
        # Section styles
        self.section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#2C3E50'),
            spaceBefore=12,
            spaceAfter=6,
            fontName="Helvetica-Bold",
            borderWidth=0,
            borderColor=colors.HexColor('#3498DB'),
            borderPadding=3,
            backColor=colors.HexColor('#ECF0F1')
        )
        
        self.body_style = ParagraphStyle(
            'BodyStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11,
            spaceAfter=4,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#2C3E50')
        )
        
        self.bullet_style = ParagraphStyle(
            'BulletStyle',
            parent=self.styles['BodyText'],
            bulletIndent=12,
            fontSize=9,
            leading=11,
            spaceAfter=3,
            leftIndent=20,
            textColor=colors.HexColor('#2C3E50')
        )
        
        self.job_title_style = ParagraphStyle(
            'JobTitleStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=2
        )
        
        self.company_style = ParagraphStyle(
            'CompanyStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#7F8C8D'),
            spaceAfter=4
        )

    def create_header(self):
        """Create enhanced header section"""
        elements = []
        personal = self.template_data['personal_info']
        
        # Name
        elements.append(Paragraph(personal['full_name'], self.name_style))
        
        # Title/Position
        elements.append(Paragraph(personal['title'], self.title_style))
        
        # Contact information in a more organized layout
        contact_info = []
        if personal.get('email'):
            contact_info.append(f"📧 {personal['email']}")
        if personal.get('phone'):
            contact_info.append(f"📞 {personal['phone']}")
        if personal.get('location'):
            contact_info.append(f"📍 {personal['location']}")
            
        elements.append(Paragraph(" | ".join(contact_info), self.contact_style))
        
        # Professional links
        links = []
        if personal.get('linkedin'):
            links.append(f"LinkedIn: {personal['linkedin']}")
        if personal.get('github'):
            links.append(f"GitHub: {personal['github']}")
        if personal.get('website'):
            links.append(f"Website: {personal['website']}")
            
        if links:
            elements.append(Paragraph(" | ".join(links), self.contact_style))
        
        # Decorative line
        elements.append(HRFlowable(
            width="100%", 
            thickness=2, 
            color=colors.HexColor('#3498DB'), 
            spaceBefore=8, 
            spaceAfter=8
        ))
        
        return elements

    def create_skills_section(self):
        """Create enhanced skills section with categories"""
        elements = []
        elements.append(Paragraph("CORE COMPETENCIES", self.section_header_style))
        
        skills_data = []
        for category in self.template_data['skills']['categories']:
            skills_text = ", ".join(category['items'])
            skills_data.append([
                Paragraph(f"<b>{category['name']}:</b>", self.body_style),
                Paragraph(skills_text, self.body_style)
            ])
        
        skills_table = Table(skills_data, colWidths=[2*inch, 4.5*inch])
        skills_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        elements.append(skills_table)
        elements.append(self.create_section_divider())
        return elements

    def create_experience_section(self):
        """Create enhanced experience section"""
        elements = []
        elements.append(Paragraph("PROFESSIONAL EXPERIENCE", self.section_header_style))
        
        for job in self.template_data['experience']:
            job_elements = []
            
            # Job title and company
            job_elements.append(Paragraph(
                f"<b>{job['title']}</b> — {job['company']}, {job['location']}", 
                self.job_title_style
            ))
            
            # Dates and employment type
            date_info = f"{job['dates']}"
            if job.get('employment_type'):
                date_info += f" | {job['employment_type']}"
            job_elements.append(Paragraph(date_info, self.company_style))
            
            # Technologies used
            if job.get('technologies'):
                tech_text = f"<b>Technologies:</b> {', '.join(job['technologies'])}"
                job_elements.append(Paragraph(tech_text, self.body_style))
            
            # Responsibilities
            for responsibility in job['responsibilities']:
                job_elements.append(Paragraph(f"• {responsibility}", self.bullet_style))
            
            # Key achievements
            if job.get('achievements'):
                job_elements.append(Paragraph("<b>Key Achievements:</b>", self.body_style))
                for achievement in job['achievements']:
                    job_elements.append(Paragraph(f"• {achievement}", self.bullet_style))
            
            # Keep job information together
            elements.append(KeepTogether(job_elements))
            elements.append(Spacer(1, 8))
        
        elements.append(self.create_section_divider())
        return elements

    def create_education_section(self):
        """Create enhanced education section"""
        elements = []
        elements.append(Paragraph("EDUCATION", self.section_header_style))
        
        for edu in self.template_data['education']:
            edu_elements = []
            
            # Degree and institution
            edu_elements.append(Paragraph(
                f"<b>{edu['degree']}</b>", 
                self.job_title_style
            ))
            
            institution_info = f"{edu['institution']}, {edu['location']} | {edu['dates']}"
            if edu.get('gpa'):
                institution_info += f" | GPA: {edu['gpa']}"
            edu_elements.append(Paragraph(institution_info, self.company_style))
            
            # Relevant coursework
            if edu.get('relevant_coursework'):
                coursework = ", ".join(edu['relevant_coursework'])
                edu_elements.append(Paragraph(f"<b>Relevant Coursework:</b> {coursework}", self.body_style))
            
            # Achievements
            if edu.get('achievements'):
                for achievement in edu['achievements']:
                    edu_elements.append(Paragraph(f"• {achievement}", self.bullet_style))
            
            elements.append(KeepTogether(edu_elements))
            elements.append(Spacer(1, 6))
        
        elements.append(self.create_section_divider())
        return elements

    def create_projects_section(self):
        """Create projects section"""
        if not self.template_data.get('projects'):
            return []
            
        elements = []
        elements.append(Paragraph("KEY PROJECTS", self.section_header_style))
        
        for project in self.template_data['projects']:
            project_elements = []
            
            # Project name and dates
            project_elements.append(Paragraph(
                f"<b>{project['name']}</b> | {project['dates']}", 
                self.job_title_style
            ))
            
            # Description
            project_elements.append(Paragraph(project['description'], self.body_style))
            
            # Technologies
            if project.get('technologies'):
                tech_text = f"<b>Technologies:</b> {', '.join(project['technologies'])}"
                project_elements.append(Paragraph(tech_text, self.body_style))
            
            # Highlights
            if project.get('highlights'):
                for highlight in project['highlights']:
                    project_elements.append(Paragraph(f"• {highlight}", self.bullet_style))
            
            # GitHub link
            if project.get('github'):
                project_elements.append(Paragraph(f"<b>Repository:</b> {project['github']}", self.body_style))
            
            elements.append(KeepTogether(project_elements))
            elements.append(Spacer(1, 6))
        
        elements.append(self.create_section_divider())
        return elements

    def create_certifications_section(self):
        """Create enhanced certifications section"""
        elements = []
        elements.append(Paragraph("CERTIFICATIONS", self.section_header_style))
        
        cert_data = []
        for cert in self.template_data['certifications']:
            cert_info = f"<b>{cert['name']}</b> - {cert['issuer']} ({cert['date']})"
            if cert.get('credential_id'):
                cert_info += f" | ID: {cert['credential_id']}"
            cert_data.append([Paragraph(f"• {cert_info}", self.bullet_style)])
        
        if cert_data:
            cert_table = Table(cert_data, colWidths=[6.5*inch])
            cert_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ]))
            elements.append(cert_table)
        
        elements.append(self.create_section_divider())
        return elements

    def create_additional_sections(self):
        """Create additional sections like languages, volunteer work, awards"""
        elements = []
        
        # Languages
        if self.template_data.get('languages'):
            elements.append(Paragraph("LANGUAGES", self.section_header_style))
            lang_text = " | ".join([f"{lang['name']} ({lang['proficiency']})" 
                                   for lang in self.template_data['languages']])
            elements.append(Paragraph(lang_text, self.body_style))
            elements.append(Spacer(1, 6))
        
        # Awards
        if self.template_data.get('awards'):
            elements.append(Paragraph("AWARDS & RECOGNITION", self.section_header_style))
            for award in self.template_data['awards']:
                award_text = f"<b>{award['name']}</b> - {award['issuer']} ({award['date']})"
                if award.get('description'):
                    award_text += f" | {award['description']}"
                elements.append(Paragraph(f"• {award_text}", self.bullet_style))
            elements.append(Spacer(1, 6))
        
        # Volunteer Work
        if self.template_data.get('volunteer_work'):
            elements.append(Paragraph("VOLUNTEER EXPERIENCE", self.section_header_style))
            for vol in self.template_data['volunteer_work']:
                vol_text = f"<b>{vol['role']}</b> - {vol['organization']} ({vol['dates']})"
                elements.append(Paragraph(vol_text, self.job_title_style))
                elements.append(Paragraph(vol['description'], self.body_style))
                elements.append(Spacer(1, 4))
        
        return elements

    def create_section_divider(self):
        """Create a subtle section divider"""
        return HRFlowable(
            width="100%", 
            thickness=0.5, 
            color=colors.HexColor('#BDC3C7'), 
            spaceBefore=8, 
            spaceAfter=8
        )

    def create_objective_section(self):
        """Create career objective section"""
        elements = []
        if self.template_data.get('career_objective'):
            elements.append(Paragraph("CAREER OBJECTIVE", self.section_header_style))
            elements.append(Paragraph(self.template_data['career_objective']['text'], self.body_style))
            elements.append(self.create_section_divider())
        return elements

    def add_page_border(self, canvas, doc):
        """Add elegant page border"""
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#3498DB'))
        canvas.setLineWidth(2)
        canvas.rect(10, 10, A4[0] - 20, A4[1] - 20)
        
        # Add a subtle inner border
        canvas.setStrokeColor(colors.HexColor('#ECF0F1'))
        canvas.setLineWidth(1)
        canvas.rect(15, 15, A4[0] - 30, A4[1] - 30)
        canvas.restoreState()

    def generate_pdf(self, output_path):
        """Generate the complete PDF resume"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Remove existing file
        if os.path.exists(output_path):
            os.remove(output_path)
        
        # Create PDF with better margins
        pdf = SimpleDocTemplate(
            output_path, 
            pagesize=A4, 
            leftMargin=0.75*inch, 
            rightMargin=0.75*inch, 
            topMargin=0.75*inch, 
            bottomMargin=0.75*inch
        )
        
        # Build document elements
        elements = []
        elements.extend(self.create_header())
        elements.extend(self.create_objective_section())
        elements.extend(self.create_skills_section())
        elements.extend(self.create_experience_section())
        elements.extend(self.create_education_section())
        elements.extend(self.create_projects_section())
        elements.extend(self.create_certifications_section())
        elements.extend(self.create_additional_sections())
        
        # Generate PDF
        pdf.build(elements, onFirstPage=self.add_page_border, onLaterPages=self.add_page_border)
        print(f"Enhanced PDF resume created successfully at: {output_path}")

    @classmethod
    def load_from_json(cls, json_file_path):
        """Load resume data from JSON file"""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        return cls(template_data)

    def save_template_to_json(self, json_file_path):
        """Save current template to JSON file"""
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.template_data, f, indent=4, ensure_ascii=False)
        print(f"Template saved to: {json_file_path}")

# Usage example
if __name__ == "__main__":
    # Define paths
    output_directory = r"E:\1landing\resume\UPDATED"
    pdf_filename = "Valentino_Resume.pdf"
    template_filename = "resume_template.json"
    
    pdf_path = os.path.join(output_directory, pdf_filename)
    template_path = os.path.join(output_directory, template_filename)
    
    # Create resume generator
    generator = ResumeGenerator()
    
    # Save template for future editing
    generator.save_template_to_json(template_path)
    
    # Generate PDF
    generator.generate_pdf(pdf_path)
    
    print("\n" + "="*50)
    print("RESUME GENERATION COMPLETE!")
    print("="*50)
    print(f"PDF Resume: {pdf_path}")
    print(f"JSON Template: {template_path}")
    print("\nTo customize your resume:")
    print("1. Edit the JSON template file")
    print("2. Load it using: ResumeGenerator.load_from_json(template_path)")
    print("3. Generate a new PDF")