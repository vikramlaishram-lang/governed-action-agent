from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def test_m4_unauthorized_role_token_rejected() -> None:
    agent = GovernedAgent(root_path=".")
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"],
        reviewer_id="reviewer-1",
        reviewer_role="intern",
        approval_scope="PRODUCTION_STATE_CHANGE",
    )

    result = agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    assert result["envelope"]["decision"] == "REQUEST_REVIEW"
    assert "REVIEWER_ROLE_NOT_ALLOWED" in result["envelope"]["approval_errors"]
