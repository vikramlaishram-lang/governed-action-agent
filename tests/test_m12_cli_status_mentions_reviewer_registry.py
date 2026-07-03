from __future__ import annotations

from gcr_agent.cli import main


def test_m12_cli_status_mentions_reviewer_registry(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    assert main(["init"]) == 0
    capsys.readouterr()

    assert main(["status"]) == 0
    output = capsys.readouterr().out

    assert "REVIEWER_REGISTRY_EXISTS: true" in output
    assert main(["reviewers"]) == 0
    reviewers_output = capsys.readouterr().out
    assert "REVIEWER_REGISTRY: OK" in reviewers_output
    assert "REVIEWERS_ACTIVE: 2" in reviewers_output
