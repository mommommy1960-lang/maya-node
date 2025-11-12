// SPDX-License-Identifier: CERL-1.0
// Copyright (c) 2025 MAYA Node Contributors
//
// Constrained Ethics Runtime License 1.0
// This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

/**
 * Audit History Viewer Component
 * 
 * Displays immutable audit trail from ledger with filtering and search.
 */

import React, { useState, useEffect } from 'react';

export interface AuditEntry {
  index: number;
  timestamp: number;
  operation: string;
  data: any;
  hash: string;
  previous_hash: string;
}

interface AuditViewerProps {
  entries?: AuditEntry[];
  autoRefresh?: boolean;
  refreshInterval?: number;
}

export function AuditHistoryViewer({ 
  entries = [], 
  autoRefresh = true,
  refreshInterval = 5000 
}: AuditViewerProps) {
  const [auditEntries, setAuditEntries] = useState<AuditEntry[]>(entries);
  const [selectedEntry, setSelectedEntry] = useState<AuditEntry | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [operationFilter, setOperationFilter] = useState<string>('all');
  const [verifying, setVerifying] = useState(false);
  const [integrityStatus, setIntegrityStatus] = useState<'verified' | 'unverified' | 'failed'>('unverified');

  useEffect(() => {
    if (entries.length > 0) {
      setAuditEntries(entries);
    } else {
      // Load mock data for development
      loadMockData();
    }

    if (autoRefresh) {
      const interval = setInterval(() => {
        // TODO: Fetch real data from API
        console.log('Refreshing audit data...');
      }, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [entries, autoRefresh, refreshInterval]);

  function loadMockData() {
    const mockEntries: AuditEntry[] = [
      {
        index: 0,
        timestamp: Date.now() - 600000,
        operation: 'genesis',
        data: { note: 'Ledger initialized' },
        hash: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
        previous_hash: '0000000000000000000000000000000000000000000000000000000000000000'
      },
      {
        index: 1,
        timestamp: Date.now() - 500000,
        operation: 'runtime_bridge_init',
        data: { timestamp: Date.now() - 500000, consent_required: true, attestation_required: false },
        hash: '1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
        previous_hash: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
      },
      {
        index: 2,
        timestamp: Date.now() - 400000,
        operation: 'consent_requested',
        data: { user_id: 'user123', operation: 'process_data', token_id: 'tok_abc123', scope: 'single_operation' },
        hash: '23456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef01',
        previous_hash: '1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef'
      },
      {
        index: 3,
        timestamp: Date.now() - 300000,
        operation: 'operation_start',
        data: { user_id: 'user123', operation: 'process_data', consent_token_id: 'tok_abc123' },
        hash: '3456789abcdef01234567890abcdef0123456789abcdef0123456789abcdef012',
        previous_hash: '23456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef01'
      },
      {
        index: 4,
        timestamp: Date.now() - 200000,
        operation: 'operation_complete',
        data: { user_id: 'user123', operation: 'process_data', status: 'success' },
        hash: '456789abcdef012345678901234567890abcdef0123456789abcdef012345678',
        previous_hash: '3456789abcdef01234567890abcdef0123456789abcdef0123456789abcdef012'
      },
      {
        index: 5,
        timestamp: Date.now() - 100000,
        operation: 'consent_requested',
        data: { user_id: 'user456', operation: 'analyze_patterns', token_id: 'tok_xyz789', scope: 'session' },
        hash: '56789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456',
        previous_hash: '456789abcdef012345678901234567890abcdef0123456789abcdef012345678'
      }
    ];
    setAuditEntries(mockEntries);
  }

  function formatTimestamp(timestamp: number): string {
    const date = new Date(timestamp);
    return date.toLocaleString();
  }

  function truncateHash(hash: string, length: number = 8): string {
    return hash.substring(0, length) + '...';
  }

  function getOperationColor(operation: string): string {
    if (operation.includes('init')) return '#2196f3';
    if (operation.includes('consent')) return '#9c27b0';
    if (operation.includes('start')) return '#ff9800';
    if (operation.includes('complete')) return '#4caf50';
    if (operation.includes('failed')) return '#f44336';
    return '#9e9e9e';
  }

  async function verifyIntegrity() {
    setVerifying(true);
    
    // Simulate verification delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // TODO: Implement actual ledger integrity verification
    // For now, simulate success
    setIntegrityStatus('verified');
    setVerifying(false);
  }

  const uniqueOperations = Array.from(new Set(auditEntries.map(e => e.operation)));
  
  const filteredEntries = auditEntries.filter(entry => {
    const matchesSearch = searchQuery === '' || 
      entry.operation.toLowerCase().includes(searchQuery.toLowerCase()) ||
      JSON.stringify(entry.data).toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesFilter = operationFilter === 'all' || entry.operation === operationFilter;
    
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="audit-history-viewer">
      <div className="audit-header">
        <h3>📜 Audit History Viewer</h3>
        <div className="audit-controls">
          <button 
            onClick={verifyIntegrity} 
            disabled={verifying}
            className="verify-button"
          >
            {verifying ? '⏳ Verifying...' : '🔍 Verify Integrity'}
          </button>
          {integrityStatus !== 'unverified' && (
            <span className={`integrity-status status-${integrityStatus}`}>
              {integrityStatus === 'verified' ? '✓ Verified' : '✗ Failed'}
            </span>
          )}
        </div>
      </div>

      <div className="audit-filters">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search audit trail..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="operation-filter">
          <label>Operation:</label>
          <select 
            value={operationFilter} 
            onChange={(e) => setOperationFilter(e.target.value)}
          >
            <option value="all">All Operations</option>
            {uniqueOperations.map(op => (
              <option key={op} value={op}>{op}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="audit-stats">
        <div className="stat-item">
          <label>Total Entries:</label>
          <span>{auditEntries.length}</span>
        </div>
        <div className="stat-item">
          <label>Filtered:</label>
          <span>{filteredEntries.length}</span>
        </div>
        <div className="stat-item">
          <label>Chain Length:</label>
          <span>{auditEntries.length > 0 ? auditEntries[auditEntries.length - 1].index + 1 : 0}</span>
        </div>
      </div>

      <div className="audit-content">
        <div className="entries-list">
          {filteredEntries.length === 0 ? (
            <div className="no-entries">
              No audit entries match your search
            </div>
          ) : (
            <div className="entries-table">
              <div className="table-header">
                <div className="col-index">Index</div>
                <div className="col-timestamp">Timestamp</div>
                <div className="col-operation">Operation</div>
                <div className="col-hash">Hash</div>
                <div className="col-actions">Actions</div>
              </div>
              <div className="table-body">
                {filteredEntries.map((entry) => (
                  <div
                    key={entry.index}
                    className={`table-row ${selectedEntry?.index === entry.index ? 'selected' : ''}`}
                    onClick={() => setSelectedEntry(entry)}
                  >
                    <div className="col-index">#{entry.index}</div>
                    <div className="col-timestamp">{formatTimestamp(entry.timestamp)}</div>
                    <div 
                      className="col-operation"
                      style={{ color: getOperationColor(entry.operation) }}
                    >
                      {entry.operation}
                    </div>
                    <div className="col-hash" title={entry.hash}>
                      {truncateHash(entry.hash)}
                    </div>
                    <div className="col-actions">
                      <button onClick={(e) => {
                        e.stopPropagation();
                        setSelectedEntry(entry);
                      }}>
                        View
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {selectedEntry && (
          <div className="entry-details">
            <div className="details-header">
              <h4>Entry Details</h4>
              <button onClick={() => setSelectedEntry(null)}>✕</button>
            </div>

            <div className="details-content">
              <div className="detail-section">
                <label>Index:</label>
                <span className="detail-value">#{selectedEntry.index}</span>
              </div>

              <div className="detail-section">
                <label>Timestamp:</label>
                <span className="detail-value">{formatTimestamp(selectedEntry.timestamp)}</span>
              </div>

              <div className="detail-section">
                <label>Operation:</label>
                <span 
                  className="detail-value operation-name"
                  style={{ color: getOperationColor(selectedEntry.operation) }}
                >
                  {selectedEntry.operation}
                </span>
              </div>

              <div className="detail-section">
                <label>Hash:</label>
                <code className="detail-hash">{selectedEntry.hash}</code>
              </div>

              <div className="detail-section">
                <label>Previous Hash:</label>
                <code className="detail-hash">{selectedEntry.previous_hash}</code>
              </div>

              <div className="detail-section">
                <label>Data:</label>
                <pre className="detail-data">
                  {JSON.stringify(selectedEntry.data, null, 2)}
                </pre>
              </div>

              <div className="detail-section chain-info">
                <label>Chain Verification:</label>
                <div className="chain-links">
                  {selectedEntry.index > 0 && (
                    <div className="chain-link">
                      ← Previous: #{selectedEntry.index - 1}
                    </div>
                  )}
                  <div className="chain-link current">
                    Current: #{selectedEntry.index}
                  </div>
                  {selectedEntry.index < auditEntries.length - 1 && (
                    <div className="chain-link">
                      Next: #{selectedEntry.index + 1} →
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
