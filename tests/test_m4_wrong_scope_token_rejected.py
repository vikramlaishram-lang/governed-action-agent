from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def test_m4_wrong_scope_token_rejected() -> None:
    agent = GovernedAgent(root_path=".")
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"],
        reviewer_id="reviewer-1",
        reviewer_role="release_manager",
        approval_scope="CODE_CHANGE",
    )

    result = agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    assert result["envelope"]["decision"] == "REQUEST_REVIEW"
    assert "REVIEW_TOKEN_SCOPE_MISMATCH" in result["envelope"]["approval_errors"]
