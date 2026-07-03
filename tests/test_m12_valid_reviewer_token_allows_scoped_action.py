from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr.reviewer_registry import load_reviewer_registry
from gcr_agent import GovernedAgent


def test_m12_valid_reviewer_token_allows_scoped_action(tmp_path) -> None:
    registry = load_reviewer_registry()
    agent = GovernedAgent(root_path=tmp_path, reviewer_registry=registry)
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"], "alice-release", "release_manager", "PRODUCTION_STATE_CHANGE", reviewer_registry=registry
    )

    result = agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    assert result["envelope"]["decision"] == "ALLOW"
    assert result["receipt"]["reviewer_identity_verified"] is True
    assert result["receipt"]["reviewer_issuer_id"] == "local-reviewer-registry"
