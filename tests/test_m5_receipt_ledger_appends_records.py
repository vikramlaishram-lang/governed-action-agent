from __future__ import annotations

from gcr.receipt_ledger import ReceiptLedger
from gcr_agent import GovernedAgent


def test_m5_receipt_ledger_appends_records(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    agent = GovernedAgent(root_path=".", ledger_path=ledger_path)

    first = agent.handle_request("Read README.md")["ledger_record"]
    second = agent.handle_request("List files")["ledger_record"]
    records = ReceiptLedger(ledger_path).read_records()

    assert len(records) == 2
    assert first["sequence_number"] == 1
    assert first["previous_record_hash"] == "GENESIS"
    assert second["sequence_number"] == 2
    assert second["previous_record_hash"] == first["record_hash"]
