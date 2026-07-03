from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr.reviewer_registry import load_reviewer_registry
from gcr_agent import GovernedAgent


def test_m12_wrong_reviewer_role_rejected(tmp_path) -> None:
    registry = load_reviewer_registry()
    agent = GovernedAgent(root_path=tmp_path, reviewer_registry=registry)
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"], "alice-release", "security_reviewer", "PRODUCTION_STATE_CHANGE", reviewer_registry=registry
    )

    result = agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    assert result["envelope"]["decision"] == "REQUEST_REVIEW"
    assert "REVIEWER_ROLE_NOT_AUTHORIZED" in result["envelope"]["approval_errors"]
