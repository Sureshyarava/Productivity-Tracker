# Productivity Tracker

A comprehensive productivity tracking tool that measures team performance across multiple dimensions including user stories, pull requests, testing activities, production support, and production issues. Get actionable insights to identify bottlenecks and optimize team productivity.

## Features

- **Real Data Integration**: Connect to Jira, GitLab, and Confluence for live data
- **Multi-Team Support**: Track and compare performance across multiple teams
- **Team Filtering**: Filter all views by specific team or view all teams combined
- **Dashboard Overview**: Real-time metrics and KPIs at a glance
- **Time Distribution Analysis**: Visualize how time is spent across different activities
- **Team Performance Tracking**: Individual team member productivity metrics
- **AI-Powered Insights**: Automated analysis and recommendations
- **User Stories Tracking**: Monitor story completion and progress from Jira
- **Pull Request Management**: Track MR status and review times from GitLab
- **Testing Activities**: Monitor test coverage and results from Jira
- **Production Support**: Track support tickets and resolution times from Jira
- **Production Issues**: Monitor and analyze production incidents from Jira
- **Documentation Metrics**: Track Confluence page updates and collaboration

## Architecture

### Backend (Python/FastAPI)
- RESTful API with multiple endpoints
- Real-time data from Jira, GitLab, and Confluence APIs
- Mock data fallback for testing/demo purposes
- Intelligent caching layer (5-minute TTL)
- Productivity metrics calculation
- Time distribution analysis
- Team performance analytics
- Multi-team filtering support

### API Integrations
- **Jira**: User stories, testing activities, support tickets, production issues
- **GitLab**: Merge requests, pipeline statistics, commit activity
- **Confluence**: Documentation metrics, collaboration stats, retrospectives

### Frontend (React)
- Modern, responsive dashboard
- Interactive data visualizations (Chart.js, Recharts)
- Multiple views for different metrics
- Real-time data updates
- Team selector for filtering data

## Project Structure

```
Progress-Tracker/
├── backend/
│   ├── app.py                    # FastAPI server
│   ├── models.py                 # Data models and metric calculations
│   ├── config.py                 # Configuration management
│   ├── jira_integration.py       # Jira API integration
│   ├── gitlab_integration.py     # GitLab API integration
│   ├── confluence_integration.py # Confluence API integration
│   ├── mock_data.json            # Mock data for testing
│   ├── .env.example              # Environment variables template
│   └── requirements.txt          # Python dependencies
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/
    │   │   ├── Dashboard.js         # Main dashboard
    │   │   ├── TimeDistribution.js  # Time analysis charts
    │   │   ├── TeamPerformance.js   # Team metrics
    │   │   ├── Insights.js          # AI insights
    │   │   ├── UserStories.js       # Stories tracking
    │   │   └── PullRequests.js      # PR tracking
    │   ├── App.js
    │   ├── App.css
    │   └── index.js
    └── package.json
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- (Optional) Jira, GitLab, and Confluence accounts with API access

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API connections (optional):
```bash
cp .env.example .env
# Edit .env with your Jira, GitLab, and Confluence credentials
```

If you don't configure API connections, the system will use mock data automatically.

5. Start the FastAPI server:
```bash
python app.py
```

The backend API will run on `http://localhost:5001`

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000` and automatically open in your browser.

## API Endpoints

### Overview & Metrics
- `GET /api/overview?team={team}` - Overall productivity metrics (optional team filter)
- `GET /api/status` - API integration status and configuration
- `GET /api/time-distribution?period=week&team={team}` - Time distribution analysis
- `GET /api/team-performance?team={team}` - Team member performance metrics
- `GET /api/insights?team={team}` - AI-generated insights and recommendations
- `GET /api/trends?days=30&team={team}` - Productivity trends over time

### Data Endpoints
- `GET /api/user-stories?team={team}` - All user stories with status
- `GET /api/pull-requests?team={team}` - All pull/merge requests
- `GET /api/testing?team={team}` - Testing activities
- `GET /api/prod-support?team={team}` - Production support tickets
- `GET /api/prod-issues?team={team}` - Production issues
- `GET /api/teams` - List of all configured teams

## 📈 Key Metrics Tracked

### Development Metrics
- User stories completed
- Story points delivered
- Time spent on development
- PR merge rate
- Code review times

### Quality Metrics
- Test coverage
- Test execution time
- Bugs found during testing
- Failed test cases

### Support Metrics
- Support tickets resolved
- Average resolution time
- Time spent on support
- Customer satisfaction

### Production Metrics
- Production issues count
- Issue severity distribution
- Mean time to resolution (MTTR)
- Impact on users

## 🎨 Dashboard Views

### 1. Dashboard
- Total time spent across all activities
- Story completion rate
- PR merge rate
- Active production issues
- Time distribution pie chart

### 2. Time Distribution
- Daily time allocation trends
- Stacked area charts
- Activity breakdown
- Comparative analysis

### 3. Team Performance
- Individual productivity scores
- Stories completed per member
- PRs merged per member
- Support tickets handled
- Issues resolved

### 4. Insights
- AI-powered recommendations
- Time waste identification
- Best practices suggestions
- Improvement areas

### 5. User Stories
- Complete story list
- Filter by status
- Priority tracking
- Time spent per story

### 6. Pull Requests
- PR status tracking
- Review times
- Code change metrics
- Comment statistics

## Insights & Recommendations

The system automatically analyzes productivity patterns and provides insights such as:

- **High Production Support Time**: Warns when support consumes >25% of time
- **Excessive Production Issues**: Alerts when issues take >20% of time
- **Low Testing Coverage**: Flags when testing is <15% of time
- **Good Development Focus**: Confirms when development is >50% of time
- **Long PR Review Times**: Identifies slow review processes

## Productivity Score Calculation

The productivity score for each team member is calculated based on:

- **Stories Completed**: 10 points per story
- **PRs Merged**: 8 points per PR
- **Tests Passed**: 5 points per test
- **Support Resolved**: 3 points per ticket
- **Issues Resolved**: 15 points per issue

Score is normalized by total time spent for fair comparison.

## Customization

### Configuring API Integrations

The system supports real-time data from:

- **Jira**: Configure `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, and `JIRA_PROJECT_KEY` in `.env`
- **GitLab**: Set `GITLAB_URL`, `GITLAB_TOKEN`, and `GITLAB_PROJECT_IDS` (comma-separated project IDs)
- **Confluence**: Configure `CONFLUENCE_URL`, `CONFLUENCE_EMAIL`, `CONFLUENCE_API_TOKEN`, and `CONFLUENCE_SPACE_KEY`

#### Obtaining API Tokens

**Jira**:
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Copy the token and add to `.env`

**GitLab**:
1. Go to User Settings > Access Tokens
2. Create a token with `read_api` and `read_repository` scopes
3. Copy the token and add to `.env`

**Confluence**:
1. Use the same API token as Jira (if using Atlassian Cloud)
2. Or generate a separate token following the Jira steps

#### Team Mapping

Teams are extracted from:
- **Jira**: Labels, custom fields, or components containing team names
- **GitLab**: Labels on merge requests matching team names
- **Confluence**: Page labels matching team names

Configure your teams in `.env`:
```
TEAMS=Team Alpha,Team Beta,Team Gamma
```

### Modifying Metrics
Edit the calculation functions in `backend/models.py`:
- `get_productivity_metrics()`
- `get_time_distribution()`
- `get_team_performance()`

## 📱 Screenshots & Features

### Dashboard Features
✅ Real-time metrics  
✅ Interactive charts  
✅ Time distribution visualization  
✅ Team performance comparison  
✅ Automated insights  
✅ Filterable data tables  
✅ Responsive design  
✅ Export capabilities (can be added)  

## Technologies Used

### Backend
- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for FastAPI
- **Python**: Core language
- **Jira API** (jira): Integration with Atlassian Jira
- **GitLab API** (python-gitlab): Integration with GitLab
- **Confluence API** (atlassian-python-api): Integration with Confluence
- **Cachetools**: Intelligent caching layer
- **Python-dotenv**: Environment configuration

### Frontend
- **React**: UI library
- **Chart.js**: Pie/doughnut charts
- **Recharts**: Line/bar/area charts
- **Axios**: HTTP client
- **CSS3**: Styling

## Security Considerations

For production deployment:
1. Add authentication and authorization
2. Implement rate limiting
3. Use environment variables for configuration
4. Enable HTTPS
5. Add input validation
6. Implement proper error handling
7. Add logging and monitoring

## Future Enhancements

- [x] Real-time data from Jira, GitLab, Confluence
- [x] Multi-team support with filtering
- [ ] Export to PDF/Excel
- [ ] Email notifications
- [ ] Custom date ranges
- [ ] Advanced filtering
- [ ] Goal setting and tracking
- [ ] Slack/Teams integration
- [ ] Machine learning predictions
- [ ] Mobile app
- [ ] GitHub integration (in addition to GitLab)
- [ ] Azure DevOps integration

## Contributing

Feel free to fork this project and customize it for your team's needs!

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For questions or issues, please open an issue in the repository.

---
