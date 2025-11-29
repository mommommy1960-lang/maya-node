# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
MAYA Node CLI - Sovereign AI Runtime Command-Line Interface

This CLI provides command-line access to the MAYA Node sovereign AI runtime
with integrated consent token management and audit logging.

Every CLI action that writes to the audit log generates and attaches a consent
token, ensuring:
    - Ethical verification for all operations
    - Human oversight acknowledgment
    - Cryptographically signed audit trail
    - Tamper-evident record keeping

Commands:
    init        Initialize a new MAYA Node runtime environment
    process     Process input through the sovereign runtime
    audit       View and verify audit log entries
    verify      Verify audit log integrity
    keygen      Generate a new trust root key for consent tokens
    
Usage:
    python cli.py init [--data-dir PATH]
    python cli.py process [--input TEXT] [--require-approval]
    python cli.py audit [--operation TYPE] [--limit N]
    python cli.py verify [--detailed]
    python cli.py keygen [--output PATH]

Environment Variables:
    MAYA_DATA_DIR: Default data directory for runtime files
    MAYA_TRUST_ROOT_KEY: Trust root key for consent token signing
"""

import argparse
import json
import os
import sys
import base64
from pathlib import Path
from typing import Optional

# Add src to path for imports when running directly
if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sovereign.consent_token import ConsentTokenManager, generate_trust_root_key
from sovereign.audit_log import AppendOnlyAuditLog
from sovereign.runtime import SovereignRuntime, RuntimeConfig


class MayaCLI:
    """
    MAYA Node Command-Line Interface.
    
    Provides command-line access to the sovereign AI runtime with integrated
    consent token management and append-only audit logging.
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the CLI.
        
        Args:
            data_dir: Directory for runtime data (audit logs, config, etc.)
                     Defaults to MAYA_DATA_DIR env var or ~/.maya
        """
        self.data_dir = Path(data_dir or os.environ.get('MAYA_DATA_DIR', 
                                                         os.path.expanduser('~/.maya')))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.audit_log_path = self.data_dir / 'audit.jsonl'
        self.key_path = self.data_dir / 'trust_root.key'
        
        # Load or generate trust root key
        trust_root_key = self._load_trust_root_key()
        self.consent_token_manager = ConsentTokenManager(trust_root_key)
        
        # Audit log is initialized on demand
        self._audit_log = None
    
    @property
    def audit_log(self):
        """Lazy-load the audit log on first access."""
        if self._audit_log is None:
            self._audit_log = AppendOnlyAuditLog(
                str(self.audit_log_path),
                consent_token_manager=self.consent_token_manager
            )
        return self._audit_log
    
    def _load_trust_root_key(self) -> Optional[bytes]:
        """
        Load trust root key from file or environment.
        
        Priority:
            1. MAYA_TRUST_ROOT_KEY environment variable
            2. trust_root.key file in data directory
            3. None (will auto-generate in ConsentTokenManager)
        
        Returns:
            Trust root key as bytes, or None to auto-generate
        """
        # Try environment variable first
        env_key = os.environ.get('MAYA_TRUST_ROOT_KEY')
        if env_key:
            return base64.b64decode(env_key)
        
        # Try file in data directory
        if self.key_path.exists():
            try:
                with open(self.key_path, 'r') as f:
                    key_b64 = f.read().strip()
                return base64.b64decode(key_b64)
            except Exception as e:
                print(f"WARNING: Failed to load key from {self.key_path}: {e}")
                print("A new key will be generated.")
        
        return None
    
    def print_consent_summary(self, operation: str, token_dict: dict) -> None:
        """
        Print a user-friendly summary of a consent token.
        
        Args:
            operation: Operation name
            token_dict: Consent token as dictionary
        """
        from sovereign.consent_token import ConsentToken
        
        token = ConsentToken.from_dict(token_dict)
        truncated_sig = self.consent_token_manager.get_truncated_signature(token)
        
        # Validate token
        is_valid = self.consent_token_manager.validate_token(token)
        status = "✓ VERIFIED" if is_valid else "✗ INVALID"
        
        print("\n" + "=" * 60)
        print("CONSENT TOKEN SUMMARY")
        print("=" * 60)
        print(f"Operation:        {token.operation}")
        print(f"Ethics Verified:  {token.ethics_verified}")
        print(f"Human Approval:   {token.human_approval}")
        print(f"Timestamp:        {token.timestamp}")
        print(f"User ID:          {token.user_id}")
        print(f"Signature:        {truncated_sig}")
        print(f"Status:           {status}")
        print("=" * 60 + "\n")
    
    def cmd_init(self, args) -> int:
        """
        Initialize a new MAYA Node runtime environment.
        
        Creates necessary directories and initializes the audit log with
        a genesis entry and consent token.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success)
        """
        print("Initializing MAYA Node runtime...")
        print(f"Data directory: {self.data_dir}")
        
        # Check if already initialized
        if self.audit_log.get_entry_count() > 1:
            print("WARNING: Runtime already initialized.")
            print(f"Audit log contains {self.audit_log.get_entry_count()} entries.")
            
            response = input("Reinitialize? This will not delete the existing log. [y/N]: ")
            if response.lower() != 'y':
                print("Initialization cancelled.")
                return 0
        
        # Create initialization consent token
        token = self.consent_token_manager.issue_token(
            operation="runtime_init",
            ethics_verified=True,
            human_approval="cli_initialization",
            user_id=os.environ.get('USER', 'unknown')
        )
        
        # Log initialization
        entry = self.audit_log.append(
            operation="runtime_init",
            data={
                "data_dir": str(self.data_dir),
                "audit_log_path": str(self.audit_log_path)
            },
            consent_token=token
        )
        
        print("✓ Runtime initialized successfully")
        print(f"✓ Audit log: {self.audit_log_path}")
        print(f"✓ Entry count: {self.audit_log.get_entry_count()}")
        
        # Print consent token summary
        self.print_consent_summary("runtime_init", token.to_dict())
        
        return 0
    
    def cmd_process(self, args) -> int:
        """
        Process input through the sovereign runtime.
        
        Creates a consent token for the operation and logs to the audit trail.
        
        Args:
            args: Command-line arguments (input, require_approval)
            
        Returns:
            Exit code (0 for success)
        """
        input_text = args.input or input("Enter input to process: ")
        
        print(f"\nProcessing input: {input_text}")
        
        # Create runtime configuration
        config = RuntimeConfig(
            enable_ethics_checks=True,
            require_human_approval=args.require_approval,
            audit_logging=True
        )
        
        runtime = SovereignRuntime(config)
        
        # Process input
        try:
            result = runtime.process({"input": input_text})
            
            # Determine human approval status
            human_approval = result.get('human_approved', False)
            if args.require_approval and not human_approval:
                print("WARNING: Human approval was required but not obtained")
            
            # Create consent token
            token = self.consent_token_manager.issue_token(
                operation="process_input",
                ethics_verified=result.get('ethics_verified', False),
                human_approval=human_approval,
                user_id=os.environ.get('USER', 'unknown')
            )
            
            # Log to audit trail
            entry = self.audit_log.append(
                operation="process_input",
                data={
                    "input": input_text,
                    "result": result,
                    "status": "success"
                },
                consent_token=token
            )
            
            print("\n✓ Processing complete")
            print(f"Result: {json.dumps(result, indent=2)}")
            
            # Print consent token summary
            self.print_consent_summary("process_input", token.to_dict())
            
            return 0
            
        except Exception as e:
            print(f"\n✗ Processing failed: {e}")
            
            # Log failure with consent token
            token = self.consent_token_manager.issue_token(
                operation="process_input_failed",
                ethics_verified=False,
                human_approval=None,
                user_id=os.environ.get('USER', 'unknown')
            )
            
            entry = self.audit_log.append(
                operation="process_input_failed",
                data={
                    "input": input_text,
                    "error": str(e),
                    "status": "failed"
                },
                consent_token=token
            )
            
            self.print_consent_summary("process_input_failed", token.to_dict())
            
            return 1
    
    def cmd_audit(self, args) -> int:
        """
        View audit log entries.
        
        Args:
            args: Command-line arguments (operation, limit)
            
        Returns:
            Exit code (0 for success)
        """
        print("AUDIT LOG")
        print("=" * 80)
        
        # Get entries
        if args.operation:
            entries = self.audit_log.get_entries_by_operation(args.operation)
            print(f"Filtering by operation: {args.operation}")
        else:
            entries = self.audit_log.read_all()
        
        # Apply limit
        if args.limit:
            entries = entries[-args.limit:]
            print(f"Showing last {args.limit} entries")
        
        print(f"Total entries: {len(entries)}\n")
        
        # Display entries
        for entry in entries:
            token = entry.consent_token
            is_valid = self.consent_token_manager.validate_token(token)
            status_icon = "✓" if is_valid else "✗"
            
            print(f"[{entry.entry_id}] {entry.operation}")
            print(f"  Timestamp: {entry.timestamp}")
            print(f"  User: {token.user_id}")
            print(f"  Ethics Verified: {token.ethics_verified}")
            print(f"  Human Approval: {token.human_approval}")
            print(f"  Token Status: {status_icon} {'VALID' if is_valid else 'INVALID'}")
            print(f"  Signature: {self.consent_token_manager.get_truncated_signature(token)}")
            
            if args.verbose:
                print(f"  Data: {json.dumps(entry.data, indent=4)}")
            
            print()
        
        return 0
    
    def cmd_verify(self, args) -> int:
        """
        Verify audit log integrity.
        
        Checks the hash chain and consent token signatures.
        
        Args:
            args: Command-line arguments (detailed)
            
        Returns:
            Exit code (0 if valid, 1 if invalid)
        """
        print("VERIFYING AUDIT LOG INTEGRITY")
        print("=" * 80)
        print(f"Audit log: {self.audit_log_path}")
        print(f"Entry count: {self.audit_log.get_entry_count()}\n")
        
        # Verify hash chain
        print("Checking hash chain integrity...")
        is_valid, error = self.audit_log.verify_integrity()
        
        if is_valid:
            print("✓ Hash chain is valid")
        else:
            print(f"✗ Hash chain is INVALID: {error}")
            return 1
        
        # Verify consent tokens
        print("\nVerifying consent token signatures...")
        entries = self.audit_log.read_all()
        invalid_tokens = []
        
        for entry in entries:
            is_valid = self.consent_token_manager.validate_token(entry.consent_token)
            if not is_valid:
                invalid_tokens.append(entry.entry_id)
                if args.detailed:
                    print(f"  ✗ Entry {entry.entry_id}: INVALID token signature")
        
        if invalid_tokens:
            print(f"\n✗ Found {len(invalid_tokens)} entries with invalid consent tokens")
            print(f"  Invalid entry IDs: {invalid_tokens}")
            return 1
        else:
            print(f"✓ All {len(entries)} consent tokens are valid")
        
        print("\n" + "=" * 80)
        print("✓ AUDIT LOG VERIFICATION COMPLETE - ALL CHECKS PASSED")
        print("=" * 80)
        
        return 0
    
    def cmd_keygen(self, args) -> int:
        """
        Generate a new trust root key for consent tokens.
        
        Args:
            args: Command-line arguments (output)
            
        Returns:
            Exit code (0 for success)
        """
        print("GENERATING TRUST ROOT KEY")
        print("=" * 80)
        print("\nWARNING: Store this key securely!")
        print("  - Never commit to source control")
        print("  - Use a secrets manager in production")
        print("  - Back up securely for disaster recovery")
        print("  - Rotate regularly per security policy\n")
        
        # Generate key
        key = generate_trust_root_key()
        key_b64 = base64.b64encode(key).decode('utf-8')
        
        print(f"Generated key (base64): {key_b64}\n")
        
        # Save to file if requested
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                f.write(key_b64)
            
            # Set restrictive permissions
            os.chmod(output_path, 0o600)
            
            print(f"✓ Key saved to: {output_path}")
            print(f"  Permissions set to 0600 (owner read/write only)")
        
        print("\nTo use this key, set the environment variable:")
        print(f"  export MAYA_TRUST_ROOT_KEY='{key_b64}'")
        print("\nOr load from file at runtime.")
        
        return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="MAYA Node CLI - Sovereign AI Runtime with Consent Tokens",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Initialize runtime:
    python cli.py init
  
  Process input:
    python cli.py process --input "optimize energy distribution"
  
  View audit log:
    python cli.py audit --limit 10
  
  Verify integrity:
    python cli.py verify --detailed
  
  Generate trust root key:
    python cli.py keygen --output ~/.maya/trust_root.key

Environment Variables:
  MAYA_DATA_DIR         Data directory (default: ~/.maya)
  MAYA_TRUST_ROOT_KEY   Trust root key (base64 encoded)
        """
    )
    
    parser.add_argument(
        '--data-dir',
        help='Data directory for runtime files (default: $MAYA_DATA_DIR or ~/.maya)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # init command
    parser_init = subparsers.add_parser('init', help='Initialize runtime environment')
    
    # process command
    parser_process = subparsers.add_parser('process', help='Process input through runtime')
    parser_process.add_argument('--input', help='Input text to process')
    parser_process.add_argument(
        '--require-approval',
        action='store_true',
        help='Require human approval for processing'
    )
    
    # audit command
    parser_audit = subparsers.add_parser('audit', help='View audit log entries')
    parser_audit.add_argument('--operation', help='Filter by operation type')
    parser_audit.add_argument('--limit', type=int, help='Limit number of entries shown')
    parser_audit.add_argument('-v', '--verbose', action='store_true', 
                             help='Show detailed entry data')
    
    # verify command
    parser_verify = subparsers.add_parser('verify', help='Verify audit log integrity')
    parser_verify.add_argument('--detailed', action='store_true',
                              help='Show detailed verification results')
    
    # keygen command
    parser_keygen = subparsers.add_parser('keygen', help='Generate trust root key')
    parser_keygen.add_argument('--output', help='Output file path for key')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize CLI
    cli = MayaCLI(data_dir=args.data_dir)
    
    # Execute command
    if args.command == 'init':
        return cli.cmd_init(args)
    elif args.command == 'process':
        return cli.cmd_process(args)
    elif args.command == 'audit':
        return cli.cmd_audit(args)
    elif args.command == 'verify':
        return cli.cmd_verify(args)
    elif args.command == 'keygen':
        return cli.cmd_keygen(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
