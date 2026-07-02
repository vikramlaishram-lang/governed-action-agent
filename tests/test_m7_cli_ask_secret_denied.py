from __future__ import annotations

from gcr_agent.cli import main


def test_m7_cli_ask_secret_denied(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("# Temp Repo\n", encoding="utf-8")
    assert main(["init"]) == 0
    capsys.readouterr()

    assert main(["ask", "Read .env"]) == 0
    output = capsys.readouterr().out

    assert "DECISION: DENY" in output
    assert "CONSEQUENCE: SECRET_ACCESS" in output
    assert "LEDGER_APPENDED: true" in output
