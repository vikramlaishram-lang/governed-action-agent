from __future__ import annotations

import json

import pytest

from gcr_agent.cli import main


def test_m7_cli_init_creates_project_config(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["init"]) == 0
    output = capsys.readouterr().out.splitlines()

    assert output == [
        "GAA_INIT: OK",
        "CONFIG_PATH: .governed-agent/config.json",
        "POLICY_PATH: .governed-agent/policy.json",
        "LEDGER_PATH: .governed-agent/ledger.jsonl",
        "AUTH_MODE: UNKEYED_HASH_CHAIN",
    ]
    assert (tmp_path / ".governed-agent" / "config.json").exists()
    assert (tmp_path / ".governed-agent" / "policy.json").exists()
    assert (tmp_path / ".governed-agent" / "ledger.jsonl").exists()


def test_m7_cli_init_does_not_overwrite_existing_config(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert main(["init"]) == 0
    config_path = tmp_path / ".governed-agent" / "config.json"
    original = json.loads(config_path.read_text(encoding="utf-8"))

    assert main(["init"]) == 1

    assert json.loads(config_path.read_text(encoding="utf-8")) == original
