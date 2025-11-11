# Tests

Test suite for MAYA Node sovereign architecture.

## Test Structure

- `runtime/` - Tests for core runtime functionality
- `ethics/` - Tests for ethics engine and constraint verification
- `ledger/` - Tests for ledger integrity and validation

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test suite
python -m pytest tests/runtime/
python -m pytest tests/ethics/
python -m pytest tests/ledger/
```

## Test Coverage

All new code should include:
- Unit tests for individual components
- Integration tests for component interactions
- Ethics verification tests
- Security tests

## License

CERL-1.0
