import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart
} from 'recharts';

const API_URL = 'http://localhost:5001/api';

function TimeDistribution({ selectedTeam }) {
  const [trends, setTrends] = useState(null);
  const [period, setPeriod] = useState(30);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrends();
  }, [period, selectedTeam]);

  const fetchTrends = async () => {
    try {
      const params = { days: period };
      if (selectedTeam) params.team = selectedTeam;
      const response = await axios.get(`${API_URL}/trends`, { params });
      setTrends(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching trends:', error);
      setLoading(false);
    }
  };

  if (loading || !trends) {
    return <div>Loading time distribution...</div>;
  }

  const chartData = trends.dates.map(date => ({
    date: date,
    Development: trends.data[date].development.toFixed(1),
    Testing: trends.data[date].testing.toFixed(1),
    'Prod Support': trends.data[date].prod_support.toFixed(1),
    'Prod Issues': trends.data[date].prod_issues.toFixed(1),
  }));

  const totalByCategory = {
    development: 0,
    testing: 0,
    prod_support: 0,
    prod_issues: 0
  };

  Object.values(trends.data).forEach(day => {
    totalByCategory.development += day.development;
    totalByCategory.testing += day.testing;
    totalByCategory.prod_support += day.prod_support;
    totalByCategory.prod_issues += day.prod_issues;
  });

  const grandTotal = Object.values(totalByCategory).reduce((a, b) => a + b, 0);

  return (
    <div className="time-distribution">
      <h2>Time Distribution Analysis</h2>
      <p style={{ marginBottom: '30px', color: '#666' }}>
        Visualize how time is allocated across different activities over time
      </p>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ marginRight: '10px', fontWeight: 'bold' }}>Time Period:</label>
        <select 
          value={period} 
          onChange={(e) => setPeriod(Number(e.target.value))}
          style={{ padding: '8px 15px', borderRadius: '5px', border: '1px solid #ddd' }}
        >
          <option value={7}>Last 7 Days</option>
          <option value={14}>Last 14 Days</option>
          <option value={30}>Last 30 Days</option>
        </select>
      </div>

      <div className="stats-grid">
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #36a2eb 0%, #1e88e5 100%)' }}>
          <h3>Development</h3>
          <div className="value">{totalByCategory.development.toFixed(1)}h</div>
          <div className="label">{((totalByCategory.development / grandTotal) * 100).toFixed(1)}% of total</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #4bc0c0 0%, #26a69a 100%)' }}>
          <h3>Testing</h3>
          <div className="value">{totalByCategory.testing.toFixed(1)}h</div>
          <div className="label">{((totalByCategory.testing / grandTotal) * 100).toFixed(1)}% of total</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #ffce56 0%, #ffa726 100%)' }}>
          <h3>Prod Support</h3>
          <div className="value">{totalByCategory.prod_support.toFixed(1)}h</div>
          <div className="label">{((totalByCategory.prod_support / grandTotal) * 100).toFixed(1)}% of total</div>
        </div>
        
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #ff6384 0%, #e53935 100%)' }}>
          <h3>Prod Issues</h3>
          <div className="value">{totalByCategory.prod_issues.toFixed(1)}h</div>
          <div className="label">{((totalByCategory.prod_issues / grandTotal) * 100).toFixed(1)}% of total</div>
        </div>
      </div>

      <div className="chart-container">
        <h3>Daily Time Distribution Trend</h3>
        <ResponsiveContainer width="100%" height={400}>
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Area type="monotone" dataKey="Development" stackId="1" stroke="#36a2eb" fill="#36a2eb" />
            <Area type="monotone" dataKey="Testing" stackId="1" stroke="#4bc0c0" fill="#4bc0c0" />
            <Area type="monotone" dataKey="Prod Support" stackId="1" stroke="#ffce56" fill="#ffce56" />
            <Area type="monotone" dataKey="Prod Issues" stackId="1" stroke="#ff6384" fill="#ff6384" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-container" style={{ marginTop: '30px' }}>
        <h3>Time Trend Lines</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="Development" stroke="#36a2eb" strokeWidth={2} />
            <Line type="monotone" dataKey="Testing" stroke="#4bc0c0" strokeWidth={2} />
            <Line type="monotone" dataKey="Prod Support" stroke="#ffce56" strokeWidth={2} />
            <Line type="monotone" dataKey="Prod Issues" stroke="#ff6384" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ marginTop: '30px', padding: '20px', background: '#f0f8ff', borderRadius: '10px' }}>
        <h3>Analysis</h3>
        <ul style={{ marginTop: '15px', lineHeight: '2', paddingLeft: '20px' }}>
          <li>Total time tracked: <strong>{grandTotal.toFixed(1)} hours</strong></li>
          <li>Average daily time: <strong>{(grandTotal / period).toFixed(1)} hours</strong></li>
          <li>Most time spent on: <strong>
            {Object.entries(totalByCategory).reduce((a, b) => totalByCategory[a[0]] > totalByCategory[b[0]] ? a : b)[0].replace('_', ' ')}
          </strong></li>
          {((totalByCategory.prod_issues / grandTotal) * 100) > 15 && (
            <li style={{ color: '#dc3545' }}>Production issues consuming significant time - review quality processes</li>
          )}
          {((totalByCategory.development / grandTotal) * 100) > 60 && (
            <li style={{ color: '#28a745' }}>Good focus on development work</li>
          )}
        </ul>
      </div>
    </div>
  );
}

export default TimeDistribution;
