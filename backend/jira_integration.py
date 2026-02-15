from jira import JIRA
from config import config
from datetime import datetime, timedelta
from cachetools import TTLCache
import time

cache = TTLCache(maxsize=100, ttl=config.CACHE_EXPIRY)

class JiraIntegration:
    def __init__(self):
        if config.JIRA_URL and config.JIRA_API_TOKEN:
            self.jira = JIRA(
                server=config.JIRA_URL,
                basic_auth=(config.JIRA_EMAIL, config.JIRA_API_TOKEN)
            )
            self.enabled = True
        else:
            self.jira = None
            self.enabled = False
    
    def get_user_stories(self):
        """Fetch user stories/issues from Jira"""
        if not self.enabled:
            return []
        
        cache_key = 'jira_stories'
        if cache_key in cache:
            return cache[cache_key]
        
        try:
            # Search for issues in the project
            jql = f'project = {config.JIRA_PROJECT_KEY} AND type in (Story, Task, Bug) ORDER BY created DESC'
            issues = self.jira.search_issues(jql, maxResults=100, expand='changelog')
            
            stories = []
            for issue in issues:
                # Get team from custom field or label
                team = self._extract_team(issue)
                
                # Calculate time spent (in hours)
                time_spent = 0
                if issue.fields.timespent:
                    time_spent = issue.fields.timespent / 3600  # Convert seconds to hours
                
                # Get story points
                story_points = getattr(issue.fields, 'customfield_10016', 0) or 0  # Common story points field
                
                story = {
                    'id': issue.key,
                    'title': issue.fields.summary,
                    'type': str(issue.fields.issuetype),
                    'status': str(issue.fields.status),
                    'assignee': str(issue.fields.assignee) if issue.fields.assignee else 'Unassigned',
                    'team': team,
                    'created_date': issue.fields.created[:10],
                    'time_spent': time_spent,
                    'story_points': story_points,
                    'priority': str(issue.fields.priority) if issue.fields.priority else 'Medium'
                }
                stories.append(story)
            
            cache[cache_key] = stories
            return stories
            
        except Exception as e:
            return []
    
    def get_testing_activities(self):
        """Fetch testing-related issues from Jira"""
        if not self.enabled:
            return []
        
        cache_key = 'jira_testing'
        if cache_key in cache:
            return cache[cache_key]
        
        try:
            # Search for test-related issues
            jql = f'project = {config.JIRA_PROJECT_KEY} AND (type = Test OR labels in (testing, qa)) ORDER BY created DESC'
            issues = self.jira.search_issues(jql, maxResults=100)
            
            tests = []
            for issue in issues:
                team = self._extract_team(issue)
                
                time_spent = 0
                if issue.fields.timespent:
                    time_spent = issue.fields.timespent / 3600
                
                test = {
                    'id': issue.key,
                    'type': 'Manual Test' if 'manual' in str(issue.fields.summary).lower() else 'Automated Test',
                    'description': issue.fields.summary,
                    'status': 'Passed' if str(issue.fields.status) == 'Done' else 'Failed' if str(issue.fields.status) == 'Failed' else 'In Progress',
                    'tester': str(issue.fields.assignee) if issue.fields.assignee else 'Unassigned',
                    'team': team,
                    'date': issue.fields.created[:10],
                    'time_spent': time_spent,
                    'test_cases': 1,
                    'bugs_found': self._count_linked_bugs(issue)
                }
                tests.append(test)
            
            cache[cache_key] = tests
            return tests
            
        except Exception as e:
            return []
    
    def get_production_issues(self):
        """Fetch production issues from Jira"""
        if not self.enabled:
            return []
        
        cache_key = 'jira_prod_issues'
        if cache_key in cache:
            return cache[cache_key]
        
        try:
            # Search for production issues
            jql = f'project = {config.JIRA_PROJECT_KEY} AND (labels in (production, prod) OR priority in (Critical, Blocker)) ORDER BY created DESC'
            issues = self.jira.search_issues(jql, maxResults=100)
            
            prod_issues = []
            for issue in issues:
                team = self._extract_team(issue)
                
                time_spent = 0
                if issue.fields.timespent:
                    time_spent = issue.fields.timespent / 3600
                
                # Calculate resolution time
                resolution_time = None
                if issue.fields.resolutiondate and issue.fields.created:
                    created = datetime.fromisoformat(issue.fields.created.replace('Z', '+00:00'))
                    resolved = datetime.fromisoformat(issue.fields.resolutiondate.replace('Z', '+00:00'))
                    resolution_time = (resolved - created).total_seconds() / 3600
                
                prod_issue = {
                    'id': issue.key,
                    'title': issue.fields.summary,
                    'severity': str(issue.fields.priority) if issue.fields.priority else 'Medium',
                    'status': str(issue.fields.status),
                    'reported_by': str(issue.fields.reporter) if issue.fields.reporter else 'Unknown',
                    'assignee': str(issue.fields.assignee) if issue.fields.assignee else 'Unassigned',
                    'team': team,
                    'reported_date': issue.fields.created[:10],
                    'time_spent': time_spent,
                    'resolution_time': resolution_time,
                    'impact': str(issue.fields.priority) if issue.fields.priority else 'Medium',
                    'affected_users': 0  # Would need custom field
                }
                prod_issues.append(prod_issue)
            
            cache[cache_key] = prod_issues
            return prod_issues
            
        except Exception as e:
            return []
    
    def get_support_tickets(self):
        """Fetch support tickets from Jira"""
        if not self.enabled:
            return []
        
        cache_key = 'jira_support'
        if cache_key in cache:
            return cache[cache_key]
        
        try:
            # Search for support tickets
            jql = f'project = {config.JIRA_PROJECT_KEY} AND (type = "Support" OR labels in (support, customer)) ORDER BY created DESC'
            issues = self.jira.search_issues(jql, maxResults=100)
            
            tickets = []
            for issue in issues:
                team = self._extract_team(issue)
                
                time_spent = 0
                if issue.fields.timespent:
                    time_spent = issue.fields.timespent / 3600
                
                ticket = {
                    'id': issue.key,
                    'type': 'User Query',
                    'description': issue.fields.summary,
                    'status': str(issue.fields.status),
                    'assignee': str(issue.fields.assignee) if issue.fields.assignee else 'Unassigned',
                    'team': team,
                    'date': issue.fields.created[:10],
                    'time_spent': time_spent,
                    'priority': str(issue.fields.priority) if issue.fields.priority else 'Medium',
                    'customer': getattr(issue.fields, 'customfield_10000', 'Unknown')  # Customer field
                }
                tickets.append(ticket)
            
            cache[cache_key] = tickets
            return tickets
            
        except Exception as e:
            return []
    
    def _extract_team(self, issue):
        """Extract team information from issue"""
        # Try to get team from labels
        if issue.fields.labels:
            for label in issue.fields.labels:
                for team in config.TEAMS:
                    if team.lower().replace(' ', '') in label.lower():
                        return team
        
        # Try to get team from custom field (adjust field ID as needed)
        team_field = getattr(issue.fields, 'customfield_10001', None)
        if team_field:
            return str(team_field)
        
        # Try to get team from component
        if issue.fields.components:
            for component in issue.fields.components:
                for team in config.TEAMS:
                    if team.lower().replace(' ', '') in str(component).lower():
                        return team
        
        # Default to first team
        return config.TEAMS[0] if config.TEAMS else 'Default Team'
    
    def _count_linked_bugs(self, issue):
        """Count linked bugs for an issue"""
        try:
            bug_count = 0
            if hasattr(issue.fields, 'issuelinks'):
                for link in issue.fields.issuelinks:
                    if hasattr(link, 'outwardIssue'):
                        if str(link.outwardIssue.fields.issuetype) == 'Bug':
                            bug_count += 1
            return bug_count
        except:
            return 0

jira_integration = JiraIntegration()
