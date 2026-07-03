from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr.reviewer_registry import load_reviewer_registry
from gcr_agent import GovernedAgent


def test_m12_wrong_reviewer_scope_rejected(tmp_path) -> None:
    registry = load_reviewer_registry()
    agent = GovernedAgent(root_path=tmp_path, reviewer_registry=registry)
    prepared = agent.prepare_request("Update README.md with governed agent summary")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"], "sam-security", "security_reviewer", "CODE_CHANGE", reviewer_registry=registry
    )

    result = agent.propose_code_change("Update README.md with governed agent summary", review_token=token, prepared=prepared)

    assert result["envelope"]["decision"] == "REQUEST_REVIEW"
    assert "REVIEWER_SCOPE_NOT_AUTHORIZED" in result["envelope"]["approval_errors"]
