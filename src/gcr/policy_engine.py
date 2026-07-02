from __future__ import annotations

import hashlib


POLICY_VERSION = "local_policy_v0.1"
DECISION_ENGINE_VERSION = "policy_engine_v0.1"

POLICY_RULES = {
    "READ_ONLY_ACCESS": "ALLOW",
    "LOCAL_COMPUTATION": "ALLOW",
    "TEXT_GENERATION": "ALLOW",
    "SECRET_ACCESS": "DENY",
    "PRODUCTION_STATE_CHANGE": "REQUEST_REVIEW",
    "WORKFLOW_CHANGE": "REQUEST_REVIEW",
    "IRREVERSIBLE_DELETE": "DENY",
    "UNKNOWN": "REQUEST_REVIEW",
}


def policy_hash() -> str:
    policy_material = "|".join(f"{key}:{value}" for key, value in sorted(POLICY_RULES.items()))
    return hashlib.sha256(policy_material.encode("utf-8")).hexdigest()


def apply_policy(proposal: dict) -> dict:
    if proposal["execution_authority_claimed"] is True:
        return {
            "decision": "DENY",
            "decision_basis": "constitutional_invariant",
            "decision_reason": "CONSTITUTIONAL_VIOLATION: agent output claimed execution authority",
            "review_status": "NOT_REQUESTED",
        }

    consequence = proposal["consequence_class"]
    decision = POLICY_RULES.get(consequence, "REQUEST_REVIEW")
    reasons = {
        "ALLOW": "Policy permits simulated low-risk local action",
        "DENY": "Policy denies this consequence class",
        "REQUEST_REVIEW": "Policy requires human review before execution",
    }
    review_status = "REQUESTED" if decision == "REQUEST_REVIEW" else "NOT_REQUESTED"
    return {
        "decision": decision,
        "decision_basis": f"{POLICY_VERSION}:{consequence}",
        "decision_reason": reasons[decision],
        "review_status": review_status,
    }
