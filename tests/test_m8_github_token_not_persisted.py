from __future__ import annotations

import json

from gcr_agent import GovernedAgent


def test_m8_github_token_not_persisted(tmp_path) -> None:
    token = "ghp_do_not_persist"
    ledger_path = tmp_path / "ledger.jsonl"
    result = GovernedAgent(root_path=".", ledger_path=ledger_path).inspect_github_pr(
        "https://github.com/vikramlaishram-lang/governed-action-agent/pull/42",
        fixture_path="tests/fixtures/github/pr_ready.json",
        github_token=token,
    )
    serialized = json.dumps(result, sort_keys=True) + ledger_path.read_text(encoding="utf-8")

    assert token not in serialized
    assert "patch" not in serialized
    assert "do not persist this patch" not in serialized
