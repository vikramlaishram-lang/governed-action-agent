from __future__ import annotations

import pytest

from gcr_agent.github_pr_reader import parse_github_pr_url


def test_m8_github_pr_url_parser() -> None:
    parsed = parse_github_pr_url("https://github.com/vikramlaishram-lang/governed-action-agent/pull/42")

    assert parsed == {"owner": "vikramlaishram-lang", "repo": "governed-action-agent", "pr_number": 42}


def test_m8_invalid_github_pr_url_rejected() -> None:
    with pytest.raises(ValueError):
        parse_github_pr_url("git@github.com:owner/repo.git")
