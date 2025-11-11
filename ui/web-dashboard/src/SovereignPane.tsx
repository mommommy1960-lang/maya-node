// SPDX-License-Identifier: CERL-1.0
// Copyright (c) 2025 MAYA Node Contributors
//
// Constrained Ethics Runtime License 1.0
// This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

/**
 * Sovereign Runtime Dashboard Pane
 * 
 * Displays sovereign AI runtime status, ethics checks, and human oversight controls.
 */

import React, { useState, useEffect } from 'react';
import {
  fetchSovereignStatus,
  fetchEthicsViolations,
  fetchRuntimeOperations,
  SovereignStatus,
  EthicsViolation,
  RuntimeOperation
} from './sovereignApi';

export function SovereignPane() {
  const [status, setStatus] = useState<SovereignStatus | null>(null);
  const [violations, setViolations] = useState<EthicsViolation[]>([]);
  const [operations, setOperations] = useState<RuntimeOperation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    // Refresh every 5 seconds
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  async function loadData() {
    try {
      const [statusData, violationsData, operationsData] = await Promise.all([
        fetchSovereignStatus(),
        fetchEthicsViolations(),
        fetchRuntimeOperations()
      ]);
      
      setStatus(statusData);
      setViolations(violationsData);
      setOperations(operationsData);
      setLoading(false);
    } catch (error) {
      console.error('Error loading sovereign data:', error);
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="sovereign-pane loading">Loading sovereign runtime...</div>;
  }

  return (
    <div className="sovereign-pane">
      <h2>🛡️ Sovereign AI Runtime</h2>
      
      {/* Runtime Status */}
      <section className="status-section">
        <h3>Runtime Status</h3>
        {status && (
          <div className="status-grid">
            <div className="status-item">
              <span className="label">State:</span>
              <span className={`value state-${status.state}`}>{status.state}</span>
            </div>
            <div className="status-item">
              <span className="label">Ethics Checks:</span>
              <span className={`value ${status.ethicsChecksEnabled ? 'enabled' : 'disabled'}`}>
                {status.ethicsChecksEnabled ? '✓ Enabled' : '✗ Disabled'}
              </span>
            </div>
            <div className="status-item">
              <span className="label">Human Oversight:</span>
              <span className={`value ${status.humanOversightEnabled ? 'enabled' : 'disabled'}`}>
                {status.humanOversightEnabled ? '✓ Enabled' : '✗ Disabled'}
              </span>
            </div>
            <div className="status-item">
              <span className="label">Vetted Models:</span>
              <span className="value">{status.vettedModelsCount}</span>
            </div>
            <div className="status-item">
              <span className="label">Iterations:</span>
              <span className="value">{status.iterationCount}</span>
            </div>
          </div>
        )}
      </section>

      {/* Ethics Violations */}
      <section className="violations-section">
        <h3>Ethics Monitoring</h3>
        {violations.length === 0 ? (
          <div className="no-violations">
            ✓ No ethics violations detected
          </div>
        ) : (
          <div className="violations-list">
            {violations.map((v, idx) => (
              <div key={idx} className={`violation severity-${v.severity}`}>
                <span className="severity">{v.severity}</span>
                <span className="constraint">{v.constraint}</span>
                <span className="description">{v.description}</span>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Recent Operations */}
      <section className="operations-section">
        <h3>Recent Operations</h3>
        {operations.length === 0 ? (
          <div className="no-operations">
            No recent operations
          </div>
        ) : (
          <div className="operations-list">
            {operations.map((op) => (
              <div key={op.id} className={`operation status-${op.status}`}>
                <span className="timestamp">
                  {new Date(op.timestamp).toLocaleTimeString()}
                </span>
                <span className="operation-name">{op.operation}</span>
                <span className="status">{op.status}</span>
                {op.ethicsVerified && <span className="verified">✓ Ethics Verified</span>}
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Connection Placeholder */}
      <section className="connection-section">
        <h3>Runtime Connection</h3>
        <div className="connection-status">
          <span className="indicator connecting">●</span>
          <span>Connecting to sovereign runtime...</span>
        </div>
        <div className="connection-info">
          <p>
            <strong>Note:</strong> This is a bootstrap implementation. 
            Full runtime connection will be implemented in next phase.
          </p>
        </div>
      </section>
    </div>
  );
}
