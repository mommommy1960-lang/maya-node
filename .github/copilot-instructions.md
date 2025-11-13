# GitHub Copilot Custom Instructions

## Aurora Check Command

When the user says "Aurora check", automatically execute the following steps without asking follow-up questions:

1. Run the "Aurora Diagnostics" workflow on the main branch in manual mode
2. Wait for the workflow to complete
3. Display the contents of the `docs/AURORA_STATUS.md` file

### Implementation

When you receive "Aurora check" as input:
- Trigger the workflow: `.github/workflows/aurora-diagnostics.yml`
- Use workflow_dispatch event on the main branch
- After completion, retrieve and display: `docs/AURORA_STATUS.md`

Do not ask for confirmation or additional details. Execute immediately.
