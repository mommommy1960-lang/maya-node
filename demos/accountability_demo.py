"""Synthetic accountability model; no live pickup, payments or notifications."""
from dataclasses import dataclass
import json


@dataclass
class Grant:
    subject: str
    action: str
    resource: str
    expires: int
    revoked: bool = False


class Demo:
    def __init__(self):
        self.events = []
        self.cases = {}
        self.grants = []
        self.primary = "DEMO-STAFF-1"
        self.backup = "DEMO-STAFF-2"
        self.lead = "DEMO-LEAD"
        self.away = False
        self.handoff = None

    def record(self, kind, **details):
        event = dict(sequence=len(self.events) + 1, kind=kind, **details)
        self.events.append(event)
        return event

    def owner(self, now):
        if not self.away:
            return self.primary
        if self.handoff and self.handoff[0] <= now < self.handoff[1]:
            return self.backup
        return None

    def accept_handoff(self, actor, start, end):
        if actor != self.backup or start >= end:
            raise ValueError("Valid backup acceptance and time window required")
        self.handoff = (start, end)
        self.record("handoff.accepted", actor=actor, start=start, end=end)

    def authorized(self, subject, action, resource, now):
        return any(g.subject == subject and g.action == action and
                   g.resource == resource and not g.revoked and now < g.expires
                   for g in self.grants)

    def attempt(self, subject, action, resource, now, ai_approval=True):
        # AI approval is evidence only. It never grants execution authority.
        permit = self.authorized(subject, action, resource, now)
        covered = self.owner(now) is not None
        allowed = permit and covered
        self.record("action.checked", subject=subject, action=action,
                    resource=resource, ai_approval=ai_approval,
                    permission=permit, coverage=covered, allowed=allowed,
                    owner=self.owner(now), at=now)
        if not allowed:
            return self.open_case(subject, resource, now,
                                  "authorization_or_coverage_failure")
        return {"allowed": True, "simulated": True}

    def open_case(self, subject, resource, now, reason):
        case_id = f"DEMO-CASE-{len(self.cases)+1}"
        case = dict(id=case_id, subject=subject, resource=resource, opened=now,
                    owner=self.owner(now) or self.lead, reason=reason,
                    status="review_required", acknowledged=None,
                    escalation_level=0, advocate=None)
        self.cases[case_id] = case
        self.record("case.opened", case_id=case_id, owner=case["owner"],
                    simulated_notification=True)
        return {"allowed": False, "case_id": case_id, "simulated": True}

    def escalate(self, case_id, now):
        c = self.cases[case_id]
        if now < c["opened"]:
            raise ValueError("Time precedes incident")
        if c["acknowledged"] is not None:
            return
        level = 2 if now-c["opened"] >= 60 else 1 if now-c["opened"] >= 30 else 0
        if level > c["escalation_level"]:
            c["escalation_level"] = level
            backup_valid = self.handoff and self.handoff[0] <= now < self.handoff[1]
            c["owner"] = self.backup if level == 1 and backup_valid else self.lead
            self.record("case.escalated", case_id=case_id, owner=c["owner"],
                        at=now, simulated_notification=True)

    def acknowledge(self, case_id, actor, now):
        c = self.cases[case_id]
        if actor != c["owner"] or now < c["opened"]:
            raise PermissionError("Only current assigned owner can acknowledge")
        if c["acknowledged"] is not None:
            raise ValueError("Acknowledgment already recorded")
        c["acknowledged"] = now
        self.record("case.acknowledged", case_id=case_id, actor=actor, at=now)
        return now-c["opened"] < 120

    def grant_advocate(self, case_id, actor, advocate, expires=300):
        c = self.cases[case_id]
        if actor != c["subject"]:
            raise PermissionError("Affected demo person must grant access")
        c["advocate"] = advocate
        c["advocate_expires"] = expires
        self.record("advocate.granted", case_id=case_id, actor=actor,
                    advocate=advocate, simulated_notification=True)

    def revoke_advocate(self, case_id, actor):
        c = self.cases[case_id]
        if actor != c["subject"]:
            raise PermissionError("Affected demo person must revoke access")
        c["advocate"] = None
        self.record("advocate.revoked", case_id=case_id, actor=actor)

    def view(self, case_id, actor, now=0):
        c = self.cases[case_id]
        advocate_valid = (actor == c["advocate"] and
                          now < c.get("advocate_expires", 0))
        if actor not in (c["subject"], c["owner"]) and not advocate_valid:
            raise PermissionError("Case access denied")
        return dict(c)

    def export_case(self, case_id, actor, now=0):
        case = self.view(case_id, actor, now)
        # Exclude every other case, even when its actor happens to be the same.
        evidence = [dict(e) for e in self.events if e.get("case_id") == case_id]
        return {"scope": "SYNTHETIC CASE EXPORT", "case": case, "events": evidence}

    def correct(self, case_id, actor, evidence):
        c = self.cases[case_id]
        if actor != c["owner"] or not evidence:
            raise PermissionError("Owner and correction evidence required")
        c["status"] = "correction_pending_verification"
        self.record("correction.started", case_id=case_id, actor=actor, evidence=evidence)

    def verify(self, case_id, reviewer, verified):
        c = self.cases[case_id]
        if reviewer != self.lead or reviewer == c["owner"]:
            raise PermissionError("Separate designated reviewer required")
        if c["status"] != "correction_pending_verification":
            raise ValueError("No correction awaiting review")
        c["status"] = "resolved" if verified else "review_required"
        self.record("correction.reviewed", case_id=case_id, actor=reviewer,
                    verified=verified)


def walkthrough():
    school = Demo()
    school.away = True
    school.accept_handoff(school.backup, 0, 300)
    school.grants.append(Grant("DEMO-PARENT-A", "pickup", "DEMO-CHILD", 300))
    result = school.attempt("DEMO-COLLECTOR-B", "pickup", "DEMO-CHILD", 0)
    school.acknowledge(result["case_id"], school.backup, 20)
    billing = Demo()
    billing.grants.append(Grant("DEMO-CUSTOMER", "charge", "DEMO-SUB", 300, True))
    payment = billing.attempt("DEMO-CUSTOMER", "charge", "DEMO-SUB", 0)
    cid = payment["case_id"]
    billing.acknowledge(cid, billing.primary, 15)
    billing.grant_advocate(cid, "DEMO-CUSTOMER", "DEMO-ADVOCATE")
    billing.correct(cid, billing.primary, "Synthetic cancellation record checked")
    billing.verify(cid, billing.lead, True)
    return dict(scope="FICTIONAL IN-MEMORY SIMULATION ONLY",
                school=school.events, billing=billing.events,
                advocate_view=billing.view(cid, "DEMO-ADVOCATE"))


if __name__ == "__main__":
    print(json.dumps(walkthrough(), indent=2))
