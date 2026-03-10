# Hi, I'm {{ config.personal_info.name }}

**{{ config.personal_info.title }}**

I build AI-powered tools, semantic search pipelines, containerized architectures, and open source developer utilities. My work spans RAG systems with Spring AI and vector databases, MCP servers, Docker-based deployment tooling, and content management extensions. I also teach cryptography and cybersecurity at [Universidad San Jorge](https://usj.es) in Zaragoza.

## What I Do

- **AI & RAG Pipelines**: Semantic search, retrieval-augmented generation, and LLM integration with Spring AI, vector databases, and embedding models
- **MCP Servers & Agents**: Building Model Context Protocol servers for AI-powered workflows
- **Docker & Cloud-Native**: Containerized architectures, Kubernetes deployments, and developer tooling — [Docker Captain](https://www.docker.com/captains/) since 2020
- **Open Source**: {{ total_repos }}+ public repositories, transform engines, search integrations, and developer utilities
- **Teaching**: Cryptography and cybersecurity lecturer — Enigma machine implementation, CTF challenges, and hands-on workshops ([enigma-python](https://github.com/angelborroy/enigma-python))

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

## Talks & Writing

- [Blog — "Programming and So"]({{ config.personal_info.website }}) — Technical posts on Java, Docker, AI/RAG, and open source
- [Hyland Developer Blog](https://connect.hyland.com/t5/alfresco-blog/bg-p/alfresco1blog-board) — Alfresco ecosystem articles
- [YouTube](https://www.youtube.com/{{ config.personal_info.social.youtube }}) — Tech Talk Live sessions and tutorials

## Repository Categories

{% for cat_key, category in categories.items() %}
{% if category.repos %}
### {{ category.title }}

{% for repo in category.repos[:config.max_repos_per_category|default(5)] %}
- **[{{ repo.name }}]({{ repo.html_url }})** {% if repo.stargazers_count > 0 %}⭐{{ repo.stargazers_count }}{% endif %}{% if repo.language %} `{{ repo.language }}`{% endif %} - {{ repo.description or "No description available" }}
{% endfor %}
{% if category.repos|length > config.max_repos_per_category|default(5) %}
  *...and {{ category.repos|length - config.max_repos_per_category|default(5) }} more repositories in this category*
{% endif %}

{% endif %}
{% endfor %}

## Recent Activity

{% for repo in recent_activity %}
- **[{{ repo.name }}]({{ repo.html_url }})** - {{ repo.description[:80] }}{% if repo.description|length > 80 %}...{% endif %} *(Updated: {{ repo.updated_at }})*
{% endfor %}

## Technologies & Tools

{{ config.technologies | join(' · ') }}

## Other Accounts

More of my work lives at [angelborroy](https://github.com/angelborroy) and [angelborroy-ks](https://github.com/angelborroy-ks).

## Let's Connect

- **Blog**: [{{ config.personal_info.website }}]({{ config.personal_info.website }})
- **Twitter**: [{{ config.personal_info.social.twitter }}](https://twitter.com/{{ config.personal_info.social.twitter.lstrip('@') }})
- **LinkedIn**: [{{ config.personal_info.social.linkedin }}](https://www.linkedin.com/{{ config.personal_info.social.linkedin }})
- **YouTube**: [{{ config.personal_info.social.youtube }}](https://www.youtube.com/{{ config.personal_info.social.youtube }})
- **Bluesky**: [{{ config.personal_info.social.bluesky }}](https://bsky.app/profile/{{ config.personal_info.social.bluesky.lstrip('@') }})

---

*Last updated: {{ last_updated }}*

<!-- This README is automatically updated by GitHub Actions -->
