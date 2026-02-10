import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import TimeDistribution from './components/TimeDistribution';
import TeamPerformance from './components/TeamPerformance';
import Insights from './components/Insights';
import UserStories from './components/UserStories';
import PullRequests from './components/PullRequests';
import axios from 'axios';

const API_URL = 'http://localhost:5001/api';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [overview, setOverview] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOverview();
  }, []);

  const fetchOverview = async () => {
    try {
      const response = await axios.get(`${API_URL}/overview`);
      setOverview(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching overview:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading productivity data...</p>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>📊 Productivity Tracker</h1>
        <p className="subtitle">Measure, Analyze, and Optimize Team Performance</p>
      </header>

      <nav className="nav-tabs">
        <button 
          className={activeTab === 'dashboard' ? 'active' : ''} 
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button 
          className={activeTab === 'time' ? 'active' : ''} 
          onClick={() => setActiveTab('time')}
        >
          Time Distribution
        </button>
        <button 
          className={activeTab === 'team' ? 'active' : ''} 
          onClick={() => setActiveTab('team')}
        >
          Team Performance
        </button>
        <button 
          className={activeTab === 'insights' ? 'active' : ''} 
          onClick={() => setActiveTab('insights')}
        >
          Insights
        </button>
        <button 
          className={activeTab === 'stories' ? 'active' : ''} 
          onClick={() => setActiveTab('stories')}
        >
          User Stories
        </button>
        <button 
          className={activeTab === 'prs' ? 'active' : ''} 
          onClick={() => setActiveTab('prs')}
        >
          Pull Requests
        </button>
      </nav>

      <main className="content">
        {activeTab === 'dashboard' && <Dashboard overview={overview} />}
        {activeTab === 'time' && <TimeDistribution />}
        {activeTab === 'team' && <TeamPerformance />}
        {activeTab === 'insights' && <Insights />}
        {activeTab === 'stories' && <UserStories />}
        {activeTab === 'prs' && <PullRequests />}
      </main>
    </div>
  );
}

export default App;
