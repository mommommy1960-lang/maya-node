// SPDX-License-Identifier: CERL-1.0
// Copyright (c) 2025 MAYA Node Contributors
//
// Constrained Ethics Runtime License 1.0
// This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

import React, { useState, useEffect } from 'react';
import { SovereignPane } from './SovereignPane';
import { EthicsDecisionViewer } from './EthicsDecisionViewer';
import { AuditHistoryViewer } from './AuditHistoryViewer';
import { login, logout, getCurrentUser, storeAuthState, clearAuthState, User } from './auth';

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [activeTab, setActiveTab] = useState('sovereign');

  useEffect(() => {
    // Check for existing auth
    const currentUser = getCurrentUser();
    if (currentUser) {
      setUser(currentUser);
    }
  }, []);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoginError('');
    
    const result = await login(username, password);
    
    if (result.success && result.user) {
      storeAuthState(result.user);
      setUser(result.user);
      setPassword('');
    } else {
      setLoginError(result.error || 'Login failed');
    }
  }

  function handleLogout() {
    clearAuthState();
    setUser(null);
    logout();
  }

  // Login screen
  if (!user) {
    return (
      <div className="login-screen">
        <div className="login-box">
          <h1>🛡️ MAYA Node Dashboard</h1>
          <p className="subtitle">Sovereign Architecture - Bootstrap Phase</p>
          
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username"
                autoComplete="username"
              />
            </div>
            
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                autoComplete="current-password"
              />
            </div>
            
            {loginError && <div className="error">{loginError}</div>}
            
            <button type="submit">Login</button>
          </form>
          
          <div className="login-note">
            <p><strong>Note:</strong> This is a bootstrap authentication stub.</p>
            <p>Any credentials will be accepted for development.</p>
          </div>
        </div>
      </div>
    );
  }

  // Main dashboard
  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>🛡️ MAYA Node Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user.username}</span>
          <span className="role">({user.role})</span>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </header>

      <nav className="dashboard-nav">
        <button
          className={activeTab === 'sovereign' ? 'active' : ''}
          onClick={() => setActiveTab('sovereign')}
        >
          Sovereign Runtime
        </button>
        <button
          className={activeTab === 'ethics' ? 'active' : ''}
          onClick={() => setActiveTab('ethics')}
        >
          Ethics Decisions
        </button>
        <button
          className={activeTab === 'audit' ? 'active' : ''}
          onClick={() => setActiveTab('audit')}
        >
          Audit History
        </button>
        <button
          className={activeTab === 'status' ? 'active' : ''}
          onClick={() => setActiveTab('status')}
        >
          System Status
        </button>
        <button
          className={activeTab === 'telemetry' ? 'active' : ''}
          onClick={() => setActiveTab('telemetry')}
        >
          Telemetry
        </button>
      </nav>

      <main className="dashboard-content">
        {activeTab === 'sovereign' && <SovereignPane />}
        {activeTab === 'ethics' && <EthicsDecisionViewer />}
        {activeTab === 'audit' && <AuditHistoryViewer />}
        {activeTab === 'status' && (
          <div className="placeholder-pane">
            <h2>System Status</h2>
            <p>TODO: Show SOC, power status, system health</p>
          </div>
        )}
        {activeTab === 'telemetry' && (
          <div className="placeholder-pane">
            <h2>Telemetry</h2>
            <p>TODO: Show real-time telemetry data</p>
          </div>
        )}
      </main>

      <footer className="dashboard-footer">
        <p>MAYA Node - Sovereign Architecture Phase Omega</p>
        <p>Licensed under CERL-1.0 | No unvetted AI models</p>
      </footer>
    </div>
  );
}

export default App;
