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
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState('');

  useEffect(() => {
    fetchTeams();
  }, []);

  useEffect(() => {
    fetchOverview();
  }, [selectedTeam]);

  const fetchTeams = async () => {
    try {
      const response = await axios.get(`${API_URL}/teams`);
      setTeams(response.data.teams);
    } catch (error) {
      console.error('Error fetching teams:', error);
    }
  };

  const fetchOverview = async () => {
    try {
      const params = selectedTeam ? { team: selectedTeam } : {};
      const response = await axios.get(`${API_URL}/overview`, { params });
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
        <h1>Productivity Tracker</h1>
        <p className="subtitle">Measure, Analyze, and Optimize Team Performance</p>
        <div className="team-selector">
          <label htmlFor="team-select">Filter by Team: </label>
          <select 
            id="team-select"
            value={selectedTeam} 
            onChange={(e) => setSelectedTeam(e.target.value)}
          >
            <option value="">All Teams</option>
            {teams.map((team) => (
              <option key={team} value={team}>{team}</option>
            ))}
          </select>
        </div>
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
        {activeTab === 'dashboard' && <Dashboard overview={overview} selectedTeam={selectedTeam} />}
        {activeTab === 'time' && <TimeDistribution selectedTeam={selectedTeam} />}
        {activeTab === 'team' && <TeamPerformance selectedTeam={selectedTeam} />}
        {activeTab === 'insights' && <Insights selectedTeam={selectedTeam} />}
        {activeTab === 'stories' && <UserStories selectedTeam={selectedTeam} />}
        {activeTab === 'prs' && <PullRequests selectedTeam={selectedTeam} />}
      </main>
    </div>
  );
}

export default App;
