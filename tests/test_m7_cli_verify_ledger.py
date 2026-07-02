from __future__ import annotations

from gcr_agent.cli import main


def test_m7_cli_verify_ledger(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("# Temp Repo\n", encoding="utf-8")
    assert main(["init"]) == 0
    assert main(["ask", "Read README.md"]) == 0
    capsys.readouterr()

    assert main(["verify-ledger"]) == 0
    output = capsys.readouterr().out

    assert "LEDGER_VALID: true" in output
    assert "RECORD_COUNT: 1" in output
    assert "LATEST_HASH_PRESENT: true" in output
