from __future__ import annotations

from gcr.report_generator import generate_markdown_report, generate_report_summary
from gcr_agent import GovernedAgent


def test_m11_report_includes_code_change_proposal(tmp_path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=tmp_path, ledger_path=ledger_path).propose_code_change(
        "Update README.md with governed agent summary"
    )
    summary = generate_report_summary(ledger_path=ledger_path)
    markdown = generate_markdown_report(summary)

    assert summary["code_change_proposals"]
    assert summary["code_change_proposals"][0]["applied_to_real_repo"] is False
    assert "## Code Change Proposals" in markdown
    assert "sandboxed code-change proposal records" in " ".join(summary["public_claims_allowed"])
