import json
import os

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
        print(f"Error: {MOCK_DATA_FILE} not found!")
        return {
            'user_stories': [],
            'pull_requests': [],
            'testing': [],
            'prod_support': [],
            'prod_issues': []
        }
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {
            'user_stories': [],
            'pull_requests': [],
            'testing': [],
            'prod_support': [],
            'prod_issues': []
        }

def generate_fake_data():
    """Load data from JSON file"""
    return load_mock_data()

def get_productivity_metrics(data):
    """Calculate overall productivity metrics"""
    total_stories = len(data['user_stories'])
    completed_stories = len([s for s in data['user_stories'] if s['status'] == 'Done'])
    total_prs = len(data['pull_requests'])
    merged_prs = len([pr for pr in data['pull_requests'] if pr['status'] == 'Merged'])
    
    total_time = sum([
        sum([s['time_spent'] for s in data['user_stories']]),
        sum([pr['time_spent'] for pr in data['pull_requests']]),
        sum([t['time_spent'] for t in data['testing']]),
        sum([s['time_spent'] for s in data['prod_support']]),
        sum([i['time_spent'] for i in data['prod_issues']])
    ])
    
    return {
        'total_time_spent': round(total_time, 1),
        'story_completion_rate': round((completed_stories / max(1, total_stories)) * 100, 1),
        'pr_merge_rate': round((merged_prs / max(1, total_prs)) * 100, 1),
        'total_stories': total_stories,
        'completed_stories': completed_stories,
        'total_prs': total_prs,
        'merged_prs': merged_prs,
        'active_prod_issues': len([i for i in data['prod_issues'] if i['status'] not in ['Resolved', 'Closed']]),
        'critical_issues': len([i for i in data['prod_issues'] if i['severity'] == 'Critical'])
    }

def get_time_distribution(data, period='week'):
    """Calculate time distribution across activities"""
    return {
        'development': {
            'user_stories': round(sum([s['time_spent'] for s in data['user_stories']]), 1),
            'pull_requests': round(sum([pr['time_spent'] for pr in data['pull_requests']]), 1)
        },
        'testing': round(sum([t['time_spent'] for t in data['testing']]), 1),
        'prod_support': round(sum([s['time_spent'] for s in data['prod_support']]), 1),
        'prod_issues': round(sum([i['time_spent'] for i in data['prod_issues']]), 1)
    }

def get_team_performance(data):
    """Calculate team member performance"""
    team_stats = {}
    
    for member in TEAM_MEMBERS:
        stories = [s for s in data['user_stories'] if s['assignee'] == member]
        prs = [pr for pr in data['pull_requests'] if pr['author'] == member]
        tests = [t for t in data['testing'] if t['tester'] == member]
        support = [s for s in data['prod_support'] if s['assignee'] == member]
        issues = [i for i in data['prod_issues'] if i['assignee'] == member]
        
        total_time = sum([
            sum([s['time_spent'] for s in stories]),
            sum([pr['time_spent'] for pr in prs]),
            sum([t['time_spent'] for t in tests]),
            sum([s['time_spent'] for s in support]),
            sum([i['time_spent'] for i in issues])
        ])
        
        team_stats[member] = {
            'name': member,
            'total_time': round(total_time, 1),
            'stories_completed': len([s for s in stories if s['status'] == 'Done']),
            'prs_merged': len([pr for pr in prs if pr['status'] == 'Merged']),
            'tests_done': len(tests),
            'support_tickets': len(support),
            'issues_resolved': len([i for i in issues if i['status'] == 'Resolved']),
            'productivity_score': round((
                len([s for s in stories if s['status'] == 'Done']) * 10 +
                len([pr for pr in prs if pr['status'] == 'Merged']) * 8 +
                len([t for t in tests if t['status'] == 'Passed']) * 5 +
                len([s for s in support if s['status'] == 'Resolved']) * 3 +
                len([i for i in issues if i['status'] == 'Resolved']) * 15
            ) / max(1, total_time), 2)
        }
    
    return list(team_stats.values())
