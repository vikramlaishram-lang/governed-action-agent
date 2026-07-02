from __future__ import annotations

import json
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from gcr.ledger_auth import HMAC_SHA256_V1, compute_record_hash
from gcr.receipt_ledger import ReceiptLedger
from gcr.replay_verifier import verify_ledger
from gcr_agent import GovernedAgent


def _copy_and_mutate(source: Path, target: Path, *, recompute_hash: bool) -> None:
    shutil.copyfile(source, target)
    records = [json.loads(line) for line in target.read_text(encoding="utf-8").splitlines()]
    records[0]["receipt"]["decision"] = "DENY"
    if recompute_hash:
        records[0]["record_hash"] = compute_record_hash(records[0])
    target.write_text("\n".join(json.dumps(record, sort_keys=True) for record in records) + "\n", encoding="utf-8")


def main() -> None:
    with TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)

        unkeyed_ledger = base / "unkeyed.jsonl"
        unkeyed_agent = GovernedAgent(ledger_path=unkeyed_ledger)
        unkeyed_agent.handle_request("Read README.md")
        unkeyed_agent.handle_request("List files")
        unkeyed_summary = verify_ledger(unkeyed_ledger)

        hmac_key = "m6-demo-dev-key"
        key_id = "m6-demo-key"
        hmac_ledger = base / "hmac.jsonl"
        hmac_agent = GovernedAgent(
            ledger_path=hmac_ledger,
            ledger_auth_mode=HMAC_SHA256_V1,
            ledger_hmac_key=hmac_key,
            ledger_key_id=key_id,
        )
        hmac_agent.handle_request("Read README.md")
        hmac_agent.handle_request("List files")
        hmac_agent.handle_request("Run tests")
        hmac_summary = verify_ledger(hmac_ledger, hmac_key=hmac_key, expected_key_id=key_id)
        wrong_key_summary = verify_ledger(hmac_ledger, hmac_key="wrong-key", expected_key_id=key_id)

        tampered_ledger = base / "tampered.jsonl"
        _copy_and_mutate(hmac_ledger, tampered_ledger, recompute_hash=False)
        tampered_summary = verify_ledger(tampered_ledger, hmac_key=hmac_key, expected_key_id=key_id)

        recomputed_ledger = base / "recomputed.jsonl"
        _copy_and_mutate(hmac_ledger, recomputed_ledger, recompute_hash=True)
        recomputed_summary = verify_ledger(recomputed_ledger, hmac_key=hmac_key, expected_key_id=key_id)

        records = ReceiptLedger(hmac_ledger).read_records()
        key_not_stored = hmac_key not in hmac_ledger.read_text(encoding="utf-8") and all(
            "hmac_key" not in record for record in records
        )

        print(f"UNKEYED_REPLAY_VALID: {str(unkeyed_summary['valid']).lower()}")
        print(f"HMAC_REPLAY_VALID: {str(hmac_summary['valid']).lower()}")
        print(f"HMAC_RECORDS_WRITTEN: {hmac_summary['hmac_record_count']}")
        print(f"HMAC_TAMPER_DETECTED: {str(not tampered_summary['valid']).lower()}")
        print(f"HMAC_RECOMPUTED_HASH_ATTACK_DETECTED: {str(not recomputed_summary['valid']).lower()}")
        print(f"HMAC_WRONG_KEY_REJECTED: {str(not wrong_key_summary['valid']).lower()}")
        print(f"HMAC_KEY_NOT_STORED: {str(key_not_stored).lower()}")


if __name__ == "__main__":
    main()
