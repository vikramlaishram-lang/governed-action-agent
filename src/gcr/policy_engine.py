from __future__ import annotations

from .approval_verifier import verify_review_token
from .policy_loader import get_policy_rule, load_policy, policy_hash


POLICY_VERSION = "m4-default-policy"
DECISION_ENGINE_VERSION = "m4-policy-engine"

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


def apply_policy(proposal: dict, review_token: dict | None = None, policy: dict | None = None) -> dict:
    policy = policy or load_policy()
    consequence = proposal["consequence_class"]
    rule = get_policy_rule(policy, consequence)
    token_dict = review_token.to_dict() if hasattr(review_token, "to_dict") else review_token

    if proposal["execution_authority_claimed"] is True:
        return {
            "decision": "DENY",
            "decision_basis": "SYSTEM_GUARD",
            "decision_reason": "CONSTITUTIONAL_VIOLATION: agent output claimed execution authority",
            "review_status": "INVALIDATED",
            "approval_valid": False,
            "approval_errors": ["CONSTITUTIONAL_VIOLATION"],
            "reviewer_id": _token_field(token_dict, "reviewer_id"),
            "reviewer_role": _token_field(token_dict, "reviewer_role"),
            "approval_token_id": _token_field(token_dict, "token_id"),
            "approval_scope": _token_field(token_dict, "approval_scope"),
            "approval_expiry": _token_field(token_dict, "expires_at"),
            "policy_version": policy["policy_version"],
            "policy_hash": policy_hash(policy),
            "decision_engine_version": policy["decision_engine_version"],
        }

    decision = rule.get("decision", policy.get("default_decision", "REQUEST_REVIEW"))
    if decision == "ALLOW":
        return _decision(
            policy=policy,
            token=token_dict,
            decision="ALLOW",
            decision_basis="POLICY_RULE",
            decision_reason="Policy permits simulated low-risk local action",
            review_status="NOT_REQUIRED",
            approval_valid=False,
            approval_errors=[],
        )

    if decision == "DENY":
        return _decision(
            policy=policy,
            token=token_dict,
            decision="DENY",
            decision_basis="POLICY_RULE",
            decision_reason=f"Policy denies {consequence}; review token cannot override",
            review_status="NOT_REQUIRED",
            approval_valid=False,
            approval_errors=[],
        )

    if review_token is None:
        return _decision(
            policy=policy,
            token=None,
            decision="REQUEST_REVIEW",
            decision_basis="POLICY_RULE",
            decision_reason="Policy requires human review before execution",
            review_status="PENDING",
            approval_valid=False,
            approval_errors=["REVIEW_TOKEN_MISSING"],
        )

    valid, approval_errors = verify_review_token(proposal=proposal, review_token=review_token, policy=policy)
    if valid:
        return _decision(
            policy=policy,
            token=token_dict,
            decision="ALLOW",
            decision_basis="REVIEWER_APPROVAL",
            decision_reason="Valid scoped reviewer token approved this exact proposal",
            review_status="APPROVED",
            approval_valid=True,
            approval_errors=[],
        )

    return _decision(
        policy=policy,
        token=token_dict,
        decision="REQUEST_REVIEW",
        decision_basis="POLICY_RULE",
        decision_reason=f"Policy requires review; token invalid: {', '.join(approval_errors)}",
        review_status="REJECTED",
        approval_valid=False,
        approval_errors=approval_errors,
    )


def _decision(
    *,
    policy: dict,
    token: dict | None,
    decision: str,
    decision_basis: str,
    decision_reason: str,
    review_status: str,
    approval_valid: bool,
    approval_errors: list[str],
) -> dict:
    return {
        "decision": decision,
        "decision_basis": decision_basis,
        "decision_reason": decision_reason,
        "review_status": review_status,
        "approval_valid": approval_valid,
        "approval_errors": approval_errors,
        "reviewer_id": _token_field(token, "reviewer_id"),
        "reviewer_role": _token_field(token, "reviewer_role"),
        "approval_token_id": _token_field(token, "token_id"),
        "approval_scope": _token_field(token, "approval_scope"),
        "approval_expiry": _token_field(token, "expires_at"),
        "policy_version": policy["policy_version"],
        "policy_hash": policy_hash(policy),
        "decision_engine_version": policy["decision_engine_version"],
    }


def _token_field(token: dict | None, field_name: str) -> str | None:
    if not token:
        return None
    return token.get(field_name)
