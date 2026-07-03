from __future__ import annotations

from gcr.replay_verifier import verify_ledger
from gcr_agent import GovernedAgent


def test_m8_github_ledger_replay(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=".", ledger_path=ledger_path).inspect_github_pr(
        "https://github.com/vikramlaishram-lang/governed-action-agent/pull/42",
        fixture_path="tests/fixtures/github/pr_ready.json",
    )

    summary = verify_ledger(ledger_path)

    assert summary["valid"] is True
    assert summary["record_count"] == 1
    assert summary["decision_counts"]["ALLOW"] == 1
