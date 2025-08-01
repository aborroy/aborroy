# update_readme.py
import os
import json
import requests
from datetime import datetime, timedelta
from jinja2 import Template
from dateutil import parser

def get_github_repos(username, token):
    """Fetch all public repositories for a user"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    repos = []
    page = 1
    
    while True:
        url = f'https://api.github.com/users/{username}/repos?per_page=100&page={page}&sort=updated&direction=desc'
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}")
            break
            
        page_repos = response.json()
        if not page_repos:
            break
            
        repos.extend(page_repos)
        page += 1
    
    return repos

def categorize_repositories(repos):
    """Categorize repositories based on topics and names"""
    categories = {
        'ai_ml': {
            'title': 'AI & Machine Learning',
            'keywords': ['ai', 'ml', 'spring-ai', 'llm', 'genai', 'summarizer', 'openai', 'ollama'],
            'repos': []
        },
        'docker_devops': {
            'title': 'Docker & DevOps',
            'keywords': ['docker', 'kubernetes', 'k8s', 'container', 'devops', 'sbom', 'helm'],
            'repos': []
        },
        'alfresco': {
            'title': 'Alfresco Extensions & Tools',
            'keywords': ['alfresco', 'alf-', 'tengine', 'share', 'content-model'],
            'repos': []
        },
        'api_integration': {
            'title': 'API & Integration',
            'keywords': ['api', 'connector', 'integration', 'mcp', 'gateway', 'hyland'],
            'repos': []
        },
        'tools_utilities': {
            'title': 'Tools & Utilities',
            'keywords': ['tool', 'utility', 'generator', 'extractor', 'installer'],
            'repos': []
        },
        'educational': {
            'title': 'Educational & Samples',
            'keywords': ['tutorial', 'sample', 'demo', 'training', 'example', 'poc'],
            'repos': []
        }
    }
    
    # Filter out forks and categorize
    for repo in repos:
        if repo['fork']:
            continue
            
        repo_name = repo['name'].lower()
        repo_topics = [topic.lower() for topic in repo.get('topics', [])]
        repo_description = (repo.get('description') or '').lower()
        
        categorized = False
        
        # Check each category
        for cat_key, category in categories.items():
            for keyword in category['keywords']:
                if (keyword in repo_name or 
                    keyword in repo_topics or 
                    keyword in repo_description):
                    category['repos'].append(repo)
                    categorized = True
                    break
            if categorized:
                break
        
        # If not categorized, add to tools & utilities
        if not categorized:
            categories['tools_utilities']['repos'].append(repo)
    
    return categories

def get_recent_activity(repos, days=90):
    """Get repositories updated in the last N days"""
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_repos = []
    
    for repo in repos:
        if repo['fork']:
            continue
            
        updated_at = parser.parse(repo['updated_at']).replace(tzinfo=None)
        if updated_at > cutoff_date:
            recent_repos.append({
                'name': repo['name'],
                'description': repo.get('description', 'No description'),
                'html_url': repo['html_url'],
                'updated_at': updated_at.strftime('%Y-%m-%d'),
                'language': repo.get('language', 'N/A'),
                'stars': repo['stargazers_count']
            })
    
    return sorted(recent_repos, key=lambda x: x['updated_at'], reverse=True)[:10]

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default configuration
        return {
            "personal_info": {
                "name": "Angel Borroy",
                "title": "Developer Evangelist @ Hyland Software | Docker Captain",
                "location": "Spain",
                "website": "https://connect.hyland.com/",
                "social": {
                    "twitter": "@AngelBorroy", 
                    "linkedin": "in/angelborroy",
                    "youtube": "c/AngelBorroy",
                    "bluesky": "@angelborroy.bsky.social"
                }
            },
            "featured_repos": [
                "alfresco-ai-framework",
                "alfresco-sbom-generator", 
                "alf-k8s",
                "spring-ai-summarizer"
            ],
            "technologies": [
                "Java", "Python", "JavaScript", "Go", "Shell/Bash",
                "Docker", "Kubernetes", "Alfresco", "Spring Framework",
                "Spring AI", "Ollama", "OpenAI", "Various LLMs"
            ]
        }

def main():
    username = os.environ.get('USERNAME', 'aborroy')
    token = os.environ.get('GITHUB_TOKEN')
    
    if not token:
        print("GITHUB_TOKEN environment variable is required")
        return
    
    print(f"Fetching repositories for {username}...")
    repos = get_github_repos(username, token)
    
    print(f"Found {len(repos)} repositories")
    
    # Categorize repositories
    categories = categorize_repositories(repos)
    
    # Get recent activity
    recent_activity = get_recent_activity(repos)
    
    # Load configuration
    config = load_config()
    
    # Load template
    with open('template.md', 'r') as f:
        template_content = f.read()
    
    # Configure Jinja2 to trim blocks and remove extra whitespace
    template = Template(template_content, trim_blocks=True, lstrip_blocks=True)
    
    # Generate README content
    readme_content = template.render(
        config=config,
        categories=categories,
        recent_activity=recent_activity,
        total_repos=len([r for r in repos if not r['fork']]),
        last_updated=datetime.now().strftime('%Y-%m-%d %H:%M UTC')
    )
    
    # Clean up excessive empty lines (replace 3+ consecutive newlines with 2)
    import re
    readme_content = re.sub(r'\n{3,}', '\n\n', readme_content)
    
    # Write README.md
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("README.md updated successfully!")

if __name__ == "__main__":
    main()