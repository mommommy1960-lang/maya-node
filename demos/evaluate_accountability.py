"""Repeatable synthetic boundary evaluation; not field reliability evidence."""
from itertools import product
import json
import math
import random
from demos.accountability_demo import Demo, Grant


def evaluate(seed=20261013, random_trials=1000):
    rng = random.Random(seed)
    failures = []
    counts = {"allowed": 0, "blocked": 0, "unauthorized_allowed": 0,
              "unassigned_cases": 0, "missing_decision_evidence": 0}
    base = list(product((False, True), repeat=7))
    cases = [(sector, flags) for sector in ("school", "billing") for flags in base]
    cases += [(sector, tuple(bool(rng.getrandbits(1)) for _ in range(7)))
              for sector in ("school", "billing") for _ in range(random_trials)]
    sectors = {sector: {"trials": 0, "correct": 0} for sector in ("school", "billing")}
    for index, (sector, flags) in enumerate(cases):
        wrong_person, wrong_resource, wrong_action, expired, revoked, away, accepted = flags
        now = rng.randrange(1, 10000)
        d = Demo(); d.away = away
        if accepted: d.accept_handoff(d.backup, now, now+100)
        valid_action = "pickup" if sector == "school" else "charge"
        valid_resource = "DEMO-CHILD" if sector == "school" else "DEMO-SUB"
        d.grants.append(Grant("DEMO-A", valid_action, valid_resource,
                              now if expired else now+100, revoked))
        subject = "DEMO-B" if wrong_person else "DEMO-A"
        resource = "OTHER" if wrong_resource else valid_resource
        action = "OTHER" if wrong_action else valid_action
        result = d.attempt(subject, action, resource, now, ai_approval=True)
        # Expected labels come from injected fault flags, not authorized().
        permission_expected = not any((wrong_person, wrong_resource, wrong_action, expired, revoked))
        expected = permission_expected and (not away or accepted)
        counts["allowed" if result["allowed"] else "blocked"] += 1
        if result["allowed"] and not permission_expected:
            counts["unauthorized_allowed"] += 1
        decision = [e for e in d.events if e["kind"] == "action.checked"]
        if len(decision) != 1 or decision[0].get("resource") != resource:
            counts["missing_decision_evidence"] += 1
        if not result["allowed"]:
            incident = d.cases[result["case_id"]]
            if not incident["owner"]: counts["unassigned_cases"] += 1
        if result["allowed"] != expected:
            failures.append(dict(index=index, sector=sector, flags=flags, expected=expected, actual=result))
        sectors[sector]["trials"] += 1
        sectors[sector]["correct"] += int(result["allowed"] == expected)
    return dict(seed=seed, scope="synthetic model decision correctness only",
                exhaustive_combinations_per_sector=128, randomized_trials_per_sector=random_trials,
                sectors=sectors,
                total=len(cases), correct=len(cases)-len(failures), failures=failures,
                metrics=counts, field_reliability_estimate=None,
                field_trials_for_zero_failures_99pct_at_one_sided_95pct=math.ceil(math.log(.05)/math.log(.99)),
                statistical_note="299 independent representative zero-failure field trials would give a one-sided exact binomial lower bound above 99%, under fixed-process IID assumptions. These synthetic runs do not qualify.")


if __name__ == "__main__":
    result = evaluate()
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result["failures"] or result["metrics"]["unauthorized_allowed"] or
                          result["metrics"]["unassigned_cases"] or result["metrics"]["missing_decision_evidence"]))
