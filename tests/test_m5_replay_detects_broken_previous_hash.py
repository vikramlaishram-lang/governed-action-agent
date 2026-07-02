from __future__ import annotations

import json

from gcr.receipt_ledger import ledger_record_hash
from gcr.replay_verifier import verify_ledger
from gcr_agent import GovernedAgent


def test_m5_replay_detects_broken_previous_hash(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    agent = GovernedAgent(root_path=".", ledger_path=ledger_path)
    agent.handle_request("Read README.md")
    agent.handle_request("List files")
    records = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines()]
    records[1]["previous_record_hash"] = "sha256:wrong"
    records[1]["record_hash"] = ledger_record_hash(records[1])
    ledger_path.write_text("\n".join(json.dumps(record, sort_keys=True) for record in records) + "\n", encoding="utf-8")

    summary = verify_ledger(ledger_path)

    assert summary["valid"] is False
    assert any(error.startswith("PREVIOUS_HASH_MISMATCH") for error in summary["errors"])
