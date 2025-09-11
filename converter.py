import json
import os
from pathlib import Path

def create_row(item):
    """Create a table row for a job item"""
    return f"""
    <tr>
        <td>{item['company']}</td>
        <td>{item['designation']}</td>
        <td>{item['location']}</td>
        <td>{item['salary']}</td>
        <td><button class="apply-button" onclick="location.href='{item['link']}'" type="button">Apply</button></td>
    </tr>
    """

def create_table(rows):
    """Create the complete HTML table"""
    return f"""
    <table>
        <tr>
            <th>Company</th>
            <th>Role</th>
            <th>Location</th>
            <th>Salary</th>
            <th>Apply</th>
        </tr>
        {rows}
    </table>
    """

def create_html(table):
    """Create the complete HTML document"""
    return f"""
    <html>
        <head>
        <style>
            table {{
                width: 100%;
            }}
            tr {{
                text-align: left;
                border: 1px solid black;
            }}
            th, td {{
                padding: 15px;
            }}
            tr:nth-child(odd) {{
                background: #CCC
            }}
            tr:nth-child(even) {{
                background: #FFF
            }}
            .no-content {{
                background-color: red;
            }}
            .apply-button {{
                padding: 11px;
            }}
        </style>
        </head>
        <body>
        {table}
        </body>
    </html>
    """

def converter():
    """Main converter function"""
    try:
        # Get current directory and build paths
        current_dir = Path(__file__).parent
        jobs_file = current_dir / "jobs.json"
        html_file = current_dir / "jobSearch.html"
        
        # Remove old HTML file if it exists
        if html_file.exists():
            print('Deleting old build file')
            html_file.unlink()
        
        # Read job data
        with open(jobs_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Generate HTML
        rows = ''.join(create_row(item) for item in data)
        table = create_table(rows)
        html = create_html(table)
        
        # Write HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print('Successfully created an HTML table')
        
    except Exception as error:
        print(f'Error generating table: {error}')

if __name__ == "__main__":
    converter()
