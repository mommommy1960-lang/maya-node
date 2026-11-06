"""Bounded synthetic case monitor for MAYA AAO.

Run in a trusted operator environment on a schedule, never from public requests.
No external notifications are sent. Output is a review queue, not authorization.
"""
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

def review(db_path, now=None):
    now = now or datetime.now(timezone.utc)
    c = sqlite3.connect(db_path)
    c.row_factory = sqlite3.Row
    try:
        rows = c.execute("SELECT id, pantry, item, quantity, deadline, status FROM cases WHERE status NOT IN ('delivered','canceled')").fetchall()
    finally:
        c.close()
    alerts = []
    for row in rows:
        r = dict(row)
        try:
            deadline = datetime.fromisoformat(r["deadline"].replace("Z","+00:00"))
            if deadline.tzinfo is None: deadline = deadline.replace(tzinfo=timezone.utc)
            remaining = (deadline - now).total_seconds()
        except (TypeError, ValueError):
            alerts.append({"case_id":r["id"],"reason":"invalid_deadline","severity":"review"})
            continue
        if remaining <= 0:
            alerts.append({"case_id":r["id"],"reason":"deadline_passed","severity":"urgent"})
        elif remaining <= 3600:
            alerts.append({"case_id":r["id"],"reason":"deadline_within_hour","severity":"urgent"})
        elif r["status"] in ("open","escalated"):
            alerts.append({"case_id":r["id"],"reason":"unresolved_case","severity":"review"})
    return alerts

if __name__=="__main__":
    if len(sys.argv)!=2 or not Path(sys.argv[1]).is_file():
        raise SystemExit("Usage: python demos/aao_monitor.py <existing-synthetic-db-path>")
    print(json.dumps({"mode":"synthetic-only","external_alerts_sent":0,"review_queue":review(sys.argv[1])},indent=2))
