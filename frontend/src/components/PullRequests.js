import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5001/api';

function PullRequests() {
  const [data, setData] = useState(null);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPullRequests();
  }, []);

  const fetchPullRequests = async () => {
    try {
      const response = await axios.get(`${API_URL}/pull-requests`);
      setData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching pull requests:', error);
      setLoading(false);
    }
  };

  if (loading || !data) {
    return <div>Loading pull requests...</div>;
  }

  const filteredPRs = filter === 'all' 
    ? data.prs 
    : data.prs.filter(pr => pr.status === filter);

  const getStatusClass = (status) => {
    const statusMap = {
      'Merged': 'merged',
      'Approved': 'resolved',
      'Under Review': 'in-progress',
      'Open': 'open',
      'Changes Requested': 'open',
      'Closed': 'open'
    };
    return statusMap[status] || 'open';
  };

  return (
    <div className="pull-requests">
      <h2>🔀 Pull Requests</h2>
      <p style={{ marginBottom: '30px', color: '#666' }}>
        Track all pull requests and review status
      </p>

      <div className="stats-grid">
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <h3>Total PRs</h3>
          <div className="value">{data.total}</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #28a745 0%, #20c997 100%)' }}>
          <h3>Merged</h3>
          <div className="value">{data.merged}</div>
          <div className="label">{((data.merged / data.total) * 100).toFixed(1)}% merge rate</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #ffc107 0%, #ff9800 100%)' }}>
          <h3>Open</h3>
          <div className="value">{data.open}</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #17a2b8 0%, #3498db 100%)' }}>
          <h3>Avg Time</h3>
          <div className="value">
            {(data.prs.reduce((sum, pr) => sum + pr.time_spent, 0) / data.total).toFixed(1)}h
          </div>
          <div className="label">per PR</div>
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
          <option value="Merged">Merged ({data.merged})</option>
          <option value="Open">Open ({data.open})</option>
          <option value="Under Review">Under Review</option>
          <option value="Approved">Approved</option>
          <option value="Changes Requested">Changes Requested</option>
        </select>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Status</th>
              <th>Author</th>
              <th>Reviewer</th>
              <th>Created</th>
              <th>Time (h)</th>
              <th>+Lines</th>
              <th>-Lines</th>
              <th>Comments</th>
              <th>Commits</th>
            </tr>
          </thead>
          <tbody>
            {filteredPRs.map((pr, index) => (
              <tr key={index}>
                <td><strong>{pr.id}</strong></td>
                <td>{pr.title}</td>
                <td>
                  <span className={`status-badge ${getStatusClass(pr.status)}`}>
                    {pr.status}
                  </span>
                </td>
                <td>{pr.author}</td>
                <td>{pr.reviewer}</td>
                <td>{pr.created_date}</td>
                <td>{pr.time_spent}</td>
                <td style={{ color: '#28a745' }}>+{pr.lines_added}</td>
                <td style={{ color: '#dc3545' }}>-{pr.lines_deleted}</td>
                <td>{pr.comments}</td>
                <td>{pr.commits}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredPRs.length === 0 && (
        <div style={{ padding: '40px', textAlign: 'center', background: '#f8f9fa', borderRadius: '10px', marginTop: '20px' }}>
          <p>No pull requests found with the selected filter.</p>
        </div>
      )}

      <div style={{ marginTop: '30px', padding: '20px', background: '#f0f8ff', borderRadius: '10px' }}>
        <h3>📊 PR Statistics</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', marginTop: '15px' }}>
          <div>
            <strong>Total Lines Changed:</strong><br/>
            {data.prs.reduce((sum, pr) => sum + pr.lines_added + pr.lines_deleted, 0).toLocaleString()}
          </div>
          <div>
            <strong>Total Comments:</strong><br/>
            {data.prs.reduce((sum, pr) => sum + pr.comments, 0)}
          </div>
          <div>
            <strong>Total Commits:</strong><br/>
            {data.prs.reduce((sum, pr) => sum + pr.commits, 0)}
          </div>
          <div>
            <strong>Avg Lines/PR:</strong><br/>
            {(data.prs.reduce((sum, pr) => sum + pr.lines_added + pr.lines_deleted, 0) / data.total).toFixed(0)}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PullRequests;
