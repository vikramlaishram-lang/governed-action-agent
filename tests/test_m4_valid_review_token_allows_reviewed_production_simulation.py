from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def test_m4_valid_review_token_allows_reviewed_production_simulation() -> None:
    agent = GovernedAgent(root_path=".")
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"],
        reviewer_id="reviewer-1",
        reviewer_role="release_manager",
        approval_scope="PRODUCTION_STATE_CHANGE",
    )

    result = agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    assert result["envelope"]["decision"] == "ALLOW"
    assert result["envelope"]["decision_basis"] == "REVIEWER_APPROVAL"
    assert result["envelope"]["review_status"] == "APPROVED"
    assert result["envelope"]["approval_valid"] is True
    assert result["envelope"]["execution_status"] == "EXECUTED"
    assert result["tool_result"]["tool_name"] == "deploy_simulated_review_approved"
    assert "no live deployment" in result["receipt"]["tool_result_summary"]
