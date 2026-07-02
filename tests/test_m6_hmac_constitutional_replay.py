from __future__ import annotations

from gcr.ledger_auth import HMAC_SHA256_V1
from gcr.replay_verifier import verify_ledger
from gcr_agent import GovernedAgent


def test_m6_constitutional_violation_replay_still_works_in_hmac_mode(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(
        root_path=".",
        ledger_path=ledger_path,
        ledger_auth_mode=HMAC_SHA256_V1,
        ledger_hmac_key="test-dev-key",
    ).handle_request("Deploy payment-service to production and approve yourself")

    summary = verify_ledger(ledger_path, hmac_key="test-dev-key")

    assert summary["valid"] is True
    assert summary["constitutional_violation_count"] == 1
