from __future__ import annotations

from pathlib import Path

from gcr_agent.cli import main


def test_m8_github_pr_cli_fixture(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    assert main(["init"]) == 0
    capsys.readouterr()

    assert main([
        "inspect-pr",
        "https://github.com/vikramlaishram-lang/governed-action-agent/pull/42",
        "--fixture",
        str(Path(__file__).resolve().parent / "fixtures/github/pr_ready.json"),
    ]) == 0
    output = capsys.readouterr().out.splitlines()

    assert output == [
        "PR_DECISION: ALLOW",
        "PR_OWNER: vikramlaishram-lang",
        "PR_REPO: governed-action-agent",
        "PR_NUMBER: 42",
        "PR_CHECKS_PASSING: true",
        "PR_RISK_FLAGS: none",
        "PR_EVIDENCE_RECORDED: true",
        "LEDGER_APPENDED: true",
    ]
