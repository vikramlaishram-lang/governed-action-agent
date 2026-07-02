from __future__ import annotations


def label_output_mode(user_request: str) -> tuple[str, str, bool]:
    lowered = user_request.lower()
    execution_authority_claimed = "approve yourself" in lowered or "self-authorize" in lowered

    if execution_authority_claimed:
        return "ACTION_PROPOSAL", "Adversarial self-approval language preserved for verifier detection", True
    if "deploy" in lowered and "production" in lowered:
        return "REVIEW_REQUEST", "Production deployment requires human review", False
    if any(term in lowered for term in ("read readme.md", ".env", "read", "list files", "git diff", "run tests")):
        return "ACTION_PROPOSAL", "User requested a bounded action proposal", False
    return "PLAN", "No directly executable action was confidently identified", False
