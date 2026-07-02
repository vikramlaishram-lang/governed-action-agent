from __future__ import annotations

from gcr_agent.cli import main


def test_m7_cli_status(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    assert main(["status"]) == 0
    assert capsys.readouterr().out.strip() == "GAA_STATUS: NOT_INITIALIZED"

    assert main(["init"]) == 0
    capsys.readouterr()
    assert main(["status"]) == 0
    output = capsys.readouterr().out

    assert "GAA_STATUS: INITIALIZED" in output
    assert "CONFIG_EXISTS: true" in output
    assert "POLICY_EXISTS: true" in output
    assert "LEDGER_EXISTS: true" in output
    assert "AUTH_MODE: UNKEYED_HASH_CHAIN" in output
