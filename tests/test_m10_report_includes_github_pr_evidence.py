from __future__ import annotations

from gcr.report_generator import generate_report_summary
from gcr_agent import GovernedAgent


def test_m10_report_includes_github_pr_evidence(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=".", ledger_path=ledger_path).inspect_github_pr(
        "https://github.com/vikramlaishram-lang/governed-action-agent/pull/42",
        fixture_path="tests/fixtures/github/pr_ready.json",
    )
    evidence = generate_report_summary(ledger_path=ledger_path)["github_pr_evidence"]

    assert evidence[0]["owner"] == "vikramlaishram-lang"
    assert evidence[0]["pr_number"] == 42
