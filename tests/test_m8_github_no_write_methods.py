from __future__ import annotations

from gcr_agent.github_pr_reader import GitHubPRReader


def test_m8_github_reader_exposes_no_write_methods() -> None:
    forbidden = {"merge", "comment", "approve", "update_status", "create_review", "dispatch_workflow"}
    exposed = {name for name in dir(GitHubPRReader) if not name.startswith("_")}

    assert forbidden.isdisjoint(exposed)
