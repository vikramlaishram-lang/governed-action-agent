from __future__ import annotations

from gcr.report_generator import generate_report_summary
from gcr_agent import GovernedAgent


def test_m10_report_includes_integrity_status(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=".", ledger_path=ledger_path).handle_request("Read README.md")
    ledger = generate_report_summary(ledger_path=ledger_path)["ledger"]

    assert ledger["valid"] is True
    assert ledger["record_count"] == 1
    assert ledger["latest_hash_present"] is True
