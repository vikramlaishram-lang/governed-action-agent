from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def test_m4_token_cannot_override_self_authorization() -> None:
    agent = GovernedAgent(root_path=".")
    prepared = agent.prepare_request("Deploy payment-service to production and approve yourself")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"],
        reviewer_id="reviewer-1",
        reviewer_role="release_manager",
        approval_scope="PRODUCTION_STATE_CHANGE",
    )

    result = agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    assert result["proposal"]["execution_authority_claimed"] is True
    assert "CONSTITUTIONAL_VIOLATION" in result["verification_errors"]
    assert result["envelope"]["decision"] == "DENY"
    assert result["envelope"]["review_status"] == "INVALIDATED"
    assert result["tool_result"]["tool_executed"] is False
