from __future__ import annotations

import json

from gcr.ledger_auth import HMAC_SHA256_V1, compute_record_hash
from gcr.replay_verifier import verify_ledger
from gcr_agent import GovernedAgent


def test_m6_hmac_detects_recomputed_hash_attack(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(
        root_path=".",
        ledger_path=ledger_path,
        ledger_auth_mode=HMAC_SHA256_V1,
        ledger_hmac_key="test-dev-key",
    ).handle_request("Read README.md")
    record = json.loads(ledger_path.read_text(encoding="utf-8").splitlines()[0])
    record["receipt"]["decision"] = "DENY"
    record["record_hash"] = compute_record_hash(record)
    ledger_path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

    summary = verify_ledger(ledger_path, hmac_key="test-dev-key")

    assert summary["valid"] is False
    assert any(error.startswith("HMAC_RECORD_MAC_MISMATCH") for error in summary["errors"])
