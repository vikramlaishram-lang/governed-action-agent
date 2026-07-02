from __future__ import annotations

import pytest

from gcr.ledger_auth import resolve_auth_config


def test_m6_production_mode_requires_hmac(monkeypatch) -> None:
    monkeypatch.setenv("GAA_RUNTIME_MODE", "production")
    monkeypatch.delenv("GAA_LEDGER_AUTH_MODE", raising=False)

    with pytest.raises(ValueError, match="UNKEYED_HASH_CHAIN"):
        resolve_auth_config()


def test_m6_production_mode_accepts_hmac(monkeypatch) -> None:
    monkeypatch.setenv("GAA_RUNTIME_MODE", "production")
    config = resolve_auth_config(auth_mode="HMAC_SHA256_V1", hmac_key="dev-key", key_id="dev-key-id")

    assert config["tamper_evidence_mode"] == "HMAC_SHA256_V1"
