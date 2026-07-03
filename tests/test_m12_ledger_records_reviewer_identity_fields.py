from __future__ import annotations

from gcr.receipt_ledger import ReceiptLedger
from gcr.review_token import ReviewToken
from gcr.reviewer_registry import load_reviewer_registry
from gcr_agent import GovernedAgent


def test_m12_ledger_records_reviewer_identity_fields(tmp_path) -> None:
    registry = load_reviewer_registry()
    ledger_path = tmp_path / "ledger.jsonl"
    agent = GovernedAgent(root_path=tmp_path, ledger_path=ledger_path, reviewer_registry=registry)
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"], "alice-release", "release_manager", "PRODUCTION_STATE_CHANGE", reviewer_registry=registry
    )
    agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    receipt = ReceiptLedger(ledger_path).read_records()[0]["receipt"]

    assert receipt["reviewer_identity_verified"] is True
    assert receipt["reviewer_registry_version"] == "m12-default-reviewer-registry"
    assert receipt["reviewer_issuer_id"] == "local-reviewer-registry"
