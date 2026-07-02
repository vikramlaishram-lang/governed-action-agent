# M5 Receipt Ledger And Replay Verifier

## Purpose

M5 adds a persistent local receipt ledger and replay verifier. Every governed action can be appended to a local JSONL ledger, chained by hashes, replayed, and independently checked for integrity and constitutional violations.

## What Changed From M4

M4 added policy files and scoped review tokens. M5 keeps that behavior and adds:

- append-only local receipt ledger records
- hash chaining with `previous_record_hash` and `record_hash`
- replay parsing and verification
- tamper detection
- constitutional violation detection during replay
- optional `GovernedAgent(ledger_path=...)` persistence

## Ledger Record Format

Each JSONL line is a `receipt_ledger_record_v0.1` object containing:

- receipt
- decision envelope
- verification errors
- tool result
- sequence number
- previous record hash
- current record hash

## Hash Chain Rule

The first record uses `previous_record_hash = "GENESIS"`. Every later record must set `previous_record_hash` to the previous record's `record_hash`. Each `record_hash` is computed over canonical JSON for the record with `record_hash` blank.

## Replay Verifier Behavior

The replay verifier parses the ledger, checks sequence numbers, checks hash chaining, recomputes record hashes, reruns constitutional invariant checks over each envelope, and summarizes decisions and constitutional violations.

## What Tampering Is Detected

M5 detects:

- modified records
- broken previous-hash links
- missing or reordered records through sequence/hash mismatches
- JSON parse failures
- constitutionally invalid records

## Constitutional Replay

Replay calls `verify_constitutional_invariants(envelope)`. If `execution_authority_claimed` is true, replay reports `CONSTITUTIONAL_VIOLATION` and increments the constitutional violation count.

## Demo Command

```bash
PYTHONPATH=src python demo/run_m5_receipt_ledger_replay_demo.py
```

## Test Command

```bash
PYTHONPATH=src python -m pytest -q
```

## Current Limitations

M5 is local JSONL persistence only. M5 is tamper-evident, not tamper-proof. M5 does not use HMAC or signatures yet. M5 does not implement remote storage. M5 does not implement production deployment. M5 does not replace external review.

## Next Milestone Suggestion

M6 should add signed ledger records or HMAC-backed integrity, plus exportable audit bundles for independent external reproduction.
