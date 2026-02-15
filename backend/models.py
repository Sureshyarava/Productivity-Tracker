import json
import os
from config import config

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_DATA_FILE = os.path.join(BASE_DIR, 'mock_data.json')

# Team members
TEAM_MEMBERS = [
    'Alice Johnson',
    'Bob Smith',
    'Charlie Davis',
    'Diana Martinez',
    'Eve Chen',
    'Frank Wilson'
]

def load_mock_data():
    """Load mock data from JSON file"""
    try:
        with open(MOCK_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'user_stories': [],
            'pull_requests': [],
            'testing': [],
            'prod_support': [],
            'prod_issues': []
        }
    except json.JSONDecodeError:
        return {
            'user_stories': [],
            'pull_requests': [],
            'testing': [],
            'prod_support': [],
            'prod_issues': []
        }

def load_real_data():
    """Load data from Jira, GitLab, and Confluence APIs"""
    from jira_integration import jira_integration
    from gitlab_integration import gitlab_integration
    
    data = {
        'user_stories': [],
        'pull_requests': [],
        'testing': [],
        'prod_support': [],
        'prod_issues': []
    }
    
    # Load user stories from Jira
    if jira_integration.enabled:
        data['user_stories'] = jira_integration.get_user_stories()
    
    # Load merge requests (pull requests) from GitLab
    if gitlab_integration.enabled:
        data['pull_requests'] = gitlab_integration.get_merge_requests()
    
    # Load testing activities from Jira
    if jira_integration.enabled:
        data['testing'] = jira_integration.get_testing_activities()
    
    # Load support tickets from Jira
    if jira_integration.enabled:
        data['prod_support'] = jira_integration.get_support_tickets()
    
    # Load production issues from Jira
    if jira_integration.enabled:
        data['prod_issues'] = jira_integration.get_production_issues()
    
    return data

def generate_fake_data():
    """Load data from APIs or JSON file based on configuration"""
    if config.USE_MOCK_DATA:
        return load_mock_data()
    else:
        return load_real_data()

def get_productivity_metrics(data, team=None):
    """Calculate overall productivity metrics"""
    stories = data['user_stories']
    prs = data['pull_requests']
    tests = data['testing']
    support = data['prod_support']
    issues = data['prod_issues']
    
    if team:
        stories = [s for s in stories if s.get('team') == team]
        prs = [pr for pr in prs if pr.get('team') == team]
        tests = [t for t in tests if t.get('team') == team]
        support = [s for s in support if s.get('team') == team]
        issues = [i for i in issues if i.get('team') == team]
    
    total_stories = len(stories)
    completed_stories = len([s for s in stories if s['status'] == 'Done'])
    total_prs = len(prs)
    merged_prs = len([pr for pr in prs if pr['status'] == 'Merged'])
    
    total_time = sum([
        sum([s['time_spent'] for s in stories]),
        sum([pr['time_spent'] for pr in prs]),
        sum([t['time_spent'] for t in tests]),
        sum([s['time_spent'] for s in support]),
        sum([i['time_spent'] for i in issues])
    ])
    
    return {
        'total_time_spent': round(total_time, 1),
        'story_completion_rate': round((completed_stories / max(1, total_stories)) * 100, 1),
        'pr_merge_rate': round((merged_prs / max(1, total_prs)) * 100, 1),
        'total_stories': total_stories,
        'completed_stories': completed_stories,
        'total_prs': total_prs,
        'merged_prs': merged_prs,
        'active_prod_issues': len([i for i in issues if i['status'] not in ['Resolved', 'Closed']]),
        'critical_issues': len([i for i in issues if i['severity'] == 'Critical'])
    }

def get_time_distribution(data, period='week', team=None):
    """Calculate time distribution across activities"""
    stories = data['user_stories']
    prs = data['pull_requests']
    tests = data['testing']
    support = data['prod_support']
    issues = data['prod_issues']
    
    if team:
        stories = [s for s in stories if s.get('team') == team]
        prs = [pr for pr in prs if pr.get('team') == team]
        tests = [t for t in tests if t.get('team') == team]
        support = [s for s in support if s.get('team') == team]
        issues = [i for i in issues if i.get('team') == team]
    
    return {
        'development': {
            'user_stories': round(sum([s['time_spent'] for s in stories]), 1),
            'pull_requests': round(sum([pr['time_spent'] for pr in prs]), 1)
        },
        'testing': round(sum([t['time_spent'] for t in tests]), 1),
        'prod_support': round(sum([s['time_spent'] for s in support]), 1),
        'prod_issues': round(sum([i['time_spent'] for i in issues]), 1)
    }

def get_team_performance(data, team=None):
    """Calculate team member performance"""
    stories = data['user_stories']
    prs = data['pull_requests']
    tests = data['testing']
    support = data['prod_support']
    issues = data['prod_issues']
    
    if team:
        stories = [s for s in stories if s.get('team') == team]
        prs = [pr for pr in prs if pr.get('team') == team]
        tests = [t for t in tests if t.get('team') == team]
        support = [s for s in support if s.get('team') == team]
        issues = [i for i in issues if i.get('team') == team]
    
    team_stats = {}
    
    for member in TEAM_MEMBERS:
        member_stories = [s for s in stories if s['assignee'] == member]
        member_prs = [pr for pr in prs if pr['author'] == member]
        member_tests = [t for t in tests if t['tester'] == member]
        member_support = [s for s in support if s['assignee'] == member]
        member_issues = [i for i in issues if i['assignee'] == member]
        
        total_time = sum([
            sum([s['time_spent'] for s in member_stories]),
            sum([pr['time_spent'] for pr in member_prs]),
            sum([t['time_spent'] for t in member_tests]),
            sum([s['time_spent'] for s in member_support]),
            sum([i['time_spent'] for i in member_issues])
        ])
        
        team_stats[member] = {
            'name': member,
            'total_time': round(total_time, 1),
            'stories_completed': len([s for s in member_stories if s['status'] == 'Done']),
            'prs_merged': len([pr for pr in member_prs if pr['status'] == 'Merged']),
            'tests_done': len(member_tests),
            'support_tickets': len(member_support),
            'issues_resolved': len([i for i in member_issues if i['status'] == 'Resolved']),
            'productivity_score': round((
                len([s for s in member_stories if s['status'] == 'Done']) * 10 +
                len([pr for pr in member_prs if pr['status'] == 'Merged']) * 8 +
                len([t for t in member_tests if t['status'] == 'Passed']) * 5 +
                len([s for s in member_support if s['status'] == 'Resolved']) * 3 +
                len([i for i in member_issues if i['status'] == 'Resolved']) * 15
            ) / max(1, total_time), 2)
        }
    
    return list(team_stats.values())
