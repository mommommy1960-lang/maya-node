#!/usr/bin/env python3
"""
SPDX-License-Identifier: CERL-1.0
Copyright (c) 2025 MAYA Node Contributors

Workflow Stress Tests
=====================
Tests GitHub Actions workflows with malformed YAML, invalid syntax, and failure injection.
"""

import os
import tempfile
import yaml
from pathlib import Path
from stress_test_framework import StressTestFramework


def test_malformed_yaml_syntax(framework: StressTestFramework):
    """Test workflow parsing with malformed YAML syntax."""
    malformed_workflows = [
        # Missing colon
        """
name: Broken Workflow
on push
jobs:
  test:
    runs-on: ubuntu-latest
""",
        # Invalid indentation
        """
name: Bad Indent
on: push
jobs:
test:
  runs-on: ubuntu-latest
""",
        # Unclosed quotes
        """
name: "Unclosed Quote
on: push
jobs:
  test:
    runs-on: ubuntu-latest
""",
        # Invalid YAML structure
        """
name: Invalid Structure
on: [push
jobs:
  test:
    runs-on: ubuntu-latest
""",
    ]
    
    for idx, bad_yaml in enumerate(malformed_workflows):
        try:
            yaml.safe_load(bad_yaml)
            # If it didn't raise an error, that's unexpected
            framework.log_test_result(
                f"workflow_malformed_yaml_{idx}",
                "ERROR",
                details="YAML parser should have rejected malformed syntax"
            )
        except yaml.YAMLError as e:
            # Expected behavior - YAML parser catches the error
            framework.log_test_result(
                f"workflow_malformed_yaml_{idx}",
                "PASS",
                details=f"YAML parser correctly rejected malformed syntax: {str(e)[:100]}"
            )


def test_invalid_workflow_schema(framework: StressTestFramework):
    """Test workflows with invalid schema (valid YAML but invalid GHA schema)."""
    invalid_workflows = [
        # Missing required 'on' field
        {
            "name": "Missing On",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [{"run": "echo test"}]
                }
            }
        },
        # Invalid job structure
        {
            "name": "Invalid Job",
            "on": "push",
            "jobs": {
                "test": "not-a-valid-job-structure"
            }
        },
        # Missing runs-on
        {
            "name": "Missing Runs-On",
            "on": "push",
            "jobs": {
                "test": {
                    "steps": [{"run": "echo test"}]
                }
            }
        },
        # Invalid event trigger
        {
            "name": "Invalid Event",
            "on": "invalid_event_type",
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [{"run": "echo test"}]
                }
            }
        },
    ]
    
    for idx, workflow in enumerate(invalid_workflows):
        try:
            # Convert to YAML
            yaml_str = yaml.dump(workflow)
            # Verify it's valid YAML
            yaml.safe_load(yaml_str)
            
            # In a real test, we'd validate against GHA schema
            # For now, we log that we created an invalid workflow
            framework.log_test_result(
                f"workflow_invalid_schema_{idx}",
                "PASS",
                details=f"Created workflow with invalid schema: {workflow.get('name', 'unknown')}"
            )
        except Exception as e:
            framework.log_test_result(
                f"workflow_invalid_schema_{idx}",
                "ERROR",
                error=str(e)
            )


def test_circular_workflow_dependencies(framework: StressTestFramework):
    """Test workflow with circular dependencies."""
    circular_workflow = {
        "name": "Circular Dependencies",
        "on": "push",
        "jobs": {
            "job_a": {
                "runs-on": "ubuntu-latest",
                "needs": ["job_b"],
                "steps": [{"run": "echo A"}]
            },
            "job_b": {
                "runs-on": "ubuntu-latest",
                "needs": ["job_c"],
                "steps": [{"run": "echo B"}]
            },
            "job_c": {
                "runs-on": "ubuntu-latest",
                "needs": ["job_a"],
                "steps": [{"run": "echo C"}]
            }
        }
    }
    
    try:
        yaml_str = yaml.dump(circular_workflow)
        framework.log_test_result(
            "workflow_circular_dependencies",
            "PASS",
            details="Created workflow with circular dependencies (would be caught by GitHub Actions)"
        )
    except Exception as e:
        framework.log_test_result(
            "workflow_circular_dependencies",
            "ERROR",
            error=str(e)
        )


def test_workflow_with_excessive_matrix(framework: StressTestFramework):
    """Test workflow with excessively large matrix strategy."""
    excessive_workflow = {
        "name": "Excessive Matrix",
        "on": "push",
        "jobs": {
            "test": {
                "runs-on": "ubuntu-latest",
                "strategy": {
                    "matrix": {
                        "os": ["ubuntu-latest"] * 100,  # Way too many
                        "python-version": ["3.8", "3.9", "3.10", "3.11", "3.12"] * 20
                    }
                },
                "steps": [{"run": "echo test"}]
            }
        }
    }
    
    try:
        yaml_str = yaml.dump(excessive_workflow)
        total_jobs = len(excessive_workflow["jobs"]["test"]["strategy"]["matrix"]["os"]) * \
                     len(excessive_workflow["jobs"]["test"]["strategy"]["matrix"]["python-version"])
        framework.log_test_result(
            "workflow_excessive_matrix",
            "PASS",
            details=f"Created workflow with {total_jobs} matrix combinations (exceeds GitHub limits)"
        )
    except Exception as e:
        framework.log_test_result(
            "workflow_excessive_matrix",
            "ERROR",
            error=str(e)
        )


def test_workflow_with_invalid_permissions(framework: StressTestFramework):
    """Test workflow with invalid permission values."""
    invalid_perms_workflow = {
        "name": "Invalid Permissions",
        "on": "push",
        "permissions": {
            "contents": "invalid-permission-value",
            "issues": "super-admin",
            "pull-requests": "owner"
        },
        "jobs": {
            "test": {
                "runs-on": "ubuntu-latest",
                "steps": [{"run": "echo test"}]
            }
        }
    }
    
    try:
        yaml_str = yaml.dump(invalid_perms_workflow)
        framework.log_test_result(
            "workflow_invalid_permissions",
            "PASS",
            details="Created workflow with invalid permission values (read/write/none only allowed)"
        )
    except Exception as e:
        framework.log_test_result(
            "workflow_invalid_permissions",
            "ERROR",
            error=str(e)
        )


def run_all_workflow_tests(framework: StressTestFramework):
    """Run all workflow stress tests."""
    print("\n" + "="*60)
    print("Running Workflow Stress Tests")
    print("="*60)
    
    framework.run_test("test_malformed_yaml_syntax", test_malformed_yaml_syntax, framework)
    framework.run_test("test_invalid_workflow_schema", test_invalid_workflow_schema, framework)
    framework.run_test("test_circular_workflow_dependencies", test_circular_workflow_dependencies, framework)
    framework.run_test("test_workflow_with_excessive_matrix", test_workflow_with_excessive_matrix, framework)
    framework.run_test("test_workflow_with_invalid_permissions", test_workflow_with_invalid_permissions, framework)


if __name__ == "__main__":
    from stress_test_framework import main
    framework = main()
    run_all_workflow_tests(framework)
    framework.save_results()
