from __future__ import annotations

from gcr_agent.github_pr_reader import GitHubPRReader


def test_m8_github_pr_failing_checks_evidence() -> None:
    snapshot = GitHubPRReader().from_fixture("tests/fixtures/github/pr_failing_checks.json")

    assert snapshot["checks_passing"] is False
    assert "CHECKS_NOT_PASSING" in snapshot["risk_flags"]
