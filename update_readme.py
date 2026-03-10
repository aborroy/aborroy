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
    """Categorize repositories based on topics and names.
    
    Categories are ordered to prioritize broader, technology-focused groupings.
    Repos are matched to the FIRST category whose keywords match, so order matters:
    AI/RAG first (most distinctive), then MCP/Agents, Docker, Search, and finally
    the Alfresco catch-all for platform-specific tooling.
    """
    categories = {
        'ai_rag': {
            'title': 'AI / RAG / LLM',
            'keywords': ['ai', 'ml', 'spring-ai', 'llm', 'genai', 'summarizer', 'openai', 'ollama', 'rag', 'content-lake', 'e2b', 'embedding'],
            'repos': []
        },
        'mcp_agents': {
            'title': 'MCP Servers & Agents',
            'keywords': ['mcp', 'agent', 'mesh'],
            'repos': []
        },
        'docker_k8s': {
            'title': 'Docker & Kubernetes',
            'keywords': ['docker', 'kubernetes', 'k8s', 'container', 'helm', 'installer', 'sbom'],
            'repos': []
        },
        'search': {
            'title': 'Search (Solr / OpenSearch)',
            'keywords': ['solr', 'opensearch', 'search', 'neural-search', 'replication'],
            'repos': []
        },
        'alfresco': {
            'title': 'Alfresco Ecosystem',
            'keywords': ['alfresco', 'alf-', 'tengine', 'share', 'content-model', 'hyland'],
            'repos': []
        },
        'other': {
            'title': 'Other Projects',
            'keywords': [],
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
        
        # Check each category (order matters — first match wins)
        for cat_key, category in categories.items():
            if cat_key == 'other':
                continue
            for keyword in category['keywords']:
                if (keyword in repo_name or 
                    keyword in repo_topics or 
                    keyword in repo_description):
                    category['repos'].append(repo)
                    categorized = True
                    break
            if categorized:
                break
        
        # If not categorized, add to other
        if not categorized:
            categories['other']['repos'].append(repo)
    
    # Sort repos within each category by stars (descending)
    for cat_key, category in categories.items():
        category['repos'].sort(key=lambda r: r['stargazers_count'], reverse=True)
    
    # Remove empty categories
    categories = {k: v for k, v in categories.items() if v['repos']}
    
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
        return {
            "personal_info": {
                "name": "Angel Borroy",
                "title": "Docker Captain | Java · Spring AI · RAG · Open Source | Cryptography & Cybersecurity Lecturer",
                "location": "Spain",
                "website": "https://angelborroy.wordpress.com/category/english/",
                "social": {
                    "twitter": "@AngelBorroy", 
                    "linkedin": "in/angelborroy",
                    "youtube": "c/AngelBorroy",
                    "bluesky": "@angelborroy.bsky.social"
                }
            },
            "featured_repos": [
                "alfresco-genai",
                "spring-ai-summarizer",
                "simple-alfresco-agent-mesh",
                "alfresco-content-lake"
            ],
            "technologies": [
                "Java", "Spring AI", "Python", "RAG / Vector Search",
                "Docker", "Kubernetes", "MCP Servers", "OpenSearch / Solr",
                "Go", "Shell/Bash", "JavaScript / TypeScript",
                "Ollama / vLLM", "Cryptography", "Alfresco / Content Management"
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
    config = load_config()
    recent_activity = get_recent_activity(repos, config.get('recent_activity_days', 90))
    
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
    
    # Print category summary
    for cat_key, category in categories.items():
        print(f"  {category['title']}: {len(category['repos'])} repos")

if __name__ == "__main__":
    main()
