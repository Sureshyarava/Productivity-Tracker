import gitlab
from config import config
from datetime import datetime
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=config.CACHE_EXPIRY)

class GitLabIntegration:
    def __init__(self):
        if config.GITLAB_URL and config.GITLAB_TOKEN:
            self.gl = gitlab.Gitlab(config.GITLAB_URL, private_token=config.GITLAB_TOKEN)
            self.enabled = True
        else:
            self.gl = None
            self.enabled = False
    
    def get_merge_requests(self):
        """Fetch merge requests (pull requests) from GitLab"""
        if not self.enabled:
            return []
        
        cache_key = 'gitlab_mrs'
        if cache_key in cache:
            return cache[cache_key]
        
        try:
            merge_requests = []
            
            for project_id in config.GITLAB_PROJECT_IDS:
                if not project_id.strip():
                    continue
                    
                try:
                    project = self.gl.projects.get(project_id.strip())
                    mrs = project.mergerequests.list(state='all', order_by='created_at', sort='desc', per_page=50)
                    
                    for mr in mrs:
                        # Determine team from labels or branch
                        team = self._extract_team_from_labels(mr.labels)
                        
                        # Calculate time spent (hours between created and merged/closed)
                        time_spent = self._calculate_mr_time(mr)
                        
                        # Get diff stats
                        changes = mr.changes() if hasattr(mr, 'changes') else {}
                        lines_added = sum(change.get('additions', 0) for change in changes.get('changes', []))
                        lines_deleted = sum(change.get('deletions', 0) for change in changes.get('changes', []))
                        
                        mr_data = {
                            'id': f'MR-{mr.iid}',
                            'title': mr.title,
                            'status': self._map_mr_state(mr.state),
                            'author': mr.author['name'] if mr.author else 'Unknown',
                            'reviewer': self._get_reviewer(mr),
                            'team': team,
                            'created_date': mr.created_at[:10],
                            'time_spent': time_spent,
                            'lines_added': lines_added if lines_added > 0 else mr.changes_count * 50,  # Estimate
                            'lines_deleted': lines_deleted if lines_deleted > 0 else mr.changes_count * 20,  # Estimate
                            'comments': mr.user_notes_count,
                            'commits': len(mr.commits().list()) if hasattr(mr, 'commits') else 1
                        }
                        merge_requests.append(mr_data)
                        
                except Exception as e:
                    continue
            
            cache[cache_key] = merge_requests
            return merge_requests
            
        except Exception as e:
            return []
    
    def get_pipeline_statistics(self):
        """Fetch CI/CD pipeline statistics"""
        if not self.enabled:
            return {}
        
        cache_key = 'gitlab_pipelines'
        if cache_key in cache:
            return cache[cache_key]
        
        try:
            pipeline_stats = {
                'total_pipelines': 0,
                'successful': 0,
                'failed': 0,
                'avg_duration': 0
            }
            
            total_duration = 0
            
            for project_id in config.GITLAB_PROJECT_IDS:
                if not project_id.strip():
                    continue
                    
                try:
                    project = self.gl.projects.get(project_id.strip())
                    pipelines = project.pipelines.list(per_page=20)
                    
                    for pipeline in pipelines:
                        pipeline_stats['total_pipelines'] += 1
                        
                        if pipeline.status == 'success':
                            pipeline_stats['successful'] += 1
                        elif pipeline.status == 'failed':
                            pipeline_stats['failed'] += 1
                        
                        if pipeline.duration:
                            total_duration += pipeline.duration
                            
                except Exception as e:
                    continue
            
            if pipeline_stats['total_pipelines'] > 0:
                pipeline_stats['avg_duration'] = total_duration / pipeline_stats['total_pipelines'] / 60  # Convert to minutes
            
            cache[cache_key] = pipeline_stats
            return pipeline_stats
            
        except Exception as e:
            return {}
    
    def get_commit_activity(self):
        """Fetch recent commit activity"""
        if not self.enabled:
            return []
        
        cache_key = 'gitlab_commits'
        if cache_key in cache:
            return cache[cache_key]
        
        try:
            commits = []
            
            for project_id in config.GITLAB_PROJECT_IDS:
                if not project_id.strip():
                    continue
                    
                try:
                    project = self.gl.projects.get(project_id.strip())
                    project_commits = project.commits.list(per_page=50)
                    
                    for commit in project_commits:
                        commit_data = {
                            'id': commit.short_id,
                            'message': commit.title,
                            'author': commit.author_name,
                            'date': commit.created_at[:10],
                            'additions': commit.stats.get('additions', 0) if hasattr(commit, 'stats') else 0,
                            'deletions': commit.stats.get('deletions', 0) if hasattr(commit, 'stats') else 0
                        }
                        commits.append(commit_data)
                        
                except Exception as e:
                    continue
            
            cache[cache_key] = commits
            return commits
            
        except Exception as e:
            return []
    
    def _extract_team_from_labels(self, labels):
        """Extract team from GitLab labels"""
        if not labels:
            return config.TEAMS[0] if config.TEAMS else 'Default Team'
        
        for label in labels:
            for team in config.TEAMS:
                if team.lower().replace(' ', '') in label.lower():
                    return team
        
        return config.TEAMS[0] if config.TEAMS else 'Default Team'
    
    def _map_mr_state(self, state):
        """Map GitLab MR state to our status"""
        state_map = {
            'merged': 'Merged',
            'opened': 'Open',
            'closed': 'Closed',
            'locked': 'Closed'
        }
        return state_map.get(state, 'Open')
    
    def _get_reviewer(self, mr):
        """Get the primary reviewer of an MR"""
        try:
            if hasattr(mr, 'reviewers') and mr.reviewers:
                return mr.reviewers[0]['name']
            elif hasattr(mr, 'assignee') and mr.assignee:
                return mr.assignee['name']
            return 'No Reviewer'
        except:
            return 'No Reviewer'
    
    def _calculate_mr_time(self, mr):
        """Calculate time spent on MR in hours"""
        try:
            created = datetime.fromisoformat(mr.created_at.replace('Z', '+00:00'))
            
            if mr.merged_at:
                merged = datetime.fromisoformat(mr.merged_at.replace('Z', '+00:00'))
                return (merged - created).total_seconds() / 3600
            elif mr.closed_at:
                closed = datetime.fromisoformat(mr.closed_at.replace('Z', '+00:00'))
                return (closed - created).total_seconds() / 3600
            else:
                now = datetime.now(created.tzinfo)
                return (now - created).total_seconds() / 3600
        except:
            return 8.0  # Default estimate

gitlab_integration = GitLabIntegration()
