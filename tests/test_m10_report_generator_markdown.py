from __future__ import annotations

from gcr.report_generator import generate_markdown_report, generate_report_summary
from gcr_agent import GovernedAgent


def test_m10_report_generator_markdown(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=".", ledger_path=ledger_path).handle_request("Read README.md")
    markdown = generate_markdown_report(generate_report_summary(ledger_path=ledger_path))

    for section in [
        "# Governed Action Agent Report",
        "## Project Summary",
        "## Ledger Integrity",
        "## Decision Summary",
        "## Violations",
        "## Review-Approved Actions",
        "## Denied Actions",
        "## Request-Review Actions",
        "## GitHub PR Evidence",
        "## Public Claims Allowed by Evidence",
        "## Limitations / Non-Claims",
    ]:
        assert section in markdown
