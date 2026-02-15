from atlassian import Confluence
from config import config
from datetime import datetime, timedelta
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=config.CACHE_EXPIRY)

class ConfluenceIntegration:
    def __init__(self):
        if config.CONFLUENCE_URL and config.CONFLUENCE_API_TOKEN:
            self.confluence = Confluence(
                url=config.CONFLUENCE_URL,
                username=config.CONFLUENCE_EMAIL,
                password=config.CONFLUENCE_API_TOKEN,
                cloud=True
            )
            self.enabled = True
        else:
            self.confluence = None
            self.enabled = False
    
    def get_documentation_stats(self):
        """Fetch documentation and collaboration statistics from Confluence"""
        if not self.enabled:
            return {}
        
        cache_key = 'confluence_docs'
        if cache_key in cache:
            return cache[cache_key]
        
        try:
            stats = {
                'total_pages': 0,
                'recent_updates': 0,
                'team_pages': {},
                'popular_pages': []
            }
            
            # Get all pages in the space
            space_key = config.CONFLUENCE_SPACE_KEY
            
            if space_key:
                # Get pages
                pages = self.confluence.get_all_pages_from_space(space_key, limit=100)
                stats['total_pages'] = len(pages)
                
                # Count recent updates (last 30 days)
                thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
                
                for page in pages[:50]:  # Process first 50 for performance
                    try:
                        page_details = self.confluence.get_page_by_id(page['id'], expand='version,metadata.labels')
                        
                        # Check if updated recently
                        last_updated = page_details.get('version', {}).get('when', '')
                        if last_updated and last_updated > thirty_days_ago:
                            stats['recent_updates'] += 1
                        
                        # Extract team from labels
                        labels = page_details.get('metadata', {}).get('labels', {}).get('results', [])
                        team = self._extract_team_from_labels(labels)
                        
                        if team not in stats['team_pages']:
                            stats['team_pages'][team] = 0
                        stats['team_pages'][team] += 1
                        
                    except Exception as e:
                        continue
            
            cache[cache_key] = stats
            return stats
            
        except Exception as e:
            return {}
    
    def get_team_collaboration_metrics(self):
        """Get collaboration metrics from Confluence"""
        if not self.enabled:
            return {}
        
        cache_key = 'confluence_collab'
        if cache_key in cache:
            return cache[cache_key]
        
        try:
            metrics = {
                'active_contributors': set(),
                'total_comments': 0,
                'knowledge_base_size': 0
            }
            
            space_key = config.CONFLUENCE_SPACE_KEY
            
            if space_key:
                pages = self.confluence.get_all_pages_from_space(space_key, limit=100)
                
                for page in pages[:50]:
                    try:
                        # Get page details
                        page_details = self.confluence.get_page_by_id(page['id'], expand='version,history')
                        
                        # Track contributors
                        author = page_details.get('version', {}).get('by', {}).get('displayName')
                        if author:
                            metrics['active_contributors'].add(author)
                        
                        # Get comments
                        comments = self.confluence.get_page_comments(page['id'])
                        if comments:
                            metrics['total_comments'] += len(comments)
                        
                        # Add to knowledge base size
                        body = page_details.get('body', {}).get('storage', {}).get('value', '')
                        metrics['knowledge_base_size'] += len(body)
                        
                    except Exception as e:
                        continue
            
            # Convert set to count
            metrics['active_contributors'] = len(metrics['active_contributors'])
            
            cache[cache_key] = metrics
            return metrics
            
        except Exception as e:
            return {}
    
    def get_sprint_retrospectives(self):
        """Get sprint retrospective data from Confluence"""
        if not self.enabled:
            return []
        
        cache_key = 'confluence_retros'
        if cache_key in cache:
            return cache[cache_key]
        
        try:
            retrospectives = []
            
            space_key = config.CONFLUENCE_SPACE_KEY
            
            if space_key:
                # Search for retrospective pages
                cql = f'space = "{space_key}" AND (title ~ "retrospective" OR title ~ "retro" OR label = "retrospective")'
                results = self.confluence.cql(cql, limit=20)
                
                if results and 'results' in results:
                    for result in results['results']:
                        try:
                            page_id = result['content']['id']
                            page = self.confluence.get_page_by_id(page_id, expand='version')
                            
                            retro = {
                                'title': result['content']['title'],
                                'date': page.get('version', {}).get('when', '')[:10],
                                'author': page.get('version', {}).get('by', {}).get('displayName', 'Unknown'),
                                'url': f"{config.CONFLUENCE_URL}/pages/viewpage.action?pageId={page_id}"
                            }
                            retrospectives.append(retro)
                            
                        except Exception as e:
                            continue
            
            cache[cache_key] = retrospectives
            return retrospectives
            
        except Exception as e:
            return []
    
    def _extract_team_from_labels(self, labels):
        """Extract team from Confluence labels"""
        if not labels:
            return config.TEAMS[0] if config.TEAMS else 'Default Team'
        
        for label in labels:
            label_name = label.get('name', '').lower()
            for team in config.TEAMS:
                if team.lower().replace(' ', '') in label_name:
                    return team
        
        return config.TEAMS[0] if config.TEAMS else 'Default Team'

confluence_integration = ConfluenceIntegration()
