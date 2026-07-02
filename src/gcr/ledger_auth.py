from __future__ import annotations

import copy
import hashlib
import hmac
import json
import os


UNKEYED_HASH_CHAIN = "UNKEYED_HASH_CHAIN"
HMAC_SHA256_V1 = "HMAC_SHA256_V1"


def canonical_json(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sha256_record(payload: dict) -> str:
    return f"sha256:{hashlib.sha256(canonical_json(payload)).hexdigest()}"


def compute_record_hash(record: dict) -> str:
    hashable = copy.deepcopy(record)
    hashable["record_hash"] = ""
    hashable["record_mac"] = None
    return sha256_record(hashable)


def compute_record_mac(record: dict, key: str) -> str:
    mac_payload = copy.deepcopy(record)
    mac_payload["record_mac"] = None
    digest = hmac.new(key.encode("utf-8"), canonical_json(mac_payload), hashlib.sha256).hexdigest()
    return f"hmac-sha256:{digest}"


def verify_record_mac(record: dict, key: str) -> bool:
    expected = compute_record_mac(record, key)
    actual = record.get("record_mac")
    return isinstance(actual, str) and hmac.compare_digest(expected, actual)


def resolve_auth_config(
    *,
    auth_mode: str | None = None,
    hmac_key: str | None = None,
    key_id: str | None = None,
) -> dict:
    mode = auth_mode or os.environ.get("GAA_LEDGER_AUTH_MODE", UNKEYED_HASH_CHAIN)
    runtime_mode = os.environ.get("GAA_RUNTIME_MODE", "local")
    if mode not in {UNKEYED_HASH_CHAIN, HMAC_SHA256_V1}:
        raise ValueError(f"Unsupported ledger auth mode: {mode}")
    if runtime_mode == "production" and mode == UNKEYED_HASH_CHAIN:
        raise ValueError("UNKEYED_HASH_CHAIN is not allowed in production runtime mode")

    resolved_key = hmac_key or os.environ.get("GAA_LEDGER_HMAC_KEY")
    resolved_key_id = key_id or os.environ.get("GAA_LEDGER_HMAC_KEY_ID", "local-dev-key")
    if mode == HMAC_SHA256_V1 and not resolved_key:
        raise ValueError("HMAC_SHA256_V1 requires an HMAC key")

    return {
        "tamper_evidence_mode": mode,
        "ledger_auth_version": "HMAC_SHA256_V1" if mode == HMAC_SHA256_V1 else "UNKEYED_HASH_CHAIN_V1",
        "hmac_key": resolved_key if mode == HMAC_SHA256_V1 else None,
        "key_id": resolved_key_id if mode == HMAC_SHA256_V1 else None,
    }
