from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import json
from models import generate_fake_data, get_productivity_metrics, get_time_distribution, get_team_performance
from typing import Optional
from config import config

app = FastAPI(title="Progress Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data = generate_fake_data()

@app.get('/api/overview')
def get_overview(team: Optional[str] = Query(None)):
    """Get overall productivity overview"""
    return get_productivity_metrics(data, team)

@app.get('/api/status')
def get_api_status():
    """Get API integration status"""
    from jira_integration import jira_integration
    from gitlab_integration import gitlab_integration
    from confluence_integration import confluence_integration
    
    return {
        'use_mock_data': config.USE_MOCK_DATA,
        'jira_enabled': jira_integration.enabled,
        'gitlab_enabled': gitlab_integration.enabled,
        'confluence_enabled': confluence_integration.enabled,
        'teams': config.TEAMS
    }

@app.get('/api/time-distribution')
def get_time_dist(
    period: str = Query('week'),
    team: Optional[str] = Query(None)
):
    """Get time distribution across different activities"""
    return get_time_distribution(data, period, team)

@app.get('/api/team-performance')
def get_team_perf(team: Optional[str] = Query(None)):
    """Get team member performance metrics"""
    return get_team_performance(data, team)

@app.get('/api/user-stories')
def get_user_stories(team: Optional[str] = Query(None)):
    """Get all user stories with status"""
    stories = data['user_stories']
    if team:
        stories = [s for s in stories if s.get('team') == team]
    return {
        'stories': stories,
        'total': len(stories),
        'completed': len([s for s in stories if s['status'] == 'Done']),
        'in_progress': len([s for s in stories if s['status'] == 'In Progress'])
    }

@app.get('/api/pull-requests')
def get_pull_requests(team: Optional[str] = Query(None)):
    """Get all pull requests"""
    prs = data['pull_requests']
    if team:
        prs = [pr for pr in prs if pr.get('team') == team]
    return {
        'prs': prs,
        'total': len(prs),
        'merged': len([pr for pr in prs if pr['status'] == 'Merged']),
        'open': len([pr for pr in prs if pr['status'] == 'Open'])
    }

@app.get('/api/testing')
def get_testing(team: Optional[str] = Query(None)):
    """Get testing activities"""
    tests = data['testing']
    if team:
        tests = [t for t in tests if t.get('team') == team]
    return {
        'tests': tests,
        'total_time': sum([t['time_spent'] for t in tests]),
        'passed': len([t for t in tests if t['status'] == 'Passed']),
        'failed': len([t for t in tests if t['status'] == 'Failed'])
    }

@app.get('/api/prod-support')
def get_prod_support(team: Optional[str] = Query(None)):
    """Get production support activities"""
    support = data['prod_support']
    if team:
        support = [s for s in support if s.get('team') == team]
    return {
        'support': support,
        'total_time': sum([s['time_spent'] for s in support]),
        'resolved': len([s for s in support if s['status'] == 'Resolved'])
    }

@app.get('/api/prod-issues')
def get_prod_issues(team: Optional[str] = Query(None)):
    """Get production issues"""
    issues = data['prod_issues']
    if team:
        issues = [i for i in issues if i.get('team') == team]
    return {
        'issues': issues,
        'total': len(issues),
        'critical': len([i for i in issues if i['severity'] == 'Critical']),
        'resolved': len([i for i in issues if i['status'] == 'Resolved']),
        'avg_resolution_time': sum([i.get('resolution_time', 0) for i in issues if i['status'] == 'Resolved']) / max(1, len([i for i in issues if i['status'] == 'Resolved']))
    }

@app.get('/api/insights')
def get_insights(team: Optional[str] = Query(None)):
    """Get AI-generated insights about productivity"""
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
    
    total_time = sum([
        sum([s['time_spent'] for s in stories]),
        sum([pr['time_spent'] for pr in prs]),
        sum([t['time_spent'] for t in tests]),
        sum([s['time_spent'] for s in support]),
        sum([i['time_spent'] for i in issues])
    ])
    
    prod_support_time = sum([s['time_spent'] for s in support])
    prod_issues_time = sum([i['time_spent'] for i in issues])
    testing_time = sum([t['time_spent'] for t in tests])
    development_time = sum([s['time_spent'] for s in stories]) + sum([pr['time_spent'] for pr in prs])
    
    insights = []
    
    if total_time > 0:
        prod_support_pct = (prod_support_time / total_time) * 100
        prod_issues_pct = (prod_issues_time / total_time) * 100
        testing_pct = (testing_time / total_time) * 100
        dev_pct = (development_time / total_time) * 100
        
        if prod_support_pct > 25:
            insights.append({
                'type': 'warning',
                'title': 'High Production Support Time',
                'message': f'{prod_support_pct:.1f}% of time spent on production support. Consider improving monitoring and preventive measures.',
                'value': prod_support_pct
            })
        
        if prod_issues_pct > 20:
            insights.append({
                'type': 'critical',
                'title': 'Excessive Production Issues',
                'message': f'{prod_issues_pct:.1f}% of time spent on production issues. This indicates quality concerns.',
                'value': prod_issues_pct
            })
        
        if testing_pct < 15:
            insights.append({
                'type': 'warning',
                'title': 'Low Testing Coverage',
                'message': f'Only {testing_pct:.1f}% of time spent on testing. Consider increasing test coverage.',
                'value': testing_pct
            })
        
        if dev_pct > 50:
            insights.append({
                'type': 'success',
                'title': 'Good Development Focus',
                'message': f'{dev_pct:.1f}% of time focused on development. Team is productive on new features.',
                'value': dev_pct
            })
    
    avg_pr_time = sum([pr['time_spent'] for pr in prs]) / max(1, len(prs))
    if avg_pr_time > 16:
        insights.append({
            'type': 'warning',
            'title': 'Long PR Review Times',
            'message': f'Average PR takes {avg_pr_time:.1f} hours. Consider streamlining review process.',
            'value': avg_pr_time
        })
    
    return {'insights': insights}

@app.get('/api/trends')
def get_trends(
    days: int = Query(30),
    team: Optional[str] = Query(None)
):
    """Get productivity trends over time"""
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
    
    trends = {}
    base_date = datetime.now() - timedelta(days=days)
    
    for i in range(days):
        date = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
        trends[date] = {
            'development': 0,
            'testing': 0,
            'prod_support': 0,
            'prod_issues': 0
        }
    
    for story in stories:
        date = story['created_date']
        if date in trends:
            trends[date]['development'] += story['time_spent'] / 7
    
    for pr in prs:
        date = pr['created_date']
        if date in trends:
            trends[date]['development'] += pr['time_spent'] / 7
    
    for test in tests:
        date = test['date']
        if date in trends:
            trends[date]['testing'] += test['time_spent']
    
    for sup in support:
        date = sup['date']
        if date in trends:
            trends[date]['prod_support'] += sup['time_spent']
    
    for issue in issues:
        date = issue['reported_date']
        if date in trends:
            trends[date]['prod_issues'] += issue['time_spent']
    
    return {
        'dates': list(trends.keys()),
        'data': trends
    }

@app.get('/api/teams')
def get_teams():
    """Get list of all teams"""
    teams = set()
    for item in data['user_stories']:
        if 'team' in item:
            teams.add(item['team'])
    for item in data['pull_requests']:
        if 'team' in item:
            teams.add(item['team'])
    for item in data['testing']:
        if 'team' in item:
            teams.add(item['team'])
    for item in data['prod_support']:
        if 'team' in item:
            teams.add(item['team'])
    for item in data['prod_issues']:
        if 'team' in item:
            teams.add(item['team'])
    return {'teams': sorted(list(teams))}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=5001)
