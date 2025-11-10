# maya-node

[![Stress Suite CI](https://github.com/mommommy1960-lang/maya-node/actions/workflows/stress-suite.yml/badge.svg)](https://github.com/mommommy1960-lang/maya-node/actions/workflows/stress-suite.yml)

## Commons Sovereignty Stack

Maya-node implements the canonical Commons Sovereignty Stack project structure, providing a comprehensive framework for Multi-Party Resonance Suppression (MPRS) simulation and governance.

### Project Structure

- **spec/** - JSON schemas and specifications
  - `mprs_inputs.schema.json` - Schema for MPRS input validation
  
- **src/** - Source code
  - `sim/mprs_fastloop.py` - Fast-loop simulation engine for MPRS operations
  - `cup/runtime/hooks_rsombind.py` - RSOM (Runtime Service Orchestration Model) binding hooks
  
- **tests/** - Test suites
  - `stress/test_resonance_suppression.py` - Stress tests for resonance suppression
  - `stress/test_burst_trap.py` - Stress tests for burst detection and trapping
  - `stress/test_collapse_lock.py` - Stress tests for collapse lock mechanism
  
- **logs/** - Telemetry and logging
  - `telemetry_header.csv` - Telemetry data headers for monitoring

### Features

- **MPRS Fast Loop Simulation**: High-performance simulation engine for multi-party resonance suppression
- **Resonance Suppression**: Configurable threshold-based resonance control
- **Burst Detection**: Window-based burst pattern detection and response
- **Collapse Lock**: Safety mechanism to prevent rapid state oscillation
- **RSOM Hooks**: Extensible runtime orchestration with pre/post/error hooks
- **Comprehensive Testing**: Full stress test suite with coverage reporting

### Getting Started

#### Prerequisites

- Python 3.9 or higher
- pytest for running tests

#### Installation

```bash
# Install dependencies
pip install pytest pytest-cov pytest-timeout
```

#### Running Tests

```bash
# Run all stress tests
pytest tests/stress/ -v

# Run specific test suite
pytest tests/stress/test_resonance_suppression.py -v

# Run with coverage
pytest tests/stress/ --cov=src --cov-report=term
```

#### Configuration

MPRS configuration follows the schema defined in `spec/mprs_inputs.schema.json`:

```python
config = {
    'resonance_threshold': 0.7,
    'suppression_factor': 2.0,
    'burst_detection_window': 50,
    'collapse_lock_timeout': 500,
    'telemetry_enabled': False
}
```

### CI/CD

The project includes automated stress testing via GitHub Actions. The stress suite runs on:
- Push to main or feat/stress-suite branches
- Pull requests to main
- Manual workflow dispatch

Tests are executed across Python 3.9, 3.10, and 3.11 with full coverage reporting.

### License

See LICENSE files for details.
 
