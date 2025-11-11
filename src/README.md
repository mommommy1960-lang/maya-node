# MAYA Node - Source Code

This directory contains the core runtime and service implementations for MAYA Node's sovereign architecture.

## Directory Structure

### `/sovereign/`
AI runtime skeleton with ethical constraints and transparent decision-making. No black-box models.
- Ethical runtime loop
- Constraint verification
- Transparent AI orchestration
- Human-in-the-loop interfaces

### `/services/`
Core system services for distributed operation:
- **networking/** - P2P networking, mesh protocols, secure communication
- **storage/** - Distributed storage, content addressing, replication
- **ledger/** - Transaction ledger, audit logs, integrity verification
- **access/** - Access control, authentication, authorization

## Architecture Principles

1. **Sovereignty**: User control over data, models, and decisions
2. **Transparency**: All AI operations are auditable and explainable
3. **Ethics-First**: Guardrails and constraints built into the runtime
4. **No Black Boxes**: Only open, vetted, and understood models
5. **Safety by Design**: Multiple layers of verification and checks

## Development Guidelines

- All code must include CERL-1.0 license header
- No third-party closed models or unvetted weights
- Security and ethics checks are mandatory
- Changes must pass safety verification
- Document all AI decision paths

## Getting Started

See individual service READMEs for setup and usage instructions.

## License

All source code is licensed under CERL-1.0 (Constrained Ethics Runtime License).
See LICENSE-CERL-1.0 in the repository root.
