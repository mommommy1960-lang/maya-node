# maya-node
### Aurora Node: System Health & Sovereign Diagnostics

This node maintains:
- Automated health reports
- Automated uptime logs
- Automated self-monitoring
- Manual override triggers
- Heartbeat tracking (scheduled + manual)
- Diagnostic snapshots committed to repo history

These workflows ensure continuous integrity checks, stability verification, 
and traceable operational logs across the entire Aurora vessel network.

## Aurora Diagnostics

Monitor system health and status through the Aurora Diagnostics workflow.

**Current Status:** [View AURORA_STATUS.md](docs/AURORA_STATUS.md)  
**Guide:** [Aurora Diagnostics Guide](docs/AURORA_DIAGNOSTICS_GUIDE.md)

Run diagnostics manually:
```bash
gh workflow run "Aurora Diagnostics" --ref main -f branch=main -f mode=manual
```

## Licensing

Commons Governance License – Node Access  
💳 [Purchase Node Access License](https://buy.stripe.com/00w28r4LN7xXalz6k733W00)
