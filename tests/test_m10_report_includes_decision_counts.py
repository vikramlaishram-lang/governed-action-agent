from __future__ import annotations

from gcr.report_generator import generate_report_summary
from gcr_agent import GovernedAgent


def test_m10_report_includes_decision_counts(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    agent = GovernedAgent(root_path=".", ledger_path=ledger_path)
    agent.handle_request("Read README.md")
    agent.handle_request("Read .env")
    agent.handle_request("Deploy payment-service to production")
    decisions = generate_report_summary(ledger_path=ledger_path)["decisions"]

    assert decisions["ALLOW"] == 1
    assert decisions["DENY"] == 1
    assert decisions["REQUEST_REVIEW"] == 1
    assert decisions["BLOCKED"] == 0
