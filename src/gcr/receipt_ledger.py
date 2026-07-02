from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from .ledger_auth import (
    HMAC_SHA256_V1,
    UNKEYED_HASH_CHAIN,
    canonical_json as canonical_json_bytes,
    compute_record_hash,
    compute_record_mac,
    resolve_auth_config,
)


def canonical_json(value: dict) -> str:
    return canonical_json_bytes(value).decode("utf-8")


def ledger_record_hash(record: dict) -> str:
    return compute_record_hash(record)


class ReceiptLedger:
    def __init__(
        self,
        path: str | Path,
        *,
        auth_mode: str | None = None,
        hmac_key: str | None = None,
        key_id: str | None = None,
    ) -> None:
        self.path = Path(path)
        self.auth_config = resolve_auth_config(auth_mode=auth_mode, hmac_key=hmac_key, key_id=key_id)

    def append_record(
        self,
        *,
        receipt: dict,
        envelope: dict,
        verification_errors: list[str],
        tool_result: dict,
    ) -> dict:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        records = self.read_records()
        sequence_number = len(records) + 1
        previous_record_hash = records[-1]["record_hash"] if records else "GENESIS"
        record = {
            "schema_version": "receipt_ledger_record_v0.2",
            "ledger_record_id": f"ledger_{uuid4().hex}",
            "created_at": datetime.now(UTC).isoformat(),
            "sequence_number": sequence_number,
            "proposal_id": receipt["proposal_id"],
            "agent_id": receipt["agent_id"],
            "receipt": receipt,
            "envelope": envelope,
            "verification_errors": verification_errors,
            "tool_result": tool_result,
            "previous_record_hash": previous_record_hash,
            "record_hash": "",
            "tamper_evidence_mode": self.auth_config["tamper_evidence_mode"],
            "ledger_auth_version": self.auth_config["ledger_auth_version"],
            "key_id": self.auth_config["key_id"],
            "record_mac": None,
        }
        record["record_hash"] = compute_record_hash(record)
        if self.auth_config["tamper_evidence_mode"] == HMAC_SHA256_V1:
            record["record_mac"] = compute_record_mac(record, self.auth_config["hmac_key"])
        elif self.auth_config["tamper_evidence_mode"] != UNKEYED_HASH_CHAIN:
            raise ValueError(f"Unsupported ledger auth mode: {self.auth_config['tamper_evidence_mode']}")
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(record) + "\n")
        return record

    def read_records(self) -> list[dict]:
        if not self.path.exists():
            return []
        records: list[dict] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    records.append(json.loads(line))
        return records

    def latest_hash(self) -> str:
        records = self.read_records()
        return records[-1]["record_hash"] if records else "GENESIS"

    def clear(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("", encoding="utf-8")
