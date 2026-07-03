from __future__ import annotations

from gcr.report_generator import generate_report_summary
from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def test_m10_report_includes_review_approved_actions(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    agent = GovernedAgent(root_path=".", ledger_path=ledger_path)
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"], "reviewer-1", "release_manager", "PRODUCTION_STATE_CHANGE"
    )
    agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)
    review = generate_report_summary(ledger_path=ledger_path)["review"]

    assert review["review_approved_count"] == 1
    assert review["review_approved_actions"][0]["reviewer_role"] == "release_manager"
