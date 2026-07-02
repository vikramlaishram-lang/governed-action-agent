from __future__ import annotations

import json

from gcr_agent.cli import main


def test_m7_cli_hmac_config_does_not_store_key_and_verifies(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GAA_LEDGER_HMAC_KEY", "m7-test-dev-key")
    (tmp_path / "README.md").write_text("# Temp Repo\n", encoding="utf-8")

    assert main(["init", "--hmac", "--key-id", "test-key"]) == 0
    capsys.readouterr()
    config_text = (tmp_path / ".governed-agent" / "config.json").read_text(encoding="utf-8")
    config = json.loads(config_text)

    assert config["ledger_auth_mode"] == "HMAC_SHA256_V1"
    assert config["ledger_key_id"] == "test-key"
    assert "m7-test-dev-key" not in config_text

    assert main(["ask", "Read README.md"]) == 0
    assert main(["verify-ledger"]) == 0
    assert "LEDGER_VALID: true" in capsys.readouterr().out


def test_m7_cli_hmac_ask_fails_without_key(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GAA_LEDGER_HMAC_KEY", raising=False)
    (tmp_path / "README.md").write_text("# Temp Repo\n", encoding="utf-8")

    assert main(["init", "--hmac", "--key-id", "test-key"]) == 0
    capsys.readouterr()

    assert main(["ask", "Read README.md"]) == 1
    assert capsys.readouterr().out.strip() == "GAA_ERROR: HMAC_KEY_MISSING"
