from __future__ import annotations

import copy
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


def canonical_json(value: dict) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def ledger_record_hash(record: dict) -> str:
    hashable = copy.deepcopy(record)
    hashable["record_hash"] = ""
    digest = hashlib.sha256(canonical_json(hashable).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


class ReceiptLedger:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

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
            "schema_version": "receipt_ledger_record_v0.1",
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
        }
        record["record_hash"] = ledger_record_hash(record)
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
