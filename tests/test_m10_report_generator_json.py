from __future__ import annotations

from gcr.report_generator import generate_report_summary
from gcr_agent import GovernedAgent


def test_m10_report_generator_json(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=".", ledger_path=ledger_path).handle_request("Read README.md")
    summary = generate_report_summary(ledger_path=ledger_path)

    assert set(summary) >= {
        "schema_version",
        "generated_at",
        "project",
        "ledger",
        "decisions",
        "violations",
        "review",
        "actions",
        "github_pr_evidence",
        "public_claims_allowed",
        "limitations",
    }
