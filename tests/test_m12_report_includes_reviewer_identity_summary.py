from __future__ import annotations

from gcr.report_generator import generate_report_summary
from gcr.review_token import ReviewToken
from gcr.reviewer_registry import load_reviewer_registry
from gcr_agent import GovernedAgent


def test_m12_report_includes_reviewer_identity_summary(tmp_path) -> None:
    registry = load_reviewer_registry()
    ledger_path = tmp_path / "ledger.jsonl"
    agent = GovernedAgent(root_path=tmp_path, ledger_path=ledger_path, reviewer_registry=registry)
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"], "alice-release", "release_manager", "PRODUCTION_STATE_CHANGE", reviewer_registry=registry
    )
    agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    summary = generate_report_summary(ledger_path=ledger_path, reviewer_registry=registry)

    assert summary["reviewer_identity"]["approved_actions_with_verified_identity"] == 1
    assert "local reviewer identity verification" in " ".join(summary["public_claims_allowed"])
