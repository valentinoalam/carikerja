import requests
import json
import time
from datetime import datetime
import google.generativeai as genai

# Configuration
ACCESS_TOKEN = ""
BASE_URL = "https://www.freelancer.com/api"
GOOGLE_API_KEY = "AIzaSyDmipzIwjethZEEPOQFZG0edrBsTTDImr0"

genai.configure(api_key=GOOGLE_API_KEY)

# Dictionary to store project details temporarily
project_details = {}

def fetch_jobs():
    """Fetch active jobs based on criteria"""
    url = f"{BASE_URL}/projects/0.1/projects/active/"
    
    params = {
        "compact": "",
        "limit": 5,
        "project_types[]": "hourly",
        "max_avg_price": 10,
        "min_avg_price": 100,
        "query": "web development"
    }
    
    headers = {
        "freelancer-oauth-v1": ACCESS_TOKEN
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data.get('status') == 'success':
            projects = data.get('result', {}).get('projects', [])
            print(f"\nFound {len(projects)} projects:")
            for project in projects:
                # Store project details temporarily
                project_details[project.get('id')] = {
                    'title': project.get('title'),
                    'type': project.get('type'),
                    'budget': project.get('budget', {}),
                    'jobs': project.get('data', {}).get('jobs', []),
                    'full_description': project.get('full_description'),
                    'preview_description': project.get('preview_description')
                }
                
                print(f"\nProject ID: {project.get('id')}")
                print(f"Title: {project.get('title')}")
                print(f"Budget: ${project.get('budget', {}).get('minimum')} - ${project.get('budget', {}).get('maximum')}")
                print(f"Full Description: {project.get('full_description')}")
                print(f"Preview Description: {project.get('preview_description')}")
            return projects
        else:
            print("No projects found or API error")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs: {e}")
        return []


def place_bid(project_id, amount, period=7):
    """Place a bid on a project"""
    url = f"{BASE_URL}/projects/0.1/bids/"
    
    headers = {
        "content-type": "application/json",
        "freelancer-oauth-v1": ACCESS_TOKEN
    }
    
    try:
        # Get project details from the stored dictionary
        project = project_details.get(project_id)
        if not project:
            print(f"Error: Project details not found for ID {project_id}")
            return False
        
        # Generate proposal using Gemini API
        prompt = f"""
        Write a short and professional proposal for a Freelancer.com project using the following details:

        Project Title: {project['title']}

        Project Type: {project['type']}

        Budget Range: ${project['budget']['minimum']} - ${project['budget']['maximum']}

        Required Skills: {', '.join(project['jobs'])}

        Project Description: {project['full_description']}, {project['preview_description']}

        The proposal should:

        Be concise and tailored to the client's specific problem and project goals

        Demonstrate understanding of the client’s needs without repeating the description verbatim

        Use a professional yet friendly tone

        Mention relevant experience or previous projects (you can use examples like Terra Virtua or Zaproxy if relevant)

        Emphasize how the proposed solution solves the client's challenge effectively

        Avoid generic phrases and fluff
        - Reference the **actual experience and stack below only** (do not modify or add to this):


        Fixed Experience and Stack to Use (when relevant):
        - **5+ years of experience** in the software industry  
        - **Tech Stack:** ReactJS (frontend), ExpressJS (backend), AWS (deployment)
        - **Project 1: Terra Virtua** — Full-stack developer on a blockchain marketplace  
        https://marketplace.virtua.com/
        - **Project 2: Zaproxy** — Contributor to security tool with 13,400+ stars  
        https://github.com/zaproxy/zaproxy

        Optionally include:

            A short money-back/quality guarantee

            An incentive for ongoing collaboration

            A free consultation offer

        Important:
        - Do not copy or restate the project description
        - Focus on clarity, relevance, and value
        - Assume this bid is written personally, not by a bot
        - Keep the proposal within 150–200 words
        - Don't use any placeholders for example [Your Name]
        - Finish the proposal with my name which is Najam Ul Saqib
        - Start each proposal with "In a sea of AI-generated and bot written bids, this one is written by human for you, so I wasn’t as fast as the bot but I made sure I read your project, understood it and then place the bid"
        """

        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generate response
        response = model.generate_content(prompt)
        proposal_text = response.text
        print(f'Generated proposal: {proposal_text}')
        
        # Save the proposal to file
        with open("generated_proposal.txt", "w") as f:
            f.write(proposal_text)
            
        # Get your user ID
        user_url = f"{BASE_URL}/users/0.1/self/"
        user_response = requests.get(user_url, headers=headers)
        user_data = user_response.json()
        bidder_id = user_data.get('result', {}).get('id')
        
        # Create bid data
        bid_data = {
            "project_id": project_id,
            "bidder_id": bidder_id,
            "amount": amount,
            "period": period,
            "description": proposal_text,
            "currency_id": 1,
            "milestone_percentage": 100
        }
        
        # Place the bid
        response = requests.post(url, headers=headers, json=bid_data)
        response.raise_for_status()
        
        # Clean up project details after successful bid
        if response.status_code == 200:
            del project_details[project_id]
            
        print(f"\nBid placed successfully!")
        print(f"Project ID: {project_id}")
        print(f"Amount: ${amount}")
        print(f"Period: {period} days")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error placing bid: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return False

def main():
    # Step 1: Fetch jobs
    print("Fetching jobs...")
    projects = fetch_jobs()
    
    if not projects:
        print("No projects found to bid on")
        return
    
    # Step 3: Place bids on projects
    successful_bid = False
    for project in projects:
        if successful_bid:
            break  # Stop after first successful bid
            
        project_id = project.get('id')
        budget_min = project.get('budget', {}).get('minimum', 250)
        
        print(f"\nPlacing bid on project: {project.get('title')}")
        success = place_bid(project_id, budget_min)
        
        if success:
            print(f"Successfully bid on project {project_id}")
            successful_bid = True
        else:
            print(f"Failed to bid on project {project_id}")
        
        # Add a delay between bids to avoid rate limiting
        time.sleep(2)

if __name__ == "__main__":
    main() 