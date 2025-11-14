#!/usr/bin/env python3
"""
SPDX-License-Identifier: CERL-1.0
Copyright (c) 2025 MAYA Node Contributors

Stress Test Division - Master Runner
=====================================
Runs all destructive automated tests and logs results to .github/council/logs/stress/
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from stress_test_framework import StressTestFramework
from test_workflow_stress import run_all_workflow_tests
from test_config_stress import run_all_config_tests
from test_tts_stress import run_all_tts_tests
from test_pipeline_stress import run_all_pipeline_tests


def main():
    """Run all stress tests."""
    print("=" * 80)
    print(" " * 20 + "MAYA NODE STRESS TEST DIVISION")
    print("=" * 80)
    print()
    print("Running comprehensive destructive automated tests...")
    print("This will test workflows, configs, JSON, YAML, TTS engine, and voice routing.")
    print("All results will be logged to .github/council/logs/stress/")
    print()
    print("=" * 80)
    
    # Initialize framework
    framework = StressTestFramework()
    
    # Run all test suites
    try:
        print("\n🔥 Starting stress test sweep...\n")
        
        # Workflow tests
        run_all_workflow_tests(framework)
        
        # Config tests
        run_all_config_tests(framework)
        
        # TTS and voice routing tests
        run_all_tts_tests(framework)
        
        # Pipeline and commit tests
        run_all_pipeline_tests(framework)
        
        print("\n✅ All stress test suites completed!\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Stress tests interrupted by user.")
        framework.log_test_result(
            "test_interrupted",
            "ERROR",
            details="Test execution interrupted by user"
        )
    except Exception as e:
        print(f"\n\n❌ Fatal error during stress test execution: {e}")
        framework.log_test_result(
            "fatal_error",
            "ERROR",
            error=str(e)
        )
    finally:
        # Always save results
        log_file = framework.save_results()
        
        # Print final summary
        print("\n" + "=" * 80)
        print("Stress Test Division - Execution Complete")
        print("=" * 80)
        print(f"📊 Results saved to: {log_file}")
        print(f"📁 Full logs available in: {framework.log_dir}")
        print("=" * 80)
        
        # Return exit code based on unexpected errors
        unexpected_errors = sum(
            1 for r in framework.test_results 
            if r["status"] == "ERROR"
        )
        
        if unexpected_errors > 0:
            print(f"\n⚠️  Warning: {unexpected_errors} unexpected errors occurred")
            print("Review the logs for details on which tests encountered issues.")
            return 1
        
        return 0


if __name__ == "__main__":
    sys.exit(main())
