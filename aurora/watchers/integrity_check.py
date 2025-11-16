#!/usr/bin/env python3
"""
Aurora Integrity Check
Validates system state and configuration integrity
"""
import sys
import os
import json

# Add parent directory to path to import statebrain
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'engine'))
import statebrain

def main():
    """Run integrity check on Aurora state"""
    state_path = os.path.join(os.path.dirname(__file__), '..', '..', 'aurora.state.json')
    
    # Check if state file exists
    if not os.path.exists(state_path):
        print("✗ State file not found")
        return 1
    
    # Load state
    state = statebrain.load_state(state_path)
    if state is None:
        print("✗ Failed to load state")
        return 1
    
    # Verify integrity
    if statebrain.verify_integrity(state):
        print("✓ Integrity check passed")
        return 0
    else:
        print("✗ Integrity check failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
