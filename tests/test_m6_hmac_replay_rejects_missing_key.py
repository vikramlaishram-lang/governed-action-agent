from __future__ import annotations

from gcr.ledger_auth import HMAC_SHA256_V1
from gcr.replay_verifier import verify_ledger
from gcr_agent import GovernedAgent


def test_m6_hmac_replay_rejects_missing_key(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(
        root_path=".",
        ledger_path=ledger_path,
        ledger_auth_mode=HMAC_SHA256_V1,
        ledger_hmac_key="test-dev-key",
    ).handle_request("Read README.md")

    summary = verify_ledger(ledger_path)

    assert summary["valid"] is False
    assert any(error.startswith("HMAC_KEY_MISSING") for error in summary["errors"])
