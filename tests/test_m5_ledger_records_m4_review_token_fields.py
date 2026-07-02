from __future__ import annotations

from gcr.receipt_ledger import ReceiptLedger
from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def test_m5_ledger_records_m4_review_token_fields(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    agent = GovernedAgent(root_path=".", ledger_path=ledger_path)
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"],
        reviewer_id="reviewer-1",
        reviewer_role="release_manager",
        approval_scope="PRODUCTION_STATE_CHANGE",
    )
    agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)
    record = ReceiptLedger(ledger_path).read_records()[0]

    assert record["receipt"]["approval_valid"] is True
    assert record["receipt"]["reviewer_role"] == "release_manager"
    assert record["receipt"]["approval_token_id"] == token.token_id
    assert record["envelope"]["approval_scope"] == "PRODUCTION_STATE_CHANGE"
