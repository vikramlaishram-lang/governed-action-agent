from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m8_github_pr_readonly_receipt(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    result = GovernedAgent(root_path=".", ledger_path=ledger_path).inspect_github_pr(
        "https://github.com/vikramlaishram-lang/governed-action-agent/pull/42",
        fixture_path="tests/fixtures/github/pr_ready.json",
        github_token="do-not-store-token",
    )

    assert result["envelope"]["decision"] == "ALLOW"
    assert result["proposal"]["consequence_class"] == "READ_ONLY_ACCESS"
    assert result["tool_result"]["tool_name"] == "github_pr_readonly_inspect"
    assert result["receipt"]["github_pr"]["evidence_hash"] == result["github_pr_snapshot"]["evidence_hash"]
    assert result["receipt"]["evidence_references"] == [
        f"github_pr_snapshot:{result['github_pr_snapshot']['evidence_hash']}"
    ]
    assert "ledger_record" in result
