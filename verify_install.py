#!/usr/bin/env python3
# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
#
# Quick installation verification script

"""
MAYA Node - Installation Verification

Run this script after installing to verify the installation is correct.
"""

import sys


def check_python_version():
    """Check if Python version is 3.11 or higher."""
    print("Checking Python version...", end=" ")
    if sys.version_info >= (3, 11):
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")
        return True
    else:
        print(f"✗ Python {sys.version_info.major}.{sys.version_info.minor} (requires 3.11+)")
        return False


def check_imports():
    """Check if core modules can be imported."""
    print("\nChecking core imports...")
    
    imports = [
        ("src.sovereign.runtime", "SovereignRuntime"),
        ("src.sovereign.ethics_engine", "EthicsEngine"),
        ("src.services.ledger.ledger", "ImmutableLedger"),
        ("src.api.endpoints", "Flask app"),
    ]
    
    all_ok = True
    for module, description in imports:
        try:
            __import__(module)
            print(f"  ✓ {description}")
        except ImportError as e:
            print(f"  ✗ {description}: {e}")
            all_ok = False
    
    return all_ok


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\nChecking dependencies...")
    
    dependencies = ["flask", "pytest"]
    
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ✗ {dep} (not installed)")
            all_ok = False
    
    return all_ok


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("MAYA Node - Installation Verification")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_imports(),
        check_dependencies(),
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✓ All checks passed! Installation is successful.")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Run tests: make test")
        print("  2. Read documentation: ONBOARDING.md")
        print("  3. Start developing!")
        return 0
    else:
        print("✗ Some checks failed. Please review the output above.")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("  1. Ensure you're in a virtual environment")
        print("  2. Run: pip install -e '.[dev]'")
        print("  3. Check DEVELOPMENT.md for setup instructions")
        return 1


if __name__ == "__main__":
    sys.exit(main())
