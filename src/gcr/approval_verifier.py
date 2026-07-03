from __future__ import annotations

from datetime import UTC, datetime

from .policy_loader import get_policy_rule
from .review_token import ReviewToken
from .reviewer_registry import ReviewerAuthorityRegistry


NEVER_APPROVABLE = {"SECRET_ACCESS", "IRREVERSIBLE_DELETE"}


def verify_review_token(
    *,
    proposal: dict,
    review_token: dict | ReviewToken | None,
    policy: dict,
    now: datetime | None = None,
    reviewer_registry: ReviewerAuthorityRegistry | dict | None = None,
) -> tuple[bool, list[str]]:
    rule = get_policy_rule(policy, proposal["consequence_class"])
    errors: list[str] = []

    if proposal.get("execution_authority_claimed") is True:
        return False, ["CONSTITUTIONAL_VIOLATION_NOT_OVERRIDABLE"]

    if proposal["consequence_class"] in NEVER_APPROVABLE:
        return False, [f"{proposal['consequence_class']}_NOT_OVERRIDABLE"]

    if not rule.get("review_can_override", False):
        errors.append("REVIEW_NOT_OVERRIDABLE")

    if review_token is None:
        errors.append("REVIEW_TOKEN_MISSING")
        return False, errors

    token = review_token.to_dict() if isinstance(review_token, ReviewToken) else dict(review_token)
    current_time = now or datetime.now(UTC)

    registry = ReviewerAuthorityRegistry(reviewer_registry) if isinstance(reviewer_registry, dict) else reviewer_registry
    if registry is None:
        if token.get("schema_version") not in {"review_token_v0.1", "review_token_v0.2"}:
            errors.append("REVIEW_TOKEN_SCHEMA_INVALID")
    else:
        if token.get("schema_version") != "review_token_v0.2":
            errors.append("REVIEW_TOKEN_VERSION_UNHARDENED")
    if token.get("approval_status") != "APPROVED":
        errors.append("REVIEW_TOKEN_NOT_APPROVED")
    if token.get("proposal_id") != proposal["proposal_id"]:
        errors.append("REVIEW_TOKEN_PROPOSAL_MISMATCH")
    if token.get("approved_normalized_action") != proposal["normalized_action"]:
        errors.append("REVIEW_TOKEN_ACTION_MISMATCH")
    if token.get("approved_consequence_class") != proposal["consequence_class"]:
        errors.append("REVIEW_TOKEN_CONSEQUENCE_MISMATCH")
    if token.get("approval_scope") != proposal["consequence_class"]:
        errors.append("REVIEW_TOKEN_SCOPE_MISMATCH")

    expires_at = _parse_iso_datetime(token.get("expires_at"))
    if expires_at is None or expires_at <= current_time:
        errors.append("REVIEW_TOKEN_EXPIRED")

    allowed_roles = rule.get("allowed_reviewer_roles", [])
    if token.get("reviewer_role") not in allowed_roles:
        errors.append("REVIEWER_ROLE_NOT_ALLOWED")

    if registry is not None:
        reviewer = registry.get_reviewer(token.get("reviewer_id"))
        if reviewer is None:
            errors.append("REVIEWER_UNKNOWN")
        else:
            if reviewer.get("status") != "ACTIVE":
                errors.append("REVIEWER_NOT_ACTIVE")
            if not registry.reviewer_has_role(token.get("reviewer_id"), token.get("reviewer_role")):
                errors.append("REVIEWER_ROLE_NOT_AUTHORIZED")
            if not registry.reviewer_has_scope(token.get("reviewer_id"), token.get("approval_scope")):
                errors.append("REVIEWER_SCOPE_NOT_AUTHORIZED")
            if not registry.verify_identity_hash(token.get("reviewer_id"), token.get("reviewer_identity_hash")):
                errors.append("REVIEWER_IDENTITY_HASH_MISMATCH")
        if token.get("issuer_id") != registry.issuer_id:
            errors.append("REVIEWER_ISSUER_MISMATCH")

    return len(errors) == 0, errors


def _parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)
