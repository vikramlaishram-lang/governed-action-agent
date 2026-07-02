from __future__ import annotations

from gcr.replay_verifier import verify_ledger
from gcr_agent import GovernedAgent


def test_m6_unkeyed_mode_still_verifies(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=".", ledger_path=ledger_path).handle_request("Read README.md")

    summary = verify_ledger(ledger_path)

    assert summary["valid"] is True
    assert summary["unkeyed_record_count"] == 1
    assert summary["hmac_record_count"] == 0
