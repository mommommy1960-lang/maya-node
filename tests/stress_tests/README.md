# Stress Test Division

## Overview

The Stress Test Division runs comprehensive destructive automated tests to validate system resilience across the maya-node repository. These tests intentionally attempt to break pipelines, parse invalid data, and inject failures to ensure robust error handling.

## Test Coverage

### 1. Workflow Stress Tests (`test_workflow_stress.py`)
- Malformed YAML syntax
- Invalid workflow schema
- Circular workflow dependencies
- Excessive matrix strategies
- Invalid permission values

### 2. Config Stress Tests (`test_config_stress.py`)
- Malformed JSON/YAML configs
- Deeply nested structures (1000+ levels)
- Extremely large configs (10MB+)
- Unicode and special characters
- Circular references
- Type confusion scenarios

### 3. TTS Engine & Voice Routing Tests (`test_tts_stress.py`)
- Missing voice configuration files
- Malformed voice configs
- Invalid agent names (empty, extremely long, injection attempts)
- Malformed text input (null, empty, extremely long)
- JSON injection attempts
- Race conditions
- Unsupported voice tags
- Resource exhaustion

### 4. Pipeline & Commit Tests (`test_pipeline_stress.py`)
- Malformed commit messages
- Invalid commit metadata (author, email)
- Large file commits (10MB+)
- Binary corruption
- Build failure injection
- Test failure injection
- Deployment failure injection
- Concurrent pipeline conflicts
- Environment corruption

## Running the Tests

### Run All Tests
```bash
python tests/stress_tests/run_stress_tests.py
```

### Run Individual Test Suites
```bash
python tests/stress_tests/test_workflow_stress.py
python tests/stress_tests/test_config_stress.py
python tests/stress_tests/test_tts_stress.py
python tests/stress_tests/test_pipeline_stress.py
```

### Via GitHub Actions
The stress tests run automatically:
- **Weekly**: Every Sunday at 2 AM UTC
- **Manual**: Workflow dispatch trigger
- **On Push**: To `stress-test/**` branches

## Log Files

All test results are logged to:
```
.github/council/logs/stress/stress_test_cycle_YYYYMMDD_HHMMSS.json
```

Each log file contains:
- Cycle ID and timestamp
- Total test count
- Pass/fail/error counts
- Detailed results for each test
- Error messages and stack traces

## Log Format

```json
{
  "cycle_id": "20251114_034215",
  "timestamp": "2025-11-14T03:42:15.123456",
  "total_tests": 50,
  "passed": 45,
  "errors": 5,
  "results": [
    {
      "timestamp": "2025-11-14T03:42:15.123456",
      "test_name": "workflow_malformed_yaml_0",
      "status": "PASS",
      "details": "YAML parser correctly rejected malformed syntax",
      "error": ""
    }
  ]
}
```

## Test Statuses

- **PASS**: Test executed successfully and validated expected behavior
- **EXPECTED_FAIL**: Test correctly identified a malformed input (success in stress testing)
- **ERROR**: Unexpected error during test execution (requires investigation)

## Design Philosophy

These are **destructive tests** - they intentionally:
- Provide invalid input
- Corrupt data structures
- Inject failures
- Exceed resource limits
- Attempt security exploits

The goal is to ensure the system handles edge cases gracefully and fails safely.

## Framework

The `stress_test_framework.py` provides:
- Centralized test result logging
- Consistent error handling
- Automatic log file generation
- Test execution tracking

## Adding New Tests

1. Create a new test file in `tests/stress_tests/`
2. Import `StressTestFramework`
3. Define test functions that accept `framework` parameter
4. Use `framework.log_test_result()` to log results
5. Add test suite to `run_stress_tests.py`

Example:
```python
def test_my_stress_case(framework: StressTestFramework):
    try:
        # Attempt to break something
        result = dangerous_operation()
        framework.log_test_result(
            "my_stress_test",
            "PASS",
            details="System handled dangerous input correctly"
        )
    except ExpectedError as e:
        framework.log_test_result(
            "my_stress_test",
            "EXPECTED_FAIL",
            details=str(e)
        )
```

## Dependencies

- Python 3.11+
- PyYAML

## License

SPDX-License-Identifier: CERL-1.0
Copyright (c) 2025 MAYA Node Contributors
