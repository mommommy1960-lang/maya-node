# Development Guide

Complete guide for setting up your MAYA Node development environment and workflow.

## 📋 Prerequisites

### Required

- **Python**: 3.11 or higher
- **Git**: 2.30 or higher
- **pip**: Latest version
- **venv**: Python virtual environment support

### Recommended

- **make**: For running development commands
- **Docker**: For containerized testing (optional)
- **Node.js**: 18+ (for UI dashboard development)

### Operating Systems

Tested on:
- ✅ Ubuntu 20.04+
- ✅ macOS 12+
- ✅ Windows 10+ (with WSL2 recommended)

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/maya-node.git
cd maya-node
```

### 2. Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
python -c "import src.sovereign.runtime; print('✓ Installation successful')"
```

### 4. Setup Pre-commit Hooks

```bash
pre-commit install
```

### 5. Verify Setup

```bash
# Run tests
make test

# Run linters
make lint

# Run security checks
make security
```

If all commands pass, you're ready to develop! 🎉

## 📁 Project Structure

```
maya-node/
├── src/                      # Source code
│   ├── sovereign/           # Core AI runtime
│   ├── services/            # Distributed services
│   └── api/                 # REST API endpoints
├── tests/                    # Test suites
│   ├── runtime/             # Runtime tests
│   ├── ethics/              # Ethics engine tests
│   └── ledger/              # Ledger tests
├── firmware/                 # Edge device controller
│   ├── controller/          # Main controller logic
│   └── edge-tests/          # Edge testing utilities
├── ui/                       # User interfaces
│   └── web-dashboard/       # React dashboard
├── docs/                     # Documentation
├── examples/                 # Usage examples
└── .github/                  # CI/CD workflows
```

## 🛠️ Development Workflow

### Running Tests

```bash
# All tests
make test

# Specific test suite
python -m pytest tests/runtime/ -v
python -m pytest tests/ethics/ -v
python -m pytest tests/ledger/ -v

# With coverage
make test-coverage

# Watch mode (requires pytest-watch)
ptw
```

### Code Quality

```bash
# Format code (Black + isort)
make format

# Run linters
make lint

# Type checking
make typecheck

# All quality checks
make check
```

### Security Scanning

```bash
# Security checks
make security

# Dependency vulnerability scan
safety check

# Code security scan
bandit -r src/
```

### Running the Runtime

```bash
# Development mode
python -m src.sovereign.runtime

# With Flask API
python -m src.api.endpoints

# With debug logging
PYTHONPATH=. python -m src.sovereign.runtime --debug
```

### Working with Firmware

```bash
cd firmware/controller

# Run controller simulation
python main.py

# Run edge tests
cd ../edge-tests
python sim_load_profiles.py
```

### UI Dashboard Development

```bash
cd ui/web-dashboard

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## 🔧 Development Tools

### Makefile Commands

The project includes a comprehensive Makefile:

```bash
make help          # Show all available commands
make install       # Install dependencies
make install-dev   # Install dev dependencies
make test          # Run tests
make test-coverage # Run tests with coverage
make lint          # Run all linters
make format        # Format code
make security      # Run security checks
make check         # Run all checks (lint + security + test)
make clean         # Clean build artifacts
make docs          # Build documentation
```

### Pre-commit Hooks

Automatically run before each commit:
- Code formatting (Black, isort)
- Linting (Flake8, Pylint)
- CERL-1.0 header verification
- Trailing whitespace removal
- End-of-file fixing

Bypass hooks (not recommended):
```bash
git commit --no-verify
```

### IDE Setup

#### VS Code

Recommended extensions:
- Python (Microsoft)
- Pylance
- Black Formatter
- isort
- GitLens

`.vscode/settings.json`:
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

#### PyCharm

1. Configure Python interpreter to use venv
2. Enable Black formatter in Settings → Tools → Black
3. Configure pytest as default test runner
4. Enable type checking with mypy plugin

## 🧪 Testing Guidelines

### Writing Tests

Place tests in appropriate directory:
- `tests/runtime/` - Core runtime functionality
- `tests/ethics/` - Ethics engine tests
- `tests/ledger/` - Ledger and audit tests

Test file naming:
- `test_<module_name>.py`

Example test:

```python
# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors

import unittest
from src.sovereign.runtime import SovereignRuntime, RuntimeConfig

class TestSovereignRuntime(unittest.TestCase):
    def setUp(self):
        self.config = RuntimeConfig(
            enable_ethics_checks=True,
            require_human_approval=False
        )
        self.runtime = SovereignRuntime(self.config)
    
    def test_initialization(self):
        """Test runtime initialization"""
        self.assertIsNotNone(self.runtime)
        self.assertEqual(self.runtime.state.value, "initializing")
    
    def tearDown(self):
        if self.runtime:
            self.runtime.shutdown()

if __name__ == '__main__':
    unittest.main()
```

### Test Coverage

Maintain >80% coverage:
```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html
```

## 🐛 Debugging

### Python Debugging

```python
# Using pdb
import pdb; pdb.set_trace()

# Using ipdb (better interface)
import ipdb; ipdb.set_trace()

# Using breakpoint() (Python 3.7+)
breakpoint()
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Common Issues

#### Import Errors

```bash
# Ensure PYTHONPATH includes project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or use editable install
pip install -e .
```

#### Test Discovery Issues

```bash
# Ensure __init__.py in all test directories
touch tests/__init__.py
touch tests/runtime/__init__.py
```

## 📦 Building and Packaging

### Building Package

```bash
# Build distribution packages
python -m build

# Install from local build
pip install dist/maya_node-0.5.0-py3-none-any.whl
```

### Version Management

Version is managed in:
- `pyproject.toml`
- `setup.py`
- `src/__init__.py` (if exists)

Update version in all locations when releasing.

## 🔒 Security Development

### Security Checklist

Before committing:
- [ ] No hardcoded credentials or API keys
- [ ] No secrets in code or config files
- [ ] Input validation on all user inputs
- [ ] Proper error handling (no stack traces to users)
- [ ] CERL-1.0 headers on all new files
- [ ] No prohibited use patterns
- [ ] Security scan passes (Bandit)
- [ ] Dependency scan passes (Safety)

### Environment Variables

Use `.env` files (never commit):
```bash
# .env (add to .gitignore)
FLASK_SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://localhost/maya
TPM_ENABLED=false
```

Load in code:
```python
import os
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv('FLASK_SECRET_KEY')
```

## 🚀 Deployment Preparation

### Pre-deployment Checklist

- [ ] All tests passing
- [ ] Code coverage >80%
- [ ] Security scans clean
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] No TODO/FIXME in production code
- [ ] Performance tested

### Building for Production

```bash
# Run full check suite
make check

# Build package
python -m build

# Test installation in fresh environment
python -m venv test_env
test_env/bin/pip install dist/maya_node-*.whl
```

## 💡 Tips and Best Practices

### Code Style

- Follow PEP 8
- Use type hints where beneficial
- Write self-documenting code
- Keep functions small and focused
- Prefer composition over inheritance
- Write tests first (TDD)

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit frequently
git add .
git commit -m "feat(component): description"

# Keep branch updated
git fetch origin
git rebase origin/main

# Push when ready
git push origin feature/my-feature
```

### Performance Profiling

```bash
# Using cProfile
python -m cProfile -o profile.stats src/sovereign/runtime.py

# Analyze with snakeviz
pip install snakeviz
snakeviz profile.stats
```

## 📚 Additional Resources

- [Contributing Guidelines](CONTRIBUTING.md)
- [Onboarding Guide](ONBOARDING.md)
- [Security Policy](SECURITY.md)
- [API Documentation](docs/api.md)
- [Architecture Overview](src/README.md)

## ❓ Getting Help

- **Documentation**: Start here
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and discussions
- **Email**: dev@maya-node.org

## 🎯 Next Steps

Now that you're set up:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Browse open issues labeled `good first issue`
3. Join community discussions
4. Start contributing!

---

**Happy coding! May your functions be pure and your tests be green.** ✨

— The MAYA Node Development Team
