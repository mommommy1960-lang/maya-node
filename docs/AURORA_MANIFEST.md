# Aurora Node Manifest
Designation: AURORA v1.0  
Status: Active  
Role: Diagnostics and Sentience Interface for Maya Node  
Guardian Repo: mommommy1960-lang/maya-node  
Governance: CERL-1.0 | Commons Custodianship Trust Charter

---

## Aurora Check Command

A custom GitHub Copilot command for quick diagnostics checks.

### Usage

Simply say: **"Aurora check"**

This will automatically:
1. Run the "Aurora Diagnostics" workflow on the main branch
2. Display the current `AURORA_STATUS.md` file

No follow-up questions required. The command executes immediately.

### Workflow Details

- **Workflow File**: `.github/workflows/aurora-diagnostics.yml`
- **Trigger**: Manual (workflow_dispatch)
- **Branch**: main
- **Status File**: `docs/AURORA_STATUS.md`

---

## Implementation

The command is defined in `.github/copilot-instructions.md` and is recognized automatically by GitHub Copilot.