# Stress Test Division - Quick Start Guide

## What is the Stress Test Division?

The Stress Test Division is a comprehensive destructive testing suite that validates system resilience by intentionally:
- Breaking pipelines with malformed commits
- Corrupting JSON/YAML configurations
- Injecting failures into workflows
- Testing TTS engine with invalid input
- Stressing voice routing with edge cases

## Running Tests Locally

### Run All Tests
```bash
python3 tests/stress_tests/run_stress_tests.py
```

### Run Individual Test Suites
```bash
# Workflow tests only
python3 tests/stress_tests/test_workflow_stress.py

# Config tests only
python3 tests/stress_tests/test_config_stress.py

# TTS/Voice routing tests only
python3 tests/stress_tests/test_tts_stress.py

# Pipeline/commit tests only
python3 tests/stress_tests/test_pipeline_stress.py
```

## Running Tests via GitHub Actions

### Manual Trigger
1. Go to Actions tab in GitHub
2. Select "Stress Test Division" workflow
3. Click "Run workflow"
4. Choose test intensity (light/normal/aggressive)
5. Click "Run workflow"

### Automatic Runs
- **Weekly**: Every Sunday at 2 AM UTC
- **On Push**: To branches matching `stress-test/**`

## Understanding Results

### Test Statuses
- **PASS**: Test successfully validated expected behavior
- **EXPECTED_FAIL**: Test correctly caught malformed input (this is GOOD!)
- **ERROR**: Unexpected error (needs investigation)

### Log Files
Location: `.github/council/logs/stress/stress_test_cycle_YYYYMMDD_HHMMSS.json`

Structure:
```json
{
  "cycle_id": "20251114_034824",
  "timestamp": "2025-11-14T03:48:24.123456",
  "total_tests": 153,
  "passed": 146,
  "errors": 7,
  "results": [...]
}
```

## Test Categories

### 1. Workflow Tests (15+ tests)
Tests GitHub Actions workflows with:
- Malformed YAML
- Invalid schemas
- Circular dependencies
- Excessive matrix strategies

### 2. Config Tests (35+ tests)
Tests configuration parsing with:
- Malformed JSON/YAML
- Deep nesting (1000+ levels)
- Large configs (10MB+)
- Special characters and unicode

### 3. TTS/Voice Tests (55+ tests)
Tests voice engine with:
- Missing configurations
- Invalid agent names
- Malformed text input
- JSON injection attempts
- Resource exhaustion

### 4. Pipeline/Commit Tests (48+ tests)
Tests git and CI/CD with:
- Malformed commit messages
- Invalid metadata
- Large file commits
- Build/test failures
- Environment corruption

## Dependencies

```bash
pip install pyyaml
```

## Exit Codes

- **0**: All tests completed without unexpected errors
- **1**: One or more unexpected errors occurred

## Best Practices

1. **Review Logs**: Always check `.github/council/logs/stress/` after runs
2. **EXPECTED_FAIL is Good**: These indicate the system caught bad input
3. **ERROR Needs Attention**: Unexpected errors should be investigated
4. **Weekly Reviews**: Check weekly automated runs for trends

## Troubleshooting

### "No module named yaml"
```bash
pip install pyyaml
```

### "Permission denied"
```bash
chmod +x tests/stress_tests/*.py
```

### "Log directory not found"
The directory is created automatically on first run.

## Contributing

To add new stress tests:

1. Create test function in appropriate file
2. Use `framework.log_test_result()` to log results
3. Add test to the `run_all_*_tests()` function
4. Test locally before committing

Example:
```python
def test_my_new_stress_case(framework: StressTestFramework):
    try:
        # Try to break something
        dangerous_operation()
        framework.log_test_result(
            "my_test_name",
            "PASS",
            details="System handled dangerous input"
        )
    except ExpectedError:
        framework.log_test_result(
            "my_test_name",
            "EXPECTED_FAIL",
            details="System correctly rejected bad input"
        )
```

## License

SPDX-License-Identifier: CERL-1.0
Copyright (c) 2025 MAYA Node Contributors

---

For detailed documentation, see `tests/stress_tests/README.md`
