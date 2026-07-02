from __future__ import annotations

from gcr.receipt_ledger import ReceiptLedger
from gcr_agent import GovernedAgent


def test_m5_agent_writes_receipts_to_ledger(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    result = GovernedAgent(root_path=".", ledger_path=ledger_path).handle_request("Read README.md")

    assert "ledger_record" in result
    assert ledger_path.exists()
    assert ReceiptLedger(ledger_path).read_records()[0]["receipt"]["receipt_id"] == result["receipt"]["receipt_id"]


def test_m5_agent_without_ledger_path_is_unchanged() -> None:
    result = GovernedAgent(root_path=".").handle_request("Read README.md")

    assert "ledger_record" not in result
    assert result["envelope"]["decision"] == "ALLOW"
