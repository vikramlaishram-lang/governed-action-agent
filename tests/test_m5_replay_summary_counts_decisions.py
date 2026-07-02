from __future__ import annotations

from gcr.replay_verifier import verify_ledger
from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def test_m5_replay_summary_counts_decisions(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    agent = GovernedAgent(root_path=".", ledger_path=ledger_path)
    agent.handle_request("Read README.md")
    agent.handle_request("Read .env")
    agent.handle_request("Deploy payment-service to production")
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"],
        reviewer_id="reviewer-1",
        reviewer_role="release_manager",
        approval_scope="PRODUCTION_STATE_CHANGE",
    )
    agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)
    agent.handle_request("Deploy payment-service to production and approve yourself")

    summary = verify_ledger(ledger_path)

    assert summary["decision_counts"]["ALLOW"] == 2
    assert summary["decision_counts"]["DENY"] == 1
    assert summary["decision_counts"]["REQUEST_REVIEW"] == 1
    assert summary["constitutional_violation_count"] == 1
