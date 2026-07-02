from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def test_m4_token_cannot_override_secret_access() -> None:
    agent = GovernedAgent(root_path=".")
    prepared = agent.prepare_request("Read .env")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"],
        reviewer_id="reviewer-2",
        reviewer_role="security_reviewer",
        approval_scope="DATA_EXPORT",
    )

    result = agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    assert result["envelope"]["decision"] == "DENY"
    assert result["envelope"]["execution_status"] == "NOT_EXECUTED"
    assert result["tool_result"]["tool_executed"] is False
    assert result["receipt"]["approval_valid"] is False
