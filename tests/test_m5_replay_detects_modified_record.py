from __future__ import annotations

import json

from gcr.replay_verifier import verify_ledger
from gcr_agent import GovernedAgent


def test_m5_replay_detects_modified_record(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=".", ledger_path=ledger_path).handle_request("Read README.md")
    record = json.loads(ledger_path.read_text(encoding="utf-8").splitlines()[0])
    record["receipt"]["decision"] = "DENY"
    ledger_path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

    summary = verify_ledger(ledger_path)

    assert summary["valid"] is False
    assert any(error.startswith("RECORD_HASH_MISMATCH") for error in summary["errors"])
