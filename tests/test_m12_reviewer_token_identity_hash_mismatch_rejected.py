from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr.reviewer_registry import load_reviewer_registry
from gcr_agent import GovernedAgent


def test_m12_reviewer_token_identity_hash_mismatch_rejected(tmp_path) -> None:
    registry = load_reviewer_registry()
    agent = GovernedAgent(root_path=tmp_path, reviewer_registry=registry)
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"], "alice-release", "release_manager", "PRODUCTION_STATE_CHANGE", reviewer_registry=registry
    ).to_dict()
    token["reviewer_identity_hash"] = "sha256:wrong"

    result = agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    assert result["envelope"]["decision"] == "REQUEST_REVIEW"
    assert "REVIEWER_IDENTITY_HASH_MISMATCH" in result["envelope"]["approval_errors"]
