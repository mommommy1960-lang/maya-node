# Welcome to MAYA Node! 🎉

Welcome aboard! We're excited to have you join the MAYA Node community. This guide will help you get started and feel at home in our sovereign AI infrastructure project.

## 🌟 What is MAYA Node?

MAYA Node is building **sovereign AI infrastructure** with:

- ✅ **Ethical Constraints** - Built-in guardrails via CERL-1.0 license
- ✅ **Transparency** - All AI decisions are auditable and explainable
- ✅ **User Sovereignty** - Users control their data and models
- ✅ **No Black Boxes** - Only open, vetted, understood AI systems
- ✅ **Distributed Architecture** - Peer-to-peer, resilient infrastructure
- ✅ **Human Oversight** - Human-in-the-loop for critical decisions

**Our Mission**: Build AI infrastructure that respects human agency and operates within ethical boundaries.

## 🎯 Quick Start Paths

Choose your path based on your role:

### 👨‍💻 I want to contribute code
→ Go to [For Developers](#-for-developers) below

### 📝 I want to improve documentation
→ Go to [For Documentation Writers](#-for-documentation-writers) below

### 🐛 I found a bug
→ Go to [Reporting Issues](#-reporting-issues) below

### 🔒 I found a security issue
→ Read [SECURITY.md](SECURITY.md) immediately

### 💡 I have a feature idea
→ Go to [Suggesting Features](#-suggesting-features) below

### 🤔 I just want to understand the project
→ Keep reading this guide!

## 📚 Essential Reading (15 minutes)

Before diving in, please read:

1. **[README.md](README.md)** (2 min) - Project overview
2. **[LICENSE-CERL-1.0](LICENSE-CERL-1.0)** (5 min) - Our ethical license
3. **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** (3 min) - Community standards
4. **[CONTRIBUTING.md](CONTRIBUTING.md)** (5 min) - How to contribute

**Why CERL-1.0?** Unlike traditional open source licenses, CERL-1.0 includes ethical constraints that prevent the software from being used for harmful purposes like weaponization or mass surveillance.

## 🏗️ Project Architecture (High Level)

```
MAYA Node
├── Sovereign Runtime          # Core AI execution engine
│   ├── Ethics Engine         # Constraint verification
│   ├── Model Interface       # AI model abstraction
│   └── Human-in-the-Loop     # Human oversight system
│
├── Distributed Services      # Infrastructure
│   ├── Immutable Ledger      # Audit trail
│   ├── Storage (CAS)         # Content-addressed storage
│   ├── Networking (P2P)      # Peer-to-peer communication
│   └── Access Control        # RBAC system
│
├── API Layer                 # REST endpoints
├── Firmware Controller       # Edge device support
└── UI Dashboard              # Web interface
```

## 👨‍💻 For Developers

### Prerequisites

- **Python**: 3.11+ (Required)
- **Git**: 2.30+ (Required)
- **Node.js**: 18+ (Optional, for UI work)
- **Make**: (Optional but recommended)

### Step-by-Step Setup

#### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/maya-node.git
cd maya-node
```

#### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

#### 3. Install Dependencies

```bash
# Install in development mode
pip install -e ".[dev]"
```

#### 4. Setup Pre-commit Hooks

```bash
pre-commit install
```

#### 5. Verify Installation

```bash
# Run tests
python -m pytest tests/ -v

# If tests pass, you're ready! 🎉
```

### Your First Contribution

1. **Find an issue** labeled `good first issue`
2. **Comment** on the issue to claim it
3. **Create a branch**: `git checkout -b fix/issue-123`
4. **Make your changes** following our style guide
5. **Add tests** for your changes
6. **Run checks**: `make check` (or manually run tests/linters)
7. **Commit**: `git commit -m "fix(component): description"`
8. **Push**: `git push origin fix/issue-123`
9. **Create Pull Request** on GitHub

**Need help?** Ask questions in the issue comments or GitHub Discussions!

### Development Commands

```bash
make test          # Run all tests
make lint          # Run linters
make format        # Format code
make security      # Run security checks
make check         # Run all checks
make help          # See all commands
```

## 📝 For Documentation Writers

Documentation is critical! Here's how you can help:

### What Needs Documentation?

- **Code examples** - Real-world usage examples
- **Tutorials** - Step-by-step guides
- **API docs** - Function/class documentation
- **Architecture docs** - System design explanations
- **FAQ** - Common questions and answers
- **Troubleshooting** - Common issues and solutions

### Documentation Structure

```
docs/
├── api.md                    # API reference
├── deployment-checklist.md   # Deployment guide
├── whitepaper-outline.md     # Technical whitepaper
└── (add more docs here!)
```

### Writing Style

- **Clear and concise** - Avoid jargon when possible
- **Examples included** - Show, don't just tell
- **Accessible** - Assume beginner-level knowledge
- **Accurate** - Test all code examples
- **CERL-1.0 aware** - Mention ethical constraints where relevant

### Documentation Workflow

1. Identify documentation gap
2. Create issue or comment on existing one
3. Write documentation in Markdown
4. Add code examples (test them!)
5. Submit PR with documentation changes
6. Reviewers will help refine

## 🐛 Reporting Issues

### Before Creating an Issue

- Search existing issues (open and closed)
- Try latest version
- Gather relevant information

### Creating a Bug Report

Include:
- **Description**: What happened vs. what you expected
- **Steps to reproduce**: Detailed steps
- **Environment**: OS, Python version, package versions
- **Logs/Errors**: Full error messages
- **Code samples**: Minimal reproducing example

Use issue templates provided in `.github/ISSUE_TEMPLATE/`.

### Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `security` - Security-related issues

## 💡 Suggesting Features

We love new ideas! Here's how to propose features:

1. **Check existing issues** - It might already be proposed
2. **Create discussion** - Start in GitHub Discussions
3. **Explain the need** - What problem does it solve?
4. **Describe the solution** - How should it work?
5. **Consider ethics** - Does it align with CERL-1.0?
6. **Discuss impact** - How does it affect existing features?

Features that align with our mission and ethics are more likely to be accepted.

## 🤝 Community Guidelines

### Communication Channels

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - Questions, ideas, and community chat
- **Pull Requests** - Code review and collaboration
- **Email** - info@maya-node.org for general inquiries

### Code of Conduct

We maintain a welcoming, inclusive environment. Key principles:

- **Be respectful** - Treat everyone with kindness
- **Be constructive** - Focus on ideas, not people
- **Be patient** - Remember we're all learning
- **Be ethical** - Uphold CERL-1.0 values

Full details: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## 🎓 Learning Resources

### Understanding MAYA Node

- **[src/README.md](src/README.md)** - Source code overview
- **[tests/README.md](tests/README.md)** - Testing guide
- **[docs/api.md](docs/api.md)** - API reference
- **Phase Summaries** - PHASE-F-SUMMARY.md, PHASE-OMEGA-SUMMARY.md

### External Resources

- **CERL-1.0** - Constrained Ethics Runtime License
- **Python Docs** - python.org
- **Flask Docs** - flask.palletsprojects.com
- **Git Workflow** - GitHub flow guide

## 🚀 Next Steps

Now that you're oriented:

1. ✅ Read essential docs (above)
2. ✅ Set up development environment
3. ✅ Join GitHub Discussions
4. ✅ Find a `good first issue`
5. ✅ Introduce yourself in Discussions
6. ✅ Make your first contribution!

## ❓ FAQ

### Q: I'm new to open source. Can I still contribute?

**A:** Absolutely! We welcome first-time contributors. Start with documentation or `good first issue` labeled items.

### Q: What if I don't know Python?

**A:** You can contribute documentation, test cases, design, or help with the TypeScript UI dashboard!

### Q: How long until my PR is reviewed?

**A:** Usually 3-5 business days for initial review. We'll provide feedback and work with you to get it merged.

### Q: Can I use MAYA Node in my project?

**A:** Yes! Review the [LICENSE-CERL-1.0](LICENSE-CERL-1.0) to understand the ethical constraints. You're free to use it as long as you comply with CERL-1.0.

### Q: What if I disagree with a decision?

**A:** Open a discussion! We make decisions transparently and welcome constructive debate.

### Q: Can AI agents contribute code?

**A:** Yes! MAYA Node has an AI agent council that participates in development under CERL-1.0 constraints. See `.github/agents/` for agent governance.

## 🎯 Contribution Ideas by Skill Level

### Beginner
- Fix typos in documentation
- Add code comments
- Write test cases
- Improve error messages

### Intermediate
- Add new test coverage
- Implement feature requests
- Refactor code for clarity
- Write tutorials

### Advanced
- Optimize performance
- Design new architecture components
- Security audits
- Complex feature implementation

## 🏆 Recognition

Contributors are recognized:
- In [AUTHORS.md](AUTHORS.md)
- In release notes
- In project announcements

Your contributions matter!

## 📬 Getting Help

Stuck? Need help? Contact us:

- **GitHub Discussions** - Best for technical questions
- **GitHub Issues** - For bugs and feature requests
- **Email** - help@maya-node.org

We aim to respond within 48 hours.

## 🎊 Welcome Again!

We're thrilled you're here. MAYA Node is built by contributors like you who believe in sovereign, ethical AI infrastructure.

**Let's build the future together!** 🚀

---

*"The best time to plant a tree was 20 years ago. The second best time is now."* — Chinese Proverb

## 📝 Checklist: Am I Ready?

Before making your first contribution:

- [ ] I've read the README
- [ ] I understand CERL-1.0 license
- [ ] I've read the Code of Conduct
- [ ] I've read Contributing Guidelines
- [ ] My dev environment is set up
- [ ] Tests pass on my machine
- [ ] I've found an issue to work on
- [ ] I'm ready to contribute!

If you checked all boxes, **go for it!** 🎉

---

**Questions about this guide?** Open an issue or discussion!

— The MAYA Node Team
