# 📊 Productivity Tracker

A comprehensive productivity tracking tool that measures team performance across multiple dimensions including user stories, GitHub pull requests, testing activities, production support, and production issues. Get actionable insights to identify bottlenecks and optimize team productivity.

## 🎯 Features

- **Dashboard Overview**: Real-time metrics and KPIs at a glance
- **Time Distribution Analysis**: Visualize how time is spent across different activities
- **Team Performance Tracking**: Individual team member productivity metrics
- **AI-Powered Insights**: Automated analysis and recommendations
- **User Stories Tracking**: Monitor story completion and progress
- **Pull Request Management**: Track PR status and review times
- **Testing Activities**: Monitor test coverage and results
- **Production Support**: Track support tickets and resolution times
- **Production Issues**: Monitor and analyze production incidents

## 🏗️ Architecture

### Backend (Python/Flask)
- RESTful API with multiple endpoints
- Fake data generation for demonstration
- Productivity metrics calculation
- Time distribution analysis
- Team performance analytics

### Frontend (React)
- Modern, responsive dashboard
- Interactive data visualizations (Chart.js, Recharts)
- Multiple views for different metrics
- Real-time data updates

## 📁 Project Structure

```
Progress-Tracker/
├── backend/
│   ├── app.py              # Flask API server
│   ├── models.py           # Data models and fake data generation
│   └── requirements.txt    # Python dependencies
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

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

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

4. Start the Flask server:
```bash
python app.py
```

The backend API will run on `http://localhost:5000`

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

## 📊 API Endpoints

### Overview & Metrics
- `GET /api/overview` - Overall productivity metrics
- `GET /api/time-distribution?period=week` - Time distribution analysis
- `GET /api/team-performance` - Team member performance metrics
- `GET /api/insights` - AI-generated insights and recommendations
- `GET /api/trends?days=30` - Productivity trends over time

### Data Endpoints
- `GET /api/user-stories` - All user stories with status
- `GET /api/pull-requests` - All pull requests
- `GET /api/testing` - Testing activities
- `GET /api/prod-support` - Production support tickets
- `GET /api/prod-issues` - Production issues

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

## 💡 Insights & Recommendations

The system automatically analyzes productivity patterns and provides insights such as:

- **High Production Support Time**: Warns when support consumes >25% of time
- **Excessive Production Issues**: Alerts when issues take >20% of time
- **Low Testing Coverage**: Flags when testing is <15% of time
- **Good Development Focus**: Confirms when development is >50% of time
- **Long PR Review Times**: Identifies slow review processes

## 🎯 Productivity Score Calculation

The productivity score for each team member is calculated based on:

- **Stories Completed**: 10 points per story
- **PRs Merged**: 8 points per PR
- **Tests Passed**: 5 points per test
- **Support Resolved**: 3 points per ticket
- **Issues Resolved**: 15 points per issue

Score is normalized by total time spent for fair comparison.

## 🔧 Customization

### Adding Real Data
Replace the fake data generation in `backend/models.py` with connections to your actual data sources:

- **User Stories**: Jira, Azure DevOps, GitHub Projects
- **Pull Requests**: GitHub API, GitLab API, Bitbucket API
- **Testing**: Test automation frameworks (Jest, Pytest, etc.)
- **Support**: Zendesk, ServiceNow, Freshdesk APIs
- **Production Issues**: PagerDuty, Datadog, New Relic

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

## 🛠️ Technologies Used

### Backend
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **Python**: Core language

### Frontend
- **React**: UI library
- **Chart.js**: Pie/doughnut charts
- **Recharts**: Line/bar/area charts
- **Axios**: HTTP client
- **CSS3**: Styling

## 🔒 Security Considerations

For production deployment:
1. Add authentication and authorization
2. Implement rate limiting
3. Use environment variables for configuration
4. Enable HTTPS
5. Add input validation
6. Implement proper error handling
7. Add logging and monitoring

## 📝 Future Enhancements

- [ ] Real-time data sync
- [ ] Export to PDF/Excel
- [ ] Email notifications
- [ ] Custom date ranges
- [ ] Advanced filtering
- [ ] Goal setting and tracking
- [ ] Slack/Teams integration
- [ ] Machine learning predictions
- [ ] Mobile app
- [ ] Multi-team support

## 🤝 Contributing

Feel free to fork this project and customize it for your team's needs!

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 📧 Support

For questions or issues, please open an issue in the repository.

---

**Made with ❤️ for productive teams**
