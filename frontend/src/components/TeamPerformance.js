import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const API_URL = 'http://localhost:5001/api';

function TeamPerformance() {
  const [teamData, setTeamData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('productivity_score');

  useEffect(() => {
    fetchTeamPerformance();
  }, []);

  const fetchTeamPerformance = async () => {
    try {
      const response = await axios.get(`${API_URL}/team-performance`);
      setTeamData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching team performance:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading team performance...</div>;
  }

  const sortedData = [...teamData].sort((a, b) => b[sortBy] - a[sortBy]);

  return (
    <div className="team-performance">
      <h2>👥 Team Performance</h2>
      <p style={{ marginBottom: '30px', color: '#666' }}>
        Individual team member productivity metrics and contributions
      </p>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ marginRight: '10px', fontWeight: 'bold' }}>Sort by:</label>
        <select 
          value={sortBy} 
          onChange={(e) => setSortBy(e.target.value)}
          style={{ padding: '8px 15px', borderRadius: '5px', border: '1px solid #ddd' }}
        >
          <option value="productivity_score">Productivity Score</option>
          <option value="total_time">Total Time</option>
          <option value="stories_completed">Stories Completed</option>
          <option value="prs_merged">PRs Merged</option>
        </select>
      </div>

      <div className="chart-container">
        <h3>Productivity Score by Team Member</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={sortedData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="productivity_score" fill="#667eea" name="Productivity Score" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Team Member</th>
              <th>Total Time (h)</th>
              <th>Stories Done</th>
              <th>PRs Merged</th>
              <th>Tests</th>
              <th>Support Tickets</th>
              <th>Issues Resolved</th>
              <th>Productivity Score</th>
            </tr>
          </thead>
          <tbody>
            {sortedData.map((member, index) => (
              <tr key={index}>
                <td><strong>{member.name}</strong></td>
                <td>{member.total_time}</td>
                <td>{member.stories_completed}</td>
                <td>{member.prs_merged}</td>
                <td>{member.tests_done}</td>
                <td>{member.support_tickets}</td>
                <td>{member.issues_resolved}</td>
                <td>
                  <span style={{ 
                    padding: '5px 10px', 
                    borderRadius: '15px', 
                    background: member.productivity_score > 3 ? '#d4edda' : 
                               member.productivity_score > 2 ? '#fff3cd' : '#f8d7da',
                    fontWeight: 'bold'
                  }}>
                    {member.productivity_score}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ marginTop: '30px', padding: '20px', background: '#f8f9fa', borderRadius: '10px' }}>
        <h3>📌 Productivity Score Calculation</h3>
        <p style={{ lineHeight: '1.8', marginTop: '10px' }}>
          The productivity score is calculated based on:
        </p>
        <ul style={{ marginTop: '10px', paddingLeft: '20px', lineHeight: '2' }}>
          <li><strong>Stories Completed:</strong> 10 points per story</li>
          <li><strong>PRs Merged:</strong> 8 points per PR</li>
          <li><strong>Tests Passed:</strong> 5 points per test</li>
          <li><strong>Support Resolved:</strong> 3 points per ticket</li>
          <li><strong>Issues Resolved:</strong> 15 points per issue</li>
          <li>Score is then normalized by total time spent</li>
        </ul>
      </div>
    </div>
  );
}

export default TeamPerformance;
