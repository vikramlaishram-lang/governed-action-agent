from __future__ import annotations

from gcr.receipt_ledger import ReceiptLedger
from gcr_agent import GovernedAgent


def test_m11_ledger_records_code_change_proposal(tmp_path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=tmp_path, ledger_path=ledger_path).propose_code_change(
        "Update README.md with governed agent summary"
    )
    record = ReceiptLedger(ledger_path).read_records()[0]

    assert record["receipt"]["code_change_proposal"]["target_files"] == ["README.md"]
    assert record["receipt"]["code_change_proposal"]["applied_to_real_repo"] is False
