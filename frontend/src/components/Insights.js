import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5001/api';

function Insights({ selectedTeam }) {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInsights();
  }, [selectedTeam]);

  const fetchInsights = async () => {
    try {
      const params = selectedTeam ? { team: selectedTeam } : {};
      const response = await axios.get(`${API_URL}/insights`, { params });
      setInsights(response.data.insights);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching insights:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading insights...</div>;
  }

  const getIcon = (type) => {
    switch(type) {
      case 'success': return '';
      case 'warning': return '';
      case 'critical': return '';
      default: return '';
    }
  };

  return (
    <div className="insights">
      <h2>Productivity Insights</h2>
      <p style={{ marginBottom: '30px', color: '#666' }}>
        AI-powered analysis of your team's productivity patterns and recommendations
      </p>

      {insights.length === 0 ? (
        <div style={{ padding: '40px', textAlign: 'center', background: '#f8f9fa', borderRadius: '10px' }}>
          <h3>Great Job!</h3>
          <p>No critical issues detected. Your team is working efficiently!</p>
        </div>
      ) : (
        <div>
          {insights.map((insight, index) => (
            <div key={index} className={`insight-card ${insight.type}`}>
              <h3>{getIcon(insight.type)} {insight.title}</h3>
              <p>{insight.message}</p>
              {insight.value && (
                <div style={{ marginTop: '10px', fontSize: '1.2em', fontWeight: 'bold' }}>
                  Metric: {insight.value.toFixed(1)}{insight.title.includes('Time') ? 'h' : '%'}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div style={{ marginTop: '40px' }}>
        <h3>Recommendations</h3>
        <div style={{ marginTop: '20px' }}>
          <div style={{ padding: '20px', marginBottom: '15px', background: '#e8f5e9', borderRadius: '10px', borderLeft: '5px solid #4caf50' }}>
            <strong>Best Practices</strong>
            <ul style={{ marginTop: '10px', paddingLeft: '20px', lineHeight: '1.8' }}>
              <li>Aim for 50-60% time on development activities</li>
              <li>Keep testing time around 15-20% for quality assurance</li>
              <li>Production support should ideally be under 15%</li>
              <li>Production issues should not exceed 10% of total time</li>
            </ul>
          </div>

          <div style={{ padding: '20px', marginBottom: '15px', background: '#fff3e0', borderRadius: '10px', borderLeft: '5px solid #ff9800' }}>
            <strong>Action Items</strong>
            <ul style={{ marginTop: '10px', paddingLeft: '20px', lineHeight: '1.8' }}>
              <li>Review production issues to identify patterns</li>
              <li>Implement automated testing to catch issues early</li>
              <li>Set up monitoring and alerting for proactive issue detection</li>
              <li>Conduct regular code reviews to maintain quality</li>
              <li>Document common issues to reduce support time</li>
            </ul>
          </div>

          <div style={{ padding: '20px', background: '#e3f2fd', borderRadius: '10px', borderLeft: '5px solid #2196f3' }}>
            <strong>Improvement Areas</strong>
            <ul style={{ marginTop: '10px', paddingLeft: '20px', lineHeight: '1.8' }}>
              <li>Reduce context switching between tasks</li>
              <li>Allocate dedicated time blocks for each activity type</li>
              <li>Create knowledge base to reduce recurring support queries</li>
              <li>Implement CI/CD to streamline deployment process</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Insights;
