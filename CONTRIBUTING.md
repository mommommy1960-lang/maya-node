# Contributing to MAYA Node

Thank you for your interest in contributing to MAYA Node! This project is building sovereign AI infrastructure with ethical constraints, and we welcome contributions that align with our mission.

## 🧡 Code of Conduct

This project operates under the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold these standards.

## 📜 License & Ethics

MAYA Node is licensed under **CERL-1.0** (Constrained Ethics Runtime License). All contributions must:

- ✅ Comply with CERL-1.0 requirements
- ✅ Include proper license headers
- ✅ Respect ethical boundaries
- ✅ Maintain transparency and auditability
- ✅ Never enable prohibited uses (weaponization, surveillance, discrimination)

**Read**: [LICENSE-CERL-1.0](LICENSE-CERL-1.0) before contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- A GitHub account

### Development Setup

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed setup instructions.

Quick start:
```bash
# Clone repository
git clone https://github.com/yourusername/maya-node.git
cd maya-node

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests to verify setup
make test
```

## 🔀 How to Contribute

### 1. Find or Create an Issue

- Browse [existing issues](https://github.com/yourusername/maya-node/issues)
- Look for issues labeled `good first issue` or `help wanted`
- If you have a new idea, create an issue first to discuss it

### 2. Fork and Branch

```bash
# Fork the repository on GitHub, then:
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test improvements
- `security/` - Security fixes

### 3. Make Your Changes

#### Code Guidelines

- **Python Style**: Follow PEP 8, enforced by Black (line length: 88)
- **Type Hints**: Use type annotations where appropriate
- **Docstrings**: Use clear docstrings for public functions/classes
- **Comments**: Explain *why*, not *what* (code should be self-documenting)
- **CERL Headers**: All Python files must include CERL-1.0 headers

#### License Headers

All new Python files must start with:

```python
# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.
```

### 4. Write Tests

- All new features require tests
- Bug fixes should include regression tests
- Aim for >80% code coverage
- Run tests locally: `make test`

### 5. Run Quality Checks

Before committing:

```bash
# Format code
make format

# Run linters
make lint

# Run security checks
make security

# Run all checks
make check
```

### 6. Commit Your Changes

**Commit Message Format:**

```
type(scope): brief description

Longer description if needed, explaining why this change
is being made and what problem it solves.

Closes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `security`: Security improvements
- `chore`: Maintenance tasks

**Examples:**
```
feat(runtime): add consent token validation

Implements validation logic for consent tokens to ensure
all operations have proper authorization.

Closes #45

---

fix(ethics): correct boundary detection in constraint engine

The previous logic had an edge case where nested operations
could bypass ethical checks. This fix ensures all operations
are properly validated.

Closes #78
```

### 7. Push and Create Pull Request

```bash
git push origin your-branch-name
```

Then create a Pull Request on GitHub with:

- **Clear title** following commit message format
- **Description** explaining the change and its purpose
- **Related issues** (use "Closes #123" or "Fixes #456")
- **Testing notes** for reviewers
- **Screenshots** if applicable (UI changes)

## 🔍 Review Process

### What Reviewers Look For

- ✅ Code quality and style
- ✅ Test coverage
- ✅ Security implications
- ✅ CERL-1.0 compliance
- ✅ Documentation updates
- ✅ Ethical considerations
- ✅ Performance impact
- ✅ Breaking changes

### CI/CD Checks

All PRs must pass:

1. **Security Scanning** (Bandit, Safety)
2. **Ethics Verification** (CERL headers, prohibited patterns)
3. **Code Quality** (Pylint, Black, Flake8)
4. **Test Suite** (All tests passing)
5. **Coverage** (No significant coverage decrease)

### Review Timeline

- **Initial review**: Within 3-5 business days
- **Follow-up reviews**: Within 2 business days after changes
- **Merge**: After 1-2 approvals (depending on change scope)

## 🎯 Contribution Areas

### Priority Areas

1. **Core Runtime** - Sovereign AI runtime improvements
2. **Ethics Engine** - Constraint verification enhancements
3. **Testing** - More comprehensive test coverage
4. **Documentation** - Tutorials, guides, API docs
5. **Security** - Security audits and improvements
6. **Performance** - Optimization and efficiency
7. **Examples** - Real-world usage examples

### Good First Issues

Look for issues labeled `good first issue` - these are:
- Well-documented
- Limited scope
- Good learning opportunities
- Have mentorship available

## 📚 Resources

### Documentation

- [Development Guide](DEVELOPMENT.md)
- [Onboarding Guide](ONBOARDING.md)
- [Architecture Documentation](docs/)
- [API Reference](docs/api.md)

### Community

- **Discussions**: GitHub Discussions
- **Issues**: GitHub Issues
- **Email**: dev@maya-node.org

### Learning Resources

- [CERL-1.0 License](LICENSE-CERL-1.0)
- [Ethics Engine Design](src/sovereign/README.md)
- [Test Examples](tests/README.md)

## ❓ Questions?

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Open an issue with the `bug` label
- **Feature requests**: Open an issue with the `enhancement` label
- **Security issues**: See [SECURITY.md](SECURITY.md)

## 🏆 Recognition

Contributors are recognized in:
- [AUTHORS.md](AUTHORS.md)
- Release notes
- Project documentation

## 🚫 What We Don't Accept

We **will not** accept contributions that:

- ❌ Violate CERL-1.0 constraints
- ❌ Enable prohibited uses (weapons, surveillance, discrimination)
- ❌ Introduce security vulnerabilities
- ❌ Lack proper testing
- ❌ Include proprietary/closed-source dependencies
- ❌ Violate code of conduct
- ❌ Include malicious code

## 💡 Tips for Success

1. **Start small** - Begin with documentation or small bug fixes
2. **Communicate early** - Discuss large changes before implementing
3. **Read the code** - Understand existing patterns and architecture
4. **Ask questions** - We're here to help!
5. **Be patient** - Quality reviews take time
6. **Iterate** - Expect and embrace feedback

## 📝 Checklist

Before submitting a PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated (if applicable)
- [ ] CERL-1.0 headers included in new files
- [ ] Commit messages follow format
- [ ] PR description is clear and complete
- [ ] Related issues are linked
- [ ] No security vulnerabilities introduced
- [ ] Ethical constraints respected

---

**Thank you for contributing to MAYA Node!**

*"Together we build sovereign AI infrastructure that respects human agency and ethical boundaries."*

— The MAYA Node Team
