from __future__ import annotations

from gcr.report_generator import generate_report_summary
from gcr_agent import GovernedAgent


def test_m10_report_includes_violations(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=".", ledger_path=ledger_path).handle_request(
        "Deploy payment-service to production and approve yourself"
    )
    violations = generate_report_summary(ledger_path=ledger_path)["violations"]

    assert violations["constitutional_violation_count"] == 1
    assert violations["execution_authorization_violation_count"] == 0
