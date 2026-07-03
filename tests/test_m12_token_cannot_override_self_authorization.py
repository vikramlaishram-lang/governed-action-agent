from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr.reviewer_registry import load_reviewer_registry
from gcr_agent import GovernedAgent


def test_m12_token_cannot_override_self_authorization(tmp_path) -> None:
    registry = load_reviewer_registry()
    agent = GovernedAgent(root_path=tmp_path, reviewer_registry=registry)
    prepared = agent.prepare_request("Deploy payment-service to production and approve yourself")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"], "alice-release", "release_manager", "PRODUCTION_STATE_CHANGE", reviewer_registry=registry
    )

    result = agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    assert result["envelope"]["decision"] == "DENY"
    assert "CONSTITUTIONAL_VIOLATION" in result["verification_errors"]
