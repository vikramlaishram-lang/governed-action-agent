from __future__ import annotations

from gcr_agent import GovernedAgent
from gcr_agent.github_pr_reader import GitHubPRReader


def test_m8_github_pr_sensitive_files_flagged() -> None:
    snapshot = GitHubPRReader().from_fixture("tests/fixtures/github/pr_sensitive_files.json")

    assert "SENSITIVE_FILE_TOUCHED" in snapshot["risk_flags"]


def test_m8_sensitive_files_create_evidence_gap() -> None:
    result = GovernedAgent(root_path=".").inspect_github_pr(
        "https://github.com/vikramlaishram-lang/governed-action-agent/pull/44",
        fixture_path="tests/fixtures/github/pr_sensitive_files.json",
    )

    assert "sensitive_file_review" in result["proposal"]["evidence_gaps"]
    assert result["receipt"]["github_pr"]["risk_flags"] == ["SENSITIVE_FILE_TOUCHED"]
