import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5001/api';

function UserStories({ selectedTeam }) {
  const [data, setData] = useState(null);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserStories();
  }, [selectedTeam]);

  const fetchUserStories = async () => {
    try {
      const params = selectedTeam ? { team: selectedTeam } : {};
      const response = await axios.get(`${API_URL}/user-stories`, { params });
      setData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching user stories:', error);
      setLoading(false);
    }
  };

  if (loading || !data) {
    return <div>Loading user stories...</div>;
  }

  const filteredStories = filter === 'all' 
    ? data.stories 
    : data.stories.filter(s => s.status === filter);

  const getStatusClass = (status) => {
    const statusMap = {
      'Done': 'done',
      'In Progress': 'in-progress',
      'Code Review': 'in-progress',
      'Testing': 'in-progress',
      'To Do': 'open'
    };
    return statusMap[status] || 'open';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      'Critical': '#dc3545',
      'High': '#fd7e14',
      'Medium': '#ffc107',
      'Low': '#28a745'
    };
    return colors[priority] || '#6c757d';
  };

  return (
    <div className="user-stories">
      <h2>User Stories</h2>
      <p style={{ marginBottom: '30px', color: '#666' }}>
        Track all user stories and their current status
      </p>

      <div className="stats-grid">
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <h3>Total Stories</h3>
          <div className="value">{data.total}</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #28a745 0%, #20c997 100%)' }}>
          <h3>Completed</h3>
          <div className="value">{data.completed}</div>
          <div className="label">{((data.completed / data.total) * 100).toFixed(1)}%</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #17a2b8 0%, #3498db 100%)' }}>
          <h3>In Progress</h3>
          <div className="value">{data.in_progress}</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #ffc107 0%, #ff9800 100%)' }}>
          <h3>Remaining</h3>
          <div className="value">{data.total - data.completed}</div>
        </div>
      </div>

      <div style={{ marginBottom: '20px', marginTop: '20px' }}>
        <label style={{ marginRight: '10px', fontWeight: 'bold' }}>Filter by Status:</label>
        <select 
          value={filter} 
          onChange={(e) => setFilter(e.target.value)}
          style={{ padding: '8px 15px', borderRadius: '5px', border: '1px solid #ddd' }}
        >
          <option value="all">All ({data.total})</option>
          <option value="Done">Done ({data.completed})</option>
          <option value="In Progress">In Progress ({data.in_progress})</option>
          <option value="Code Review">Code Review</option>
          <option value="Testing">Testing</option>
          <option value="To Do">To Do</option>
        </select>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Type</th>
              <th>Status</th>
              <th>Assignee</th>
              <th>Priority</th>
              <th>Story Points</th>
              <th>Time Spent (h)</th>
              <th>Created Date</th>
            </tr>
          </thead>
          <tbody>
            {filteredStories.map((story, index) => (
              <tr key={index}>
                <td><strong>{story.id}</strong></td>
                <td>{story.title}</td>
                <td>{story.type}</td>
                <td>
                  <span className={`status-badge ${getStatusClass(story.status)}`}>
                    {story.status}
                  </span>
                </td>
                <td>{story.assignee}</td>
                <td>
                  <span style={{ 
                    color: getPriorityColor(story.priority), 
                    fontWeight: 'bold' 
                  }}>
                    {story.priority}
                  </span>
                </td>
                <td style={{ textAlign: 'center' }}>{story.story_points}</td>
                <td>{story.time_spent}</td>
                <td>{story.created_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredStories.length === 0 && (
        <div style={{ padding: '40px', textAlign: 'center', background: '#f8f9fa', borderRadius: '10px', marginTop: '20px' }}>
          <p>No stories found with the selected filter.</p>
        </div>
      )}
    </div>
  );
}

export default UserStories;
