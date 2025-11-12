// SPDX-License-Identifier: CERL-1.0
// Copyright (c) 2025 MAYA Node Contributors
//
// Constrained Ethics Runtime License 1.0
// This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

/**
 * Ethics Decision Viewer Component
 * 
 * Displays ethics engine decisions, violations, and constraint checks.
 */

import React, { useState, useEffect } from 'react';

export interface EthicsDecision {
  id: string;
  timestamp: number;
  operation: string;
  constraints_checked: string[];
  violations: EthicsViolation[];
  decision: 'approved' | 'rejected' | 'flagged';
  human_review_required: boolean;
}

export interface EthicsViolation {
  severity: 'info' | 'warning' | 'error' | 'critical';
  constraint: string;
  description: string;
  recommendation?: string;
}

interface EthicsViewerProps {
  decisions?: EthicsDecision[];
  autoRefresh?: boolean;
  refreshInterval?: number;
}

export function EthicsDecisionViewer({ 
  decisions = [], 
  autoRefresh = true,
  refreshInterval = 5000 
}: EthicsViewerProps) {
  const [ethicsData, setEthicsData] = useState<EthicsDecision[]>(decisions);
  const [selectedDecision, setSelectedDecision] = useState<EthicsDecision | null>(null);
  const [filter, setFilter] = useState<'all' | 'approved' | 'rejected' | 'flagged'>('all');

  useEffect(() => {
    if (decisions.length > 0) {
      setEthicsData(decisions);
    } else {
      // Load mock data for development
      loadMockData();
    }

    if (autoRefresh) {
      const interval = setInterval(() => {
        // TODO: Fetch real data from API
        console.log('Refreshing ethics data...');
      }, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [decisions, autoRefresh, refreshInterval]);

  function loadMockData() {
    const mockDecisions: EthicsDecision[] = [
      {
        id: 'eth_001',
        timestamp: Date.now() - 300000,
        operation: 'process_data',
        constraints_checked: [
          'no_weaponization',
          'no_surveillance',
          'no_harm',
          'require_transparency'
        ],
        violations: [],
        decision: 'approved',
        human_review_required: false
      },
      {
        id: 'eth_002',
        timestamp: Date.now() - 120000,
        operation: 'analyze_patterns',
        constraints_checked: [
          'no_manipulation',
          'no_discrimination',
          'respect_autonomy'
        ],
        violations: [
          {
            severity: 'warning',
            constraint: 'require_transparency',
            description: 'AI operation lacks explanation',
            recommendation: 'Add explanation field for transparency'
          }
        ],
        decision: 'flagged',
        human_review_required: true
      },
      {
        id: 'eth_003',
        timestamp: Date.now() - 60000,
        operation: 'optimize_energy',
        constraints_checked: [
          'no_weaponization',
          'no_harm',
          'require_auditability'
        ],
        violations: [],
        decision: 'approved',
        human_review_required: false
      }
    ];
    setEthicsData(mockDecisions);
  }

  function formatTimestamp(timestamp: number): string {
    const date = new Date(timestamp);
    return date.toLocaleString();
  }

  function getDecisionColor(decision: string): string {
    switch (decision) {
      case 'approved':
        return '#4caf50';
      case 'rejected':
        return '#f44336';
      case 'flagged':
        return '#ff9800';
      default:
        return '#9e9e9e';
    }
  }

  function getSeverityColor(severity: string): string {
    switch (severity) {
      case 'critical':
        return '#d32f2f';
      case 'error':
        return '#f44336';
      case 'warning':
        return '#ff9800';
      case 'info':
        return '#2196f3';
      default:
        return '#9e9e9e';
    }
  }

  const filteredDecisions = ethicsData.filter(d => 
    filter === 'all' || d.decision === filter
  );

  return (
    <div className="ethics-decision-viewer">
      <div className="ethics-header">
        <h3>🛡️ Ethics Decision Viewer</h3>
        <div className="ethics-filter">
          <label>Filter:</label>
          <select value={filter} onChange={(e) => setFilter(e.target.value as any)}>
            <option value="all">All Decisions</option>
            <option value="approved">Approved</option>
            <option value="flagged">Flagged</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>
      </div>

      <div className="ethics-content">
        <div className="decisions-list">
          <h4>Recent Decisions ({filteredDecisions.length})</h4>
          {filteredDecisions.length === 0 ? (
            <div className="no-decisions">
              No ethics decisions to display
            </div>
          ) : (
            <div className="decisions-grid">
              {filteredDecisions.map((decision) => (
                <div
                  key={decision.id}
                  className={`decision-card ${selectedDecision?.id === decision.id ? 'selected' : ''}`}
                  onClick={() => setSelectedDecision(decision)}
                  style={{ borderLeftColor: getDecisionColor(decision.decision) }}
                >
                  <div className="decision-header">
                    <span className="decision-id">{decision.id}</span>
                    <span 
                      className={`decision-badge decision-${decision.decision}`}
                      style={{ backgroundColor: getDecisionColor(decision.decision) }}
                    >
                      {decision.decision}
                    </span>
                  </div>
                  <div className="decision-operation">{decision.operation}</div>
                  <div className="decision-time">{formatTimestamp(decision.timestamp)}</div>
                  {decision.violations.length > 0 && (
                    <div className="decision-violations">
                      ⚠️ {decision.violations.length} violation(s)
                    </div>
                  )}
                  {decision.human_review_required && (
                    <div className="decision-review">
                      👤 Human review required
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {selectedDecision && (
          <div className="decision-details">
            <div className="details-header">
              <h4>Decision Details</h4>
              <button onClick={() => setSelectedDecision(null)}>✕</button>
            </div>

            <div className="details-content">
              <div className="detail-section">
                <label>Decision ID:</label>
                <span>{selectedDecision.id}</span>
              </div>

              <div className="detail-section">
                <label>Operation:</label>
                <span>{selectedDecision.operation}</span>
              </div>

              <div className="detail-section">
                <label>Timestamp:</label>
                <span>{formatTimestamp(selectedDecision.timestamp)}</span>
              </div>

              <div className="detail-section">
                <label>Decision:</label>
                <span 
                  className="decision-status"
                  style={{ color: getDecisionColor(selectedDecision.decision) }}
                >
                  {selectedDecision.decision.toUpperCase()}
                </span>
              </div>

              <div className="detail-section">
                <label>Constraints Checked:</label>
                <div className="constraints-list">
                  {selectedDecision.constraints_checked.map((constraint, idx) => (
                    <div key={idx} className="constraint-item">
                      ✓ {constraint}
                    </div>
                  ))}
                </div>
              </div>

              {selectedDecision.violations.length > 0 && (
                <div className="detail-section">
                  <label>Violations:</label>
                  <div className="violations-list">
                    {selectedDecision.violations.map((violation, idx) => (
                      <div 
                        key={idx} 
                        className="violation-item"
                        style={{ borderLeftColor: getSeverityColor(violation.severity) }}
                      >
                        <div className="violation-header">
                          <span 
                            className="violation-severity"
                            style={{ color: getSeverityColor(violation.severity) }}
                          >
                            {violation.severity.toUpperCase()}
                          </span>
                          <span className="violation-constraint">{violation.constraint}</span>
                        </div>
                        <div className="violation-description">{violation.description}</div>
                        {violation.recommendation && (
                          <div className="violation-recommendation">
                            💡 {violation.recommendation}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {selectedDecision.human_review_required && (
                <div className="detail-section human-review">
                  <label>Human Review:</label>
                  <div className="review-notice">
                    ⚠️ This decision requires human review before proceeding.
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
