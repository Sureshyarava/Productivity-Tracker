import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Jira Configuration
    JIRA_URL = os.getenv('JIRA_URL', '')
    JIRA_EMAIL = os.getenv('JIRA_EMAIL', '')
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN', '')
    JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY', '')
    
    # GitLab Configuration
    GITLAB_URL = os.getenv('GITLAB_URL', 'https://gitlab.com')
    GITLAB_TOKEN = os.getenv('GITLAB_TOKEN', '')
    GITLAB_PROJECT_IDS = os.getenv('GITLAB_PROJECT_IDS', '').split(',') if os.getenv('GITLAB_PROJECT_IDS') else []
    
    # Confluence Configuration
    CONFLUENCE_URL = os.getenv('CONFLUENCE_URL', '')
    CONFLUENCE_EMAIL = os.getenv('CONFLUENCE_EMAIL', '')
    CONFLUENCE_API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN', '')
    CONFLUENCE_SPACE_KEY = os.getenv('CONFLUENCE_SPACE_KEY', '')
    
    # Team Configuration
    TEAMS = os.getenv('TEAMS', 'Team Alpha,Team Beta,Team Gamma').split(',')
    
    # Cache Configuration
    CACHE_EXPIRY = int(os.getenv('CACHE_EXPIRY', '300'))
    
    # Use mock data if APIs not configured
    USE_MOCK_DATA = not all([JIRA_URL, JIRA_API_TOKEN, GITLAB_TOKEN])

config = Config()
