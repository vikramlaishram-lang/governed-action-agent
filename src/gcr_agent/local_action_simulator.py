from __future__ import annotations


def simulate_local_action(decision: str, constitutional_errors: list[str]) -> dict:
    if "CONSTITUTIONAL_VIOLATION" in constitutional_errors:
        return {"execution_status": "NOT_EXECUTED", "outcome_status": "BLOCKED"}
    if decision == "ALLOW":
        return {"execution_status": "EXECUTED", "outcome_status": "SUCCESS"}
    if decision == "DENY":
        return {"execution_status": "NOT_EXECUTED", "outcome_status": "BLOCKED"}
    if decision == "REQUEST_REVIEW":
        return {"execution_status": "NOT_EXECUTED", "outcome_status": "PENDING_REVIEW"}
    return {"execution_status": "NOT_EXECUTED", "outcome_status": "BLOCKED"}
