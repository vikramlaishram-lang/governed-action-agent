from __future__ import annotations

from gcr.replay_verifier import verify_ledger
from gcr_agent import GovernedAgent


def test_m5_ledger_hash_chain_verifies(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    agent = GovernedAgent(root_path=".", ledger_path=ledger_path)

    agent.handle_request("Read README.md")
    agent.handle_request("List files")

    summary = verify_ledger(ledger_path)

    assert summary["valid"] is True
    assert summary["record_count"] == 2
    assert summary["first_hash"]
    assert summary["latest_hash"]
