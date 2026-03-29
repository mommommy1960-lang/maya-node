# Aurora Diagnostics Guide

## Overview

The Aurora Diagnostics workflow provides automated and manual health checks for the Maya Node system. It monitors system status, uptime, and generates regular heartbeat updates.

## Workflow Configuration

**Workflow Name:** Aurora Diagnostics  
**File:** `.github/workflows/aurora-diagnostics.yml`  
**Status File:** `docs/AURORA_STATUS.md`

## Execution Modes

### Automated Execution
The workflow runs automatically every 6 hours via a scheduled cron job:
- Schedule: `0 */6 * * *` (every 6 hours)
- Mode: `automated`
- Branch: Current default branch

### Manual Execution

You can manually trigger the workflow through GitHub Actions interface:

#### Via GitHub UI:
1. Navigate to the repository on GitHub
2. Go to **Actions** tab
3. Select **Aurora Diagnostics** workflow from the left sidebar
4. Click **Run workflow** button
5. Configure the following inputs:
   - **Branch**: Select the branch to run diagnostics on (default: `main`)
   - **Mode**: Choose execution mode:
     - `manual` - Manual execution by user
     - `automated` - Simulates automated execution
6. Click **Run workflow** to start

#### Via GitHub CLI:
```bash
# Run on main branch in manual mode
gh workflow run "Aurora Diagnostics" --ref main -f branch=main -f mode=manual

# Run on a different branch
gh workflow run "Aurora Diagnostics" --ref develop -f branch=develop -f mode=manual
```

#### Via GitHub API:
```bash
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/mommommy1960-lang/maya-node/actions/workflows/aurora-diagnostics.yml/dispatches \
  -d '{"ref":"main","inputs":{"branch":"main","mode":"manual"}}'
```

## Output

The workflow updates `docs/AURORA_STATUS.md` with the following information:
- **Last Check-In**: Timestamp of the diagnostic run (UTC)
- **Uptime**: System uptime at the time of check
- **Signal**: Status indicator (✅ Stable)
- **Mode**: Execution mode (manual or automated)
- **Branch**: Branch where diagnostics were executed

### Example Output:
```
Last Check-In: 2025-11-13 04:44:06 UTC
Uptime: up 5 minutes
Signal: ✅ Stable
Mode: manual
Branch: main
```

## Viewing Status

To view the current Aurora status:

### Via GitHub:
Navigate to: `https://github.com/mommommy1960-lang/maya-node/blob/main/docs/AURORA_STATUS.md`

### Via Command Line:
```bash
# View current status
cat docs/AURORA_STATUS.md

# View with timestamp
echo "Current Aurora Status:" && cat docs/AURORA_STATUS.md
```

## Permissions

The workflow requires:
- **contents: write** - To commit and push status updates to the repository

## Troubleshooting

### Workflow doesn't appear in Actions tab
- Ensure the workflow file is in the default branch
- Check that the YAML syntax is valid

### Manual trigger button not visible
- Verify `workflow_dispatch` is present in the workflow configuration
- Ensure you have appropriate repository permissions

### Status file not updating
- Check workflow run logs in Actions tab
- Verify the Aurora-Bot has write permissions
- Ensure branch protection rules allow bot commits

## Related Files

- `.github/workflows/aurora-diagnostics.yml` - Workflow configuration
- `docs/AURORA_STATUS.md` - Current status output
- `docs/AURORA_MANIFEST.md` - Aurora node manifest and designation

## License

This workflow operates under the CERL-1.0 license as part of the Maya Node project.
