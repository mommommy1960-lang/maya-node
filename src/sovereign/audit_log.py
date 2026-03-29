# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Append-Only Audit Log Module

This module implements an append-only audit log system using JSONL format
(JSON Lines) for persistent, tamper-evident audit trails.

Key Features:
    - Append-only file operations (no modifications allowed)
    - JSONL format for easy parsing and streaming
    - Consent token integration for every entry
    - Integrity verification through hash chains
    - Tamper detection capabilities

Audit Log Structure:
    Each line in the audit log is a JSON object containing:
    - entry_id: Sequential entry identifier
    - timestamp: ISO 8601 UTC timestamp
    - operation: Operation type/name
    - data: Operation-specific data
    - consent_token: Full consent token object
    - previous_hash: SHA256 hash of previous entry (chain linkage)
    - entry_hash: SHA256 hash of current entry

The audit log provides:
    1. Immutable record of all operations
    2. Consent token verification for each action
    3. Hash chain for tamper detection
    4. Human-readable JSON format
    5. Streaming-friendly JSONL structure

Security Considerations:
    - File should be write-protected after initialization
    - Regular integrity checks should be performed
    - Backups should be maintained securely
    - Consider encryption at rest for sensitive data
"""

import json
import hashlib
import os
import fcntl
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pathlib import Path

# Handle imports for both module and standalone use
try:
    from .consent_token import ConsentToken
except ImportError:
    from consent_token import ConsentToken


class AuditLogEntry:
    """
    Represents a single entry in the audit log.
    
    Each entry forms a node in the hash chain, linking to the previous
    entry and providing tamper detection capabilities.
    """
    
    def __init__(
        self,
        entry_id: int,
        timestamp: str,
        operation: str,
        data: Dict[str, Any],
        consent_token: ConsentToken,
        previous_hash: str
    ):
        """
        Initialize an audit log entry.
        
        Args:
            entry_id: Sequential entry number
            timestamp: ISO 8601 UTC timestamp
            operation: Operation type/name
            data: Operation-specific data
            consent_token: Consent token for this operation
            previous_hash: Hash of previous entry (for chain linkage)
        """
        self.entry_id = entry_id
        self.timestamp = timestamp
        self.operation = operation
        self.data = data
        self.consent_token = consent_token
        self.previous_hash = previous_hash
        self.entry_hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """
        Compute SHA256 hash of this entry.
        
        The hash includes all fields except entry_hash itself, creating
        a tamper-evident record.
        
        Returns:
            Hexadecimal SHA256 hash string
        """
        # Create canonical representation for hashing
        content = json.dumps({
            'entry_id': self.entry_id,
            'timestamp': self.timestamp,
            'operation': self.operation,
            'data': self.data,
            'consent_token': self.consent_token.to_dict(),
            'previous_hash': self.previous_hash
        }, sort_keys=True)
        
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert entry to dictionary for serialization.
        
        Returns:
            Dictionary representation including all fields
        """
        return {
            'entry_id': self.entry_id,
            'timestamp': self.timestamp,
            'operation': self.operation,
            'data': self.data,
            'consent_token': self.consent_token.to_dict(),
            'previous_hash': self.previous_hash,
            'entry_hash': self.entry_hash
        }
    
    def to_json(self) -> str:
        """
        Serialize entry to JSON string.
        
        Returns:
            JSON string (single line, suitable for JSONL)
        """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuditLogEntry':
        """
        Create AuditLogEntry from dictionary.
        
        Args:
            data: Dictionary containing entry fields
            
        Returns:
            AuditLogEntry instance
        """
        consent_token = ConsentToken.from_dict(data['consent_token'])
        entry = cls(
            entry_id=data['entry_id'],
            timestamp=data['timestamp'],
            operation=data['operation'],
            data=data['data'],
            consent_token=consent_token,
            previous_hash=data['previous_hash']
        )
        # Override computed hash with stored hash for verification
        entry.entry_hash = data['entry_hash']
        return entry
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AuditLogEntry':
        """
        Deserialize entry from JSON string.
        
        Args:
            json_str: JSON string representation
            
        Returns:
            AuditLogEntry instance
        """
        return cls.from_dict(json.loads(json_str))


class AppendOnlyAuditLog:
    """
    Manages an append-only audit log with consent tokens and integrity verification.
    
    This class provides:
        - Append-only operations (no updates or deletes)
        - JSONL persistence
        - Hash chain integrity
        - Consent token verification
        - Tamper detection
    
    File Format:
        Each line is a complete JSON object (JSONL format)
        Enables streaming reads and efficient appends
    """
    
    def __init__(self, log_path: str, consent_token_manager=None):
        """
        Initialize the audit log.
        
        Args:
            log_path: Path to the JSONL audit log file
            consent_token_manager: Optional ConsentTokenManager instance to use
                                  for genesis entry creation. If None, creates a new one.
            
        Creates the log file if it doesn't exist. If the file exists,
        loads the current state for chain continuation.
        """
        self.log_path = Path(log_path)
        self.entry_count = 0
        self.last_hash = "0" * 64  # Genesis hash
        self.consent_token_manager = consent_token_manager
        
        # Ensure directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize or load existing log
        if self.log_path.exists():
            self._load_state()
        else:
            self._initialize_log()
    
    def _initialize_log(self) -> None:
        """
        Initialize a new audit log with genesis entry.
        
        Creates the log file with a genesis entry that establishes
        the start of the hash chain.
        """
        # Create genesis entry
        try:
            from .consent_token import ConsentTokenManager
        except ImportError:
            from consent_token import ConsentTokenManager
        
        # Use provided manager or create temporary one
        if self.consent_token_manager:
            manager = self.consent_token_manager
        else:
            manager = ConsentTokenManager()
        
        genesis_token = manager.issue_token(
            operation="genesis",
            ethics_verified=True,
            human_approval=None,
            user_id="system"
        )
        
        genesis_entry = AuditLogEntry(
            entry_id=0,
            timestamp=datetime.now(timezone.utc).isoformat(),
            operation="genesis",
            data={"note": "Audit log initialized"},
            consent_token=genesis_token,
            previous_hash=self.last_hash
        )
        
        # Write genesis entry
        with open(self.log_path, 'w') as f:
            f.write(genesis_entry.to_json() + '\n')
        
        self.entry_count = 1
        self.last_hash = genesis_entry.entry_hash
    
    def _load_state(self) -> None:
        """
        Load current state from existing audit log.
        
        Reads the log to determine the current entry count and last hash
        for continuing the chain. Does not verify integrity (use verify_integrity
        for that).
        """
        with open(self.log_path, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            # Empty file, treat as new
            self._initialize_log()
            return
        
        # Get last entry
        last_line = lines[-1].strip()
        if last_line:
            last_entry = AuditLogEntry.from_json(last_line)
            self.entry_count = last_entry.entry_id + 1
            self.last_hash = last_entry.entry_hash
        else:
            # File exists but empty/corrupted
            self._initialize_log()
    
    def append(
        self,
        operation: str,
        data: Dict[str, Any],
        consent_token: ConsentToken
    ) -> AuditLogEntry:
        """
        Append a new entry to the audit log.
        
        This is the primary method for adding entries. Each entry must have
        a valid consent token. The entry is immediately persisted to disk.
        
        Args:
            operation: Operation type/name
            data: Operation-specific data
            consent_token: Valid consent token for this operation
            
        Returns:
            Created AuditLogEntry
            
        Raises:
            IOError: If write fails
            
        Example:
            >>> from consent_token import ConsentTokenManager
            >>> manager = ConsentTokenManager()
            >>> token = manager.issue_token("data_write", True, True)
            >>> log = AppendOnlyAuditLog("audit.jsonl")
            >>> entry = log.append("data_write", {"key": "value"}, token)
        """
        # Create new entry
        entry = AuditLogEntry(
            entry_id=self.entry_count,
            timestamp=datetime.now(timezone.utc).isoformat(),
            operation=operation,
            data=data,
            consent_token=consent_token,
            previous_hash=self.last_hash
        )
        
        # Append to file (with file locking for concurrent access)
        with open(self.log_path, 'a') as f:
            # Acquire exclusive lock
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                f.write(entry.to_json() + '\n')
                f.flush()
                os.fsync(f.fileno())  # Ensure write to disk
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        
        # Update state
        self.entry_count += 1
        self.last_hash = entry.entry_hash
        
        return entry
    
    def read_all(self) -> List[AuditLogEntry]:
        """
        Read all entries from the audit log.
        
        Returns:
            List of all AuditLogEntry objects in order
            
        Note:
            For large logs, consider using read_stream() instead.
        """
        entries = []
        
        if not self.log_path.exists():
            return entries
        
        with open(self.log_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(AuditLogEntry.from_json(line))
        
        return entries
    
    def read_stream(self):
        """
        Stream entries from the audit log (generator).
        
        Yields:
            AuditLogEntry objects one at a time
            
        Useful for processing large logs without loading everything into memory.
        
        Example:
            >>> log = AppendOnlyAuditLog("audit.jsonl")
            >>> for entry in log.read_stream():
            ...     print(entry.operation)
        """
        if not self.log_path.exists():
            return
        
        with open(self.log_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    yield AuditLogEntry.from_json(line)
    
    def verify_integrity(self) -> tuple[bool, Optional[str]]:
        """
        Verify the integrity of the entire audit log.
        
        Checks:
            1. Each entry's hash matches its computed hash
            2. Each entry's previous_hash matches the actual previous entry
            3. Entry IDs are sequential
        
        Returns:
            Tuple of (is_valid, error_message)
            - (True, None) if log is valid
            - (False, error_message) if corruption detected
            
        Example:
            >>> log = AppendOnlyAuditLog("audit.jsonl")
            >>> is_valid, error = log.verify_integrity()
            >>> if not is_valid:
            ...     print(f"Log corrupted: {error}")
        """
        entries = self.read_all()
        
        if not entries:
            return True, None
        
        for i, entry in enumerate(entries):
            # Verify entry hash
            expected_hash = entry._compute_hash()
            if entry.entry_hash != expected_hash:
                return False, f"Hash mismatch at entry {entry.entry_id}"
            
            # Verify entry ID sequence
            if entry.entry_id != i:
                return False, f"Entry ID out of sequence at position {i}"
            
            # Verify chain linkage
            if i > 0:
                previous_entry = entries[i - 1]
                if entry.previous_hash != previous_entry.entry_hash:
                    return False, f"Chain broken at entry {entry.entry_id}"
        
        return True, None
    
    def get_entry_count(self) -> int:
        """
        Get the total number of entries in the log.
        
        Returns:
            Number of entries (including genesis)
        """
        return self.entry_count
    
    def get_entries_by_operation(self, operation: str) -> List[AuditLogEntry]:
        """
        Get all entries matching a specific operation type.
        
        Args:
            operation: Operation type to filter by
            
        Returns:
            List of matching entries
        """
        return [entry for entry in self.read_all() if entry.operation == operation]


if __name__ == "__main__":
    """
    Example usage and self-test of audit log system.
    """
    import tempfile
    import os
    import sys
    
    # Fix imports for standalone execution
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from consent_token import ConsentToken, ConsentTokenManager
    
    print("=== Append-Only Audit Log Self-Test ===\n")
    
    # Create temporary log file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        temp_log = f.name
    
    try:
        # Initialize log
        print("1. Initializing audit log...")
        log = AppendOnlyAuditLog(temp_log)
        print(f"   Entry count: {log.get_entry_count()}")
        
        # Create consent tokens and append entries
        print("\n2. Appending entries with consent tokens...")
        
        manager = ConsentTokenManager(b"test_key_for_demonstration")
        
        for i in range(3):
            token = manager.issue_token(
                operation=f"test_operation_{i}",
                ethics_verified=True,
                human_approval=True,
                user_id=f"user_{i}"
            )
            
            entry = log.append(
                operation=f"test_operation_{i}",
                data={"test_value": i * 10},
                consent_token=token
            )
            print(f"   Added entry {entry.entry_id}: {entry.operation}")
        
        print(f"\n   Total entries: {log.get_entry_count()}")
        
        # Verify integrity
        print("\n3. Verifying log integrity...")
        is_valid, error = log.verify_integrity()
        print(f"   Valid: {is_valid}")
        if error:
            print(f"   Error: {error}")
        
        # Read entries
        print("\n4. Reading all entries...")
        entries = log.read_all()
        for entry in entries:
            print(f"   [{entry.entry_id}] {entry.operation} - Token valid: "
                  f"{manager.validate_token(entry.consent_token)}")
        
        # Test tamper detection
        print("\n5. Testing tamper detection...")
        print("   Manually corrupting log file...")
        
        # Read file, corrupt an entry, write back
        with open(temp_log, 'r') as f:
            lines = f.readlines()
        
        if len(lines) > 1:
            # Corrupt the second entry
            entry_dict = json.loads(lines[1])
            entry_dict['data']['corrupted'] = True
            lines[1] = json.dumps(entry_dict) + '\n'
            
            with open(temp_log, 'w') as f:
                f.writelines(lines)
            
            # Reload and verify
            log2 = AppendOnlyAuditLog(temp_log)
            is_valid, error = log2.verify_integrity()
            print(f"   Corrupted log valid: {is_valid}")
            if error:
                print(f"   Detected: {error}")
        
        print("\n=== Self-Test Complete ===")
        
    finally:
        # Cleanup
        if os.path.exists(temp_log):
            os.remove(temp_log)
