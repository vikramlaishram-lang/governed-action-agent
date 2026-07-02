from __future__ import annotations

from gcr.replay_verifier import verify_ledger
from gcr_agent.cli import main


def test_m7_cli_ask_safe_read(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("# Temp Repo\n", encoding="utf-8")
    assert main(["init"]) == 0
    capsys.readouterr()

    assert main(["ask", "Read README.md"]) == 0
    output = capsys.readouterr().out

    assert "DECISION: ALLOW" in output
    assert "CONSEQUENCE: READ_ONLY_ACCESS" in output
    assert "EXECUTION_STATUS: EXECUTED" in output
    assert "LEDGER_APPENDED: true" in output
    assert verify_ledger(tmp_path / ".governed-agent" / "ledger.jsonl")["record_count"] == 1
