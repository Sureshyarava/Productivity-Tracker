# Quick Setup Guide

## One-Time Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### API Configuration (Optional)
The system works with mock data by default. To use real data from Jira, GitLab, and Confluence:

1. Copy the environment template:
```bash
cd backend
cp .env.example .env
```

2. Edit `.env` with your credentials:
```bash
# Jira Configuration
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token
JIRA_PROJECT_KEY=PROJ

# GitLab Configuration
GITLAB_URL=https://gitlab.com
GITLAB_TOKEN=your_gitlab_personal_access_token
GITLAB_PROJECT_IDS=12345,67890

# Confluence Configuration
CONFLUENCE_URL=https://your-domain.atlassian.net/wiki
CONFLUENCE_EMAIL=your-email@example.com
CONFLUENCE_API_TOKEN=your_confluence_api_token
CONFLUENCE_SPACE_KEY=SPACE

# Team Configuration
TEAMS=Team Alpha,Team Beta,Team Gamma

# Cache settings (in seconds)
CACHE_EXPIRY=300
```

#### How to Get API Tokens

**Jira API Token:**
1. Visit https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name (e.g., "Progress Tracker")
4. Copy the token immediately (you won't see it again)

**GitLab Personal Access Token:**
1. Go to GitLab > User Settings > Access Tokens
2. Create a token with these scopes:
   - `read_api`
   - `read_repository`
3. Copy the token

**Confluence API Token:**
- Use the same token as Jira (if using Atlassian Cloud)
- Or generate a separate token following the Jira steps

**GitLab Project IDs:**
1. Go to your GitLab project
2. Look under the project name - you'll see "Project ID: 12345"
3. For multiple projects, separate IDs with commas: `12345,67890,11111`

### Frontend
```bash
cd frontend
npm install
```

## Running the Application

### Terminal 1 - Backend (FastAPI)
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

Backend runs on: http://localhost:5001

### Terminal 2 - Frontend
```bash
cd frontend
npm start
```

## Access the Application
Open your browser and go to: http://localhost:3000

## Features

### Multi-Team Support
- Use the team selector dropdown in the header to filter by team
- Select "All Teams" to view combined metrics
- All views (Dashboard, Time Distribution, Team Performance, Insights, User Stories, Pull Requests) support team filtering

### Available Teams
- Team Alpha
- Team Beta
- Team Gamma

## Verifying API Connections

Once you've configured your `.env` file and started the backend, verify your API integrations:

### Check Connection Status
Visit: http://localhost:5001/api/status

You should see a response like:
```json
{
  "use_mock_data": false,
  "jira_enabled": true,
  "gitlab_enabled": true,
  "confluence_enabled": true,
  "teams": ["Team Alpha", "Team Beta", "Team Gamma"]
}
```

- `use_mock_data: false` - Real API data is being used
- `use_mock_data: true` - Mock data is being used (APIs not configured)
- `jira_enabled`, `gitlab_enabled`, `confluence_enabled` - Shows which APIs are connected

### Testing Individual APIs

**Test Jira Connection:**
```bash
curl http://localhost:5001/api/user-stories
```

**Test GitLab Connection:**
```bash
curl http://localhost:5001/api/pull-requests
```

### Common API Issues

1. **Authentication Failed**: Double-check your API tokens in `.env`
2. **Project Not Found**: Verify `JIRA_PROJECT_KEY` and `GITLAB_PROJECT_IDS`
3. **Permission Denied**: Ensure your API tokens have the correct scopes/permissions
4. **Data Not Showing**: Check that your Jira/GitLab projects have team labels matching the `TEAMS` configuration

## Troubleshooting

### Port Already in Use
**Backend (Port 5001):**
```bash
lsof -ti:5001 | xargs kill -9  # macOS/Linux
```

**Frontend (Port 3000):**
- The browser will prompt to use a different port (e.g., 3001)

### CORS Issues
Make sure the backend is running before starting the frontend.

### Module Not Found
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## Data Sources

### Mock Data (Default)
If no API credentials are configured, the application uses mock data including:
- 10 User Stories across 3 teams
- 10 Merge Requests across 3 teams
- 10 Test Cases across 3 teams
- 10 Support Tickets across 3 teams
- 10 Production Issues across 3 teams

Perfect for exploring features without API setup!

### Real Data (With API Configuration)
When API credentials are configured in `.env`:
- **User Stories**: Fetched from Jira issues with type "Story" or "Task"
- **Testing Activities**: Jira issues with type "Test" or "Bug" 
- **Support Tickets**: Jira issues with type "Support" or custom support labels
- **Production Issues**: Jira issues with "Production" label or in "Bug" category
- **Merge Requests**: GitLab merge requests from configured projects
- **Pipeline Stats**: CI/CD metrics from GitLab
- **Documentation**: Confluence page updates and collaboration metrics

### Team Assignment
The system automatically assigns items to teams based on:
- **Jira**: Labels, custom fields, or components containing team names
- **GitLab**: Labels on merge requests
- **Confluence**: Page labels

Ensure your Jira/GitLab items are labeled with team names matching your `TEAMS` configuration.
