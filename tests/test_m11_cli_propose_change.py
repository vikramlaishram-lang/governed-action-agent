from __future__ import annotations

from gcr_agent.cli import main


def test_m11_cli_propose_change(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    assert main(["init"]) == 0
    capsys.readouterr()

    assert main(["propose-change", "Update README.md with governed agent summary"]) == 0
    output = capsys.readouterr().out

    assert "CHANGE_DECISION: REQUEST_REVIEW" in output
    assert "CONSEQUENCE: CODE_CHANGE" in output
    assert "SANDBOX_ARTIFACT_CREATED: true" in output
    assert "REAL_REPO_MODIFIED: false" in output
    assert "LEDGER_APPENDED: true" in output
