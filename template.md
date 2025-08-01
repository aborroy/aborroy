# Hi there! I'm {{ config.personal_info.name }}

**{{ config.personal_info.title }}**

Welcome to my GitHub! I'm passionate about helping developers build better content management solutions, containerized applications, and AI-powered tools. Here you'll find my contributions to the Alfresco ecosystem, Docker utilities, and innovative AI integrations.

## What I Do

- **Developer Evangelism**: Helping developers succeed with Hyland Software solutions
- **Docker Technologies**: Creating tools and best practices for containerized deployments
- **Content Management**: Extending Alfresco with custom transformers, connectors, and frameworks
- **AI Integration**: Building bridges between AI services and content management systems

## Quick Stats

- **{{ total_repos }}** public repositories
- Active in **{{ categories|length }}** different technology areas
- Based in {{ config.personal_info.location }}
- Last updated: {{ last_updated }}

## Featured Projects

{% set featured_found = [] %}
{% for repo_name in config.featured_repos %}
  {% for cat_key, category in categories.items() %}
    {% for repo in category.repos %}
      {% if repo.name == repo_name %}
        {% set _ = featured_found.append(repo) %}
      {% endif %}
    {% endfor %}
  {% endfor %}
{% endfor %}

{% for repo in featured_found %}
- **[{{ repo.name }}]({{ repo.html_url }})** {% if repo.stargazers_count > 0 %}⭐{{ repo.stargazers_count }}{% endif %} - {{ repo.description or "No description available" }}
{% endfor %}

## Repository Categories

{% for cat_key, category in categories.items() %}
{% if category.repos %}
### {{ category.title }}

{% for repo in category.repos[:8] %}
- **[{{ repo.name }}]({{ repo.html_url }})** {% if repo.stargazers_count > 0 %}⭐{{ repo.stargazers_count }}{% endif %}{% if repo.language %} `{{ repo.language }}`{% endif %} - {{ repo.description or "No description available" }}
{% endfor %}
{% if category.repos|length > 8 %}
*...and {{ category.repos|length - 8 }} more repositories in this category*
{% endif %}

{% endif %}
{% endfor %}

## Recent Activity

{% for repo in recent_activity %}
- **[{{ repo.name }}]({{ repo.html_url }})** - {{ repo.description[:80] }}{% if repo.description|length > 80 %}...{% endif %} *(Updated: {{ repo.updated_at }})*
{% endfor %}

## Technologies & Tools

{{ config.technologies | join(', ') }}

## Let's Connect!

- **Website**: [{{ config.personal_info.website }}]({{ config.personal_info.website }})
- **Twitter**: [{{ config.personal_info.social.twitter }}](https://twitter.com/{{ config.personal_info.social.twitter.lstrip('@') }})
- **LinkedIn**: [{{ config.personal_info.social.linkedin }}](https://www.linkedin.com/{{ config.personal_info.social.linkedin }})
- **YouTube**: [{{ config.personal_info.social.youtube }}](https://www.youtube.com/{{ config.personal_info.social.youtube }})
- **Bluesky**: [{{ config.personal_info.social.bluesky }}](https://bsky.app/profile/{{ config.personal_info.social.bluesky.lstrip('@') }})

## Contributing

I welcome contributions, questions, and discussions! Feel free to:
- Open issues on any repository
- Submit pull requests
- Reach out for collaboration opportunities
- Ask questions about Alfresco, Docker, or AI integrations

---

*"Helping developers build better content management solutions, one repository at a time."*

<!-- This README is automatically updated by GitHub Actions -->