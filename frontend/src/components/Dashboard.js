import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import axios from 'axios';

ChartJS.register(ArcElement, Tooltip, Legend);

const API_URL = 'http://localhost:5001/api';

function Dashboard({ overview, selectedTeam }) {
  const [timeDistribution, setTimeDistribution] = useState(null);

  useEffect(() => {
    fetchTimeDistribution();
  }, [selectedTeam]);

  const fetchTimeDistribution = async () => {
    try {
      const params = selectedTeam ? { team: selectedTeam } : {};
      const response = await axios.get(`${API_URL}/time-distribution`, { params });
      setTimeDistribution(response.data);
    } catch (error) {
      console.error('Error fetching time distribution:', error);
    }
  };

  if (!overview || !timeDistribution) {
    return <div>Loading...</div>;
  }

  const totalDevTime = timeDistribution.development.user_stories + timeDistribution.development.pull_requests;
  
  const pieData = {
    labels: ['Development', 'Testing', 'Prod Support', 'Prod Issues'],
    datasets: [
      {
        label: 'Hours',
        data: [
          totalDevTime,
          timeDistribution.testing,
          timeDistribution.prod_support,
          timeDistribution.prod_issues
        ],
        backgroundColor: [
          'rgba(54, 162, 235, 0.8)',
          'rgba(75, 192, 192, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(255, 99, 132, 0.8)',
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(255, 99, 132, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const totalTime = totalDevTime + timeDistribution.testing + 
                    timeDistribution.prod_support + timeDistribution.prod_issues;

  const devPercentage = ((totalDevTime / totalTime) * 100).toFixed(1);
  const testPercentage = ((timeDistribution.testing / totalTime) * 100).toFixed(1);
  const supportPercentage = ((timeDistribution.prod_support / totalTime) * 100).toFixed(1);
  const issuesPercentage = ((timeDistribution.prod_issues / totalTime) * 100).toFixed(1);

  return (
    <div className="dashboard">
      <h2>Productivity Overview</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Time Spent</h3>
          <div className="value">{overview.total_time_spent}h</div>
          <div className="label">Across all activities</div>
        </div>
        
        <div className="stat-card">
          <h3>Story Completion</h3>
          <div className="value">{overview.story_completion_rate}%</div>
          <div className="label">{overview.completed_stories} of {overview.total_stories} stories</div>
        </div>
        
        <div className="stat-card">
          <h3>PR Merge Rate</h3>
          <div className="value">{overview.pr_merge_rate}%</div>
          <div className="label">{overview.merged_prs} of {overview.total_prs} PRs</div>
        </div>
        
        <div className="stat-card">
          <h3>Active Prod Issues</h3>
          <div className="value">{overview.active_prod_issues}</div>
          <div className="label">{overview.critical_issues} critical</div>
        </div>
      </div>

      <div className="chart-container">
        <h2>Time Distribution</h2>
        <div style={{ maxWidth: '500px', margin: '0 auto' }}>
          <Pie data={pieData} />
        </div>
        
        <div style={{ marginTop: '30px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
            <div style={{ padding: '15px', background: 'rgba(54, 162, 235, 0.1)', borderRadius: '8px' }}>
              <strong>Development</strong>
              <div style={{ fontSize: '1.5em', color: 'rgba(54, 162, 235, 1)' }}>
                {totalDevTime}h ({devPercentage}%)
              </div>
            </div>
            <div style={{ padding: '15px', background: 'rgba(75, 192, 192, 0.1)', borderRadius: '8px' }}>
              <strong>Testing</strong>
              <div style={{ fontSize: '1.5em', color: 'rgba(75, 192, 192, 1)' }}>
                {timeDistribution.testing}h ({testPercentage}%)
              </div>
            </div>
            <div style={{ padding: '15px', background: 'rgba(255, 206, 86, 0.1)', borderRadius: '8px' }}>
              <strong>Prod Support</strong>
              <div style={{ fontSize: '1.5em', color: 'rgba(255, 206, 86, 1)' }}>
                {timeDistribution.prod_support}h ({supportPercentage}%)
              </div>
            </div>
            <div style={{ padding: '15px', background: 'rgba(255, 99, 132, 0.1)', borderRadius: '8px' }}>
              <strong>Prod Issues</strong>
              <div style={{ fontSize: '1.5em', color: 'rgba(255, 99, 132, 1)' }}>
                {timeDistribution.prod_issues}h ({issuesPercentage}%)
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style={{ marginTop: '30px', padding: '20px', background: '#f0f8ff', borderRadius: '10px' }}>
        <h3>Quick Summary</h3>
        <ul style={{ marginTop: '15px', lineHeight: '2', paddingLeft: '20px' }}>
          <li>Team has completed <strong>{overview.completed_stories}</strong> user stories</li>
          <li><strong>{overview.merged_prs}</strong> pull requests have been merged</li>
          <li><strong>{devPercentage}%</strong> of time is spent on development activities</li>
          <li><strong>{issuesPercentage}%</strong> of time is spent addressing production issues</li>
          {parseFloat(issuesPercentage) > 20 && (
            <li style={{ color: '#dc3545' }}>High production issue time - consider improving quality processes</li>
          )}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
