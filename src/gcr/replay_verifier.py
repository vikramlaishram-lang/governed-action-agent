from __future__ import annotations

import json
from pathlib import Path

from .ledger_auth import HMAC_SHA256_V1, UNKEYED_HASH_CHAIN, compute_record_hash, verify_record_mac
from .verify_envelope_chain import verify_constitutional_invariants


def replay_records(path: str | Path) -> list[dict]:
    ledger_path = Path(path)
    if not ledger_path.exists():
        return []
    records: list[dict] = []
    with ledger_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def verify_ledger(
    path: str | Path,
    *,
    hmac_key: str | None = None,
    expected_key_id: str | None = None,
    reviewer_registry=None,
) -> dict:
    ledger_path = Path(path)
    errors: list[str] = []
    integrity_errors: list[str] = []
    decision_counts: dict[str, int] = {}
    constitutional_violation_count = 0
    hmac_record_count = 0
    unkeyed_record_count = 0
    auth_modes_seen: list[str] = []
    records: list[dict] = []

    if not ledger_path.exists() or ledger_path.read_text(encoding="utf-8") == "":
        return {
            "valid": True,
            "record_count": 0,
            "errors": [],
            "decision_counts": {},
            "constitutional_violation_count": 0,
            "first_hash": None,
            "latest_hash": None,
            "hmac_record_count": 0,
            "unkeyed_record_count": 0,
            "auth_modes_seen": [],
        }

    with ledger_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                error = f"JSON_PARSE_ERROR:{line_number}"
                errors.append(error)
                integrity_errors.append(error)

    previous_hash = "GENESIS"
    first_hash: str | None = None
    latest_hash: str | None = None

    for index, record in enumerate(records, start=1):
        record_hash = record.get("record_hash")
        if index == 1:
            first_hash = record_hash
        latest_hash = record_hash

        if record.get("sequence_number") != index:
            error = f"SEQUENCE_NUMBER_MISMATCH:{index}"
            errors.append(error)
            integrity_errors.append(error)
        if record.get("previous_record_hash") != previous_hash:
            error = f"PREVIOUS_HASH_MISMATCH:{index}"
            errors.append(error)
            integrity_errors.append(error)
        if compute_record_hash(record) != record_hash:
            error = f"RECORD_HASH_MISMATCH:{index}"
            errors.append(error)
            integrity_errors.append(error)

        auth_mode = record.get("tamper_evidence_mode", UNKEYED_HASH_CHAIN)
        if auth_mode not in auth_modes_seen:
            auth_modes_seen.append(auth_mode)
        if auth_mode == UNKEYED_HASH_CHAIN:
            unkeyed_record_count += 1
            if record.get("record_mac") is not None:
                error = f"UNKEYED_RECORD_MAC_PRESENT:{index}"
                errors.append(error)
                integrity_errors.append(error)
        elif auth_mode == HMAC_SHA256_V1:
            hmac_record_count += 1
            if expected_key_id is not None and record.get("key_id") != expected_key_id:
                error = f"HMAC_KEY_ID_MISMATCH:{index}"
                errors.append(error)
                integrity_errors.append(error)
            if not hmac_key:
                error = f"HMAC_KEY_MISSING:{index}"
                errors.append(error)
                integrity_errors.append(error)
            elif not verify_record_mac(record, hmac_key):
                error = f"HMAC_RECORD_MAC_MISMATCH:{index}"
                errors.append(error)
                integrity_errors.append(error)
        else:
            error = f"UNKNOWN_AUTH_MODE:{index}"
            errors.append(error)
            integrity_errors.append(error)

        envelope = record.get("envelope", {})
        constitutional_errors = verify_constitutional_invariants(envelope)
        has_constitutional_violation = "CONSTITUTIONAL_VIOLATION" in constitutional_errors
        if has_constitutional_violation:
            constitutional_violation_count += 1
            errors.append(f"CONSTITUTIONAL_VIOLATION:{index}")
        if "EXECUTION_WITHOUT_AUTHORIZATION" in constitutional_errors:
            errors.append(f"EXECUTION_WITHOUT_AUTHORIZATION:{index}")

        decision = record.get("receipt", {}).get("decision") or envelope.get("decision")
        if reviewer_registry is not None and record.get("receipt", {}).get("review_status") == "APPROVED":
            if record.get("receipt", {}).get("reviewer_identity_verified") is not True:
                errors.append(f"REVIEWER_IDENTITY_MISSING_FOR_APPROVED_ACTION:{index}")
        if decision and not has_constitutional_violation:
            decision_counts[decision] = decision_counts.get(decision, 0) + 1

        previous_hash = record_hash

    return {
        "valid": len(integrity_errors) == 0,
        "record_count": len(records),
        "errors": errors,
        "decision_counts": decision_counts,
        "constitutional_violation_count": constitutional_violation_count,
        "first_hash": first_hash,
        "latest_hash": latest_hash,
        "hmac_record_count": hmac_record_count,
        "unkeyed_record_count": unkeyed_record_count,
        "auth_modes_seen": auth_modes_seen,
    }
