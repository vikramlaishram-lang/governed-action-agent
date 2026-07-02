# M6 HMAC Signed Ledger And Keyed Verification

## Purpose

M6 adds keyed integrity to the local receipt ledger using HMAC-SHA256. The ledger now supports unkeyed hash-chain verification for local development and HMAC-authenticated verification for keyed replay.

## What Changed From M5

M5 added an append-only JSONL ledger and replay verifier. M6 keeps that behavior and adds:

- `HMAC_SHA256_V1` ledger records
- `key_id`
- `record_mac`
- keyed replay verification
- wrong-key rejection
- recomputed-hash tamper detection
- a production guard that rejects unkeyed mode

## UNKEYED_HASH_CHAIN vs HMAC_SHA256_V1

`UNKEYED_HASH_CHAIN` is the M5-compatible default in local runtime mode. It is tamper-evident under local verification, but not authenticated.

`HMAC_SHA256_V1` adds a keyed MAC over each record. A verifier must have the correct key to validate the ledger.

## Ledger Record v0.2 Format

Ledger record v0.2 adds:

- `tamper_evidence_mode`
- `ledger_auth_version`
- `key_id`
- `record_mac`

## What record_hash Proves

`record_hash` proves the local hash chain is internally consistent when replayed. It is computed over canonical JSON excluding `record_hash` and `record_mac`.

## What record_mac Proves

`record_mac` proves that a verifier with the correct HMAC key can authenticate the record contents, including `record_hash`. It detects modified records even when an attacker recomputes `record_hash`.

## Key Handling

The HMAC key can come from constructor arguments or `GAA_LEDGER_HMAC_KEY`. The key id can come from constructor arguments or `GAA_LEDGER_HMAC_KEY_ID`. The HMAC secret is never stored in ledger records.

## Environment Variables

- `GAA_LEDGER_AUTH_MODE`
- `GAA_LEDGER_HMAC_KEY`
- `GAA_LEDGER_HMAC_KEY_ID`
- `GAA_RUNTIME_MODE`

## Demo Command

```bash
PYTHONPATH=src python demo/run_m6_hmac_signed_ledger_demo.py
```

## Test Command

```bash
PYTHONPATH=src python -m pytest -q
```

## Attacks Detected

M6 detects:

- modified HMAC records
- wrong keys
- missing keys for HMAC records
- recomputed-hash attacks
- key id mismatches when expected
- constitutional violations during replay

## Current Limitations

M6 is authenticated local ledger integrity. M6 is not remote notarization. M6 is not key management infrastructure. M6 does not store secrets safely for production. M6 does not implement signatures or KMS. M6 does not perform real production deployment.

## Next Milestone Suggestion

M7 should add signed audit bundle export and external reproduction tooling so an independent reviewer can verify policy, envelopes, receipts, and ledger integrity from a portable artifact.
