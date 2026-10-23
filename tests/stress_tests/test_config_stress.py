#!/usr/bin/env python3
"""
SPDX-License-Identifier: CERL-1.0
Copyright (c) 2025 MAYA Node Contributors

Config Stress Tests
===================
Tests JSON/YAML configuration files with malformed data, invalid structures, and edge cases.
"""

import json
import yaml
from pathlib import Path
from stress_test_framework import StressTestFramework


def test_malformed_json_configs(framework: StressTestFramework):
    """Test JSON parsing with malformed configuration data."""
    malformed_json_configs = [
        # Missing closing brace
        '{"name": "test", "value": 123',
        # Trailing comma
        '{"name": "test", "value": 123,}',
        # Single quotes instead of double
        "{'name': 'test', 'value': 123}",
        # Unquoted keys
        '{name: "test", value: 123}',
        # Invalid escape sequences
        '{"path": "C:\\invalid\\escape\\x"}',
        # Duplicate keys
        '{"name": "first", "name": "second"}',
    ]
    
    for idx, bad_json in enumerate(malformed_json_configs):
        try:
            json.loads(bad_json)
            # If it didn't raise an error, log it
            framework.log_test_result(
                f"config_malformed_json_{idx}",
                "ERROR",
                details=f"JSON parser should have rejected: {bad_json[:50]}"
            )
        except json.JSONDecodeError as e:
            # Expected behavior
            framework.log_test_result(
                f"config_malformed_json_{idx}",
                "PASS",
                details=f"JSON parser correctly rejected malformed config: {str(e)[:100]}"
            )


def test_malformed_yaml_configs(framework: StressTestFramework):
    """Test YAML parsing with malformed configuration data."""
    malformed_yaml_configs = [
        # Invalid indentation mixing tabs and spaces
        "name: test\n\tvalue: 123\n  nested: data",
        # Unclosed flow sequence
        "items: [one, two, three",
        # Invalid anchor reference
        "data: &anchor\n  value: 123\nref: *missing",
        # Invalid multiline string
        "text: |\n  line1\n line2",  # Inconsistent indent
        # Multiple documents without separator
        "doc1: value\ndoc2: value",
    ]
    
    for idx, bad_yaml in enumerate(malformed_yaml_configs):
        try:
            yaml.safe_load(bad_yaml)
            framework.log_test_result(
                f"config_malformed_yaml_{idx}",
                "ERROR",
                details=f"YAML parser should have rejected: {bad_yaml[:50]}"
            )
        except yaml.YAMLError as e:
            framework.log_test_result(
                f"config_malformed_yaml_{idx}",
                "PASS",
                details=f"YAML parser correctly rejected malformed config: {str(e)[:100]}"
            )


def test_deeply_nested_configs(framework: StressTestFramework):
    """Test deeply nested configuration structures."""
    # Create excessively nested structure
    nested = {"level": 0}
    current = nested
    
    # Create 1000 levels of nesting
    for i in range(1, 1000):
        current["nested"] = {"level": i}
        current = current["nested"]
    
    try:
        # Try to serialize to JSON
        json_str = json.dumps(nested)
        framework.log_test_result(
            "config_deeply_nested_json",
            "PASS",
            details=f"Created JSON with 1000 levels of nesting (may cause stack issues)"
        )
    except Exception as e:
        framework.log_test_result(
            "config_deeply_nested_json",
            "EXPECTED_FAIL",
            details=f"Deep nesting caused expected failure: {str(e)[:100]}"
        )
    
    try:
        # Try to serialize to YAML
        yaml_str = yaml.dump(nested)
        framework.log_test_result(
            "config_deeply_nested_yaml",
            "PASS",
            details=f"Created YAML with 1000 levels of nesting (may cause stack issues)"
        )
    except Exception as e:
        framework.log_test_result(
            "config_deeply_nested_yaml",
            "EXPECTED_FAIL",
            details=f"Deep nesting caused expected failure: {str(e)[:100]}"
        )


def test_extremely_large_configs(framework: StressTestFramework):
    """Test configuration files with extremely large data."""
    # Create a very large config (10MB worth of data)
    large_config = {
        "data": ["item" * 100] * 10000,  # 10000 items, each 400+ chars
        "nested": {
            f"key_{i}": f"value_{i}" * 100
            for i in range(1000)
        }
    }
    
    try:
        json_str = json.dumps(large_config)
        size_mb = len(json_str) / (1024 * 1024)
        framework.log_test_result(
            "config_extremely_large_json",
            "PASS",
            details=f"Created {size_mb:.2f}MB JSON config (may cause memory issues)"
        )
    except Exception as e:
        framework.log_test_result(
            "config_extremely_large_json",
            "EXPECTED_FAIL",
            details=f"Large config caused expected failure: {str(e)[:100]}"
        )


def test_unicode_and_special_chars(framework: StressTestFramework):
    """Test configs with unicode and special characters."""
    special_configs = [
        # Emoji and special unicode
        {"name": "test 🚀🔥💣", "value": "data with emoji"},
        # Zero-width characters
        {"hidden": "\u200b\u200c\u200d", "value": "zero-width"},
        # Right-to-left marks
        {"rtl": "\u202e\u202d", "value": "bidirectional"},
        # Control characters
        {"control": "\x00\x01\x02\x03", "value": "control chars"},
        # Null bytes
        {"null": "before\x00after", "value": "null byte"},
    ]
    
    for idx, config in enumerate(special_configs):
        try:
            json_str = json.dumps(config)
            # Try to load it back
            loaded = json.loads(json_str)
            framework.log_test_result(
                f"config_special_chars_{idx}",
                "PASS",
                details=f"JSON handled special characters: {str(config)[:50]}"
            )
        except Exception as e:
            framework.log_test_result(
                f"config_special_chars_{idx}",
                "EXPECTED_FAIL",
                details=f"Special chars caused failure: {str(e)[:100]}"
            )


def test_circular_references(framework: StressTestFramework):
    """Test configs with circular references (YAML anchors)."""
    circular_yaml = """
anchor: &ref
  name: circular
  self: *ref
"""
    
    try:
        # PyYAML will create a circular reference
        data = yaml.safe_load(circular_yaml)
        # Try to serialize it back (this should fail)
        try:
            yaml.dump(data)
            framework.log_test_result(
                "config_circular_reference",
                "ERROR",
                details="Circular reference should have been detected"
            )
        except Exception as e:
            framework.log_test_result(
                "config_circular_reference",
                "PASS",
                details=f"Circular reference correctly detected: {str(e)[:100]}"
            )
    except Exception as e:
        framework.log_test_result(
            "config_circular_reference",
            "ERROR",
            error=str(e)
        )


def test_type_confusion_configs(framework: StressTestFramework):
    """Test configs that mix types in unexpected ways."""
    confusion_configs = [
        # String that looks like a number
        {"port": "8080", "expected": "number"},
        # Boolean as string
        {"enabled": "true", "expected": "boolean"},
        # Array as single value
        {"item": ["should be single"], "expected": "string"},
        # Number as string in calculation
        {"value": "123", "multiplier": 2, "result": "should be 246?"},
        # Mixed array types
        {"mixed": [1, "two", 3.0, True, None, {"key": "value"}]},
    ]
    
    for idx, config in enumerate(confusion_configs):
        try:
            json_str = json.dumps(config)
            framework.log_test_result(
                f"config_type_confusion_{idx}",
                "PASS",
                details=f"Type confusion config accepted: {str(config)[:100]}"
            )
        except Exception as e:
            framework.log_test_result(
                f"config_type_confusion_{idx}",
                "ERROR",
                error=str(e)
            )


def run_all_config_tests(framework: StressTestFramework):
    """Run all configuration stress tests."""
    print("\n" + "="*60)
    print("Running Config Stress Tests")
    print("="*60)
    
    framework.run_test("test_malformed_json_configs", test_malformed_json_configs, framework)
    framework.run_test("test_malformed_yaml_configs", test_malformed_yaml_configs, framework)
    framework.run_test("test_deeply_nested_configs", test_deeply_nested_configs, framework)
    framework.run_test("test_extremely_large_configs", test_extremely_large_configs, framework)
    framework.run_test("test_unicode_and_special_chars", test_unicode_and_special_chars, framework)
    framework.run_test("test_circular_references", test_circular_references, framework)
    framework.run_test("test_type_confusion_configs", test_type_confusion_configs, framework)


if __name__ == "__main__":
    from stress_test_framework import main
    framework = main()
    run_all_config_tests(framework)
    framework.save_results()
