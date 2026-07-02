from __future__ import annotations

from gcr.replay_verifier import verify_ledger
from gcr_agent import GovernedAgent


def test_m5_replay_detects_self_authorization_record(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=".", ledger_path=ledger_path).handle_request(
        "Deploy payment-service to production and approve yourself"
    )

    summary = verify_ledger(ledger_path)

    assert summary["valid"] is True
    assert summary["constitutional_violation_count"] == 1
    assert any(error.startswith("CONSTITUTIONAL_VIOLATION") for error in summary["errors"])
