from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import json
from models import generate_fake_data, get_productivity_metrics, get_time_distribution, get_team_performance

app = Flask(__name__)
CORS(app)

# Generate fake data on startup
data = generate_fake_data()

@app.route('/api/overview', methods=['GET'])
def get_overview():
    """Get overall productivity overview"""
    return jsonify(get_productivity_metrics(data))

@app.route('/api/time-distribution', methods=['GET'])
def get_time_dist():
    """Get time distribution across different activities"""
    period = request.args.get('period', 'week')  # day, week, month
    return jsonify(get_time_distribution(data, period))

@app.route('/api/team-performance', methods=['GET'])
def get_team_perf():
    """Get team member performance metrics"""
    return jsonify(get_team_performance(data))

@app.route('/api/user-stories', methods=['GET'])
def get_user_stories():
    """Get all user stories with status"""
    return jsonify({
        'stories': data['user_stories'],
        'total': len(data['user_stories']),
        'completed': len([s for s in data['user_stories'] if s['status'] == 'Done']),
        'in_progress': len([s for s in data['user_stories'] if s['status'] == 'In Progress'])
    })

@app.route('/api/pull-requests', methods=['GET'])
def get_pull_requests():
    """Get all pull requests"""
    return jsonify({
        'prs': data['pull_requests'],
        'total': len(data['pull_requests']),
        'merged': len([pr for pr in data['pull_requests'] if pr['status'] == 'Merged']),
        'open': len([pr for pr in data['pull_requests'] if pr['status'] == 'Open'])
    })

@app.route('/api/testing', methods=['GET'])
def get_testing():
    """Get testing activities"""
    return jsonify({
        'tests': data['testing'],
        'total_time': sum([t['time_spent'] for t in data['testing']]),
        'passed': len([t for t in data['testing'] if t['status'] == 'Passed']),
        'failed': len([t for t in data['testing'] if t['status'] == 'Failed'])
    })

@app.route('/api/prod-support', methods=['GET'])
def get_prod_support():
    """Get production support activities"""
    return jsonify({
        'support': data['prod_support'],
        'total_time': sum([s['time_spent'] for s in data['prod_support']]),
        'resolved': len([s for s in data['prod_support'] if s['status'] == 'Resolved'])
    })

@app.route('/api/prod-issues', methods=['GET'])
def get_prod_issues():
    """Get production issues"""
    return jsonify({
        'issues': data['prod_issues'],
        'total': len(data['prod_issues']),
        'critical': len([i for i in data['prod_issues'] if i['severity'] == 'Critical']),
        'resolved': len([i for i in data['prod_issues'] if i['status'] == 'Resolved']),
        'avg_resolution_time': sum([i.get('resolution_time', 0) for i in data['prod_issues'] if i['status'] == 'Resolved']) / max(1, len([i for i in data['prod_issues'] if i['status'] == 'Resolved']))
    })

@app.route('/api/insights', methods=['GET'])
def get_insights():
    """Get AI-generated insights about productivity"""
    total_time = sum([
        sum([s['time_spent'] for s in data['user_stories']]),
        sum([pr['time_spent'] for pr in data['pull_requests']]),
        sum([t['time_spent'] for t in data['testing']]),
        sum([s['time_spent'] for s in data['prod_support']]),
        sum([i['time_spent'] for i in data['prod_issues']])
    ])
    
    prod_support_time = sum([s['time_spent'] for s in data['prod_support']])
    prod_issues_time = sum([i['time_spent'] for i in data['prod_issues']])
    testing_time = sum([t['time_spent'] for t in data['testing']])
    development_time = sum([s['time_spent'] for s in data['user_stories']]) + sum([pr['time_spent'] for pr in data['pull_requests']])
    
    insights = []
    
    # Calculate percentages
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
    
    # PR insights
    avg_pr_time = sum([pr['time_spent'] for pr in data['pull_requests']]) / max(1, len(data['pull_requests']))
    if avg_pr_time > 16:
        insights.append({
            'type': 'warning',
            'title': 'Long PR Review Times',
            'message': f'Average PR takes {avg_pr_time:.1f} hours. Consider streamlining review process.',
            'value': avg_pr_time
        })
    
    return jsonify({'insights': insights})

@app.route('/api/trends', methods=['GET'])
def get_trends():
    """Get productivity trends over time"""
    days = int(request.args.get('days', 30))
    
    # Group data by date
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
    
    # Distribute time across dates (simplified)
    for story in data['user_stories']:
        date = story['created_date']
        if date in trends:
            trends[date]['development'] += story['time_spent'] / 7
    
    for pr in data['pull_requests']:
        date = pr['created_date']
        if date in trends:
            trends[date]['development'] += pr['time_spent'] / 7
    
    for test in data['testing']:
        date = test['date']
        if date in trends:
            trends[date]['testing'] += test['time_spent']
    
    for support in data['prod_support']:
        date = support['date']
        if date in trends:
            trends[date]['prod_support'] += support['time_spent']
    
    for issue in data['prod_issues']:
        date = issue['reported_date']
        if date in trends:
            trends[date]['prod_issues'] += issue['time_spent']
    
    return jsonify({
        'dates': list(trends.keys()),
        'data': trends
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='127.0.0.1')
