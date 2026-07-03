# M9 Execution Authorization Invariant Hardening

## Purpose

M9 makes execution authorization a verifier-level invariant: no envelope or ledger record may claim execution occurred unless the decision was `ALLOW`.

## New Invariant

```text
if execution_status == EXECUTED and decision != ALLOW:
    EXECUTION_WITHOUT_AUTHORIZATION
```

## What Changed

- `verify_constitutional_invariants` now reports `EXECUTION_WITHOUT_AUTHORIZATION`.
- Replay verification reports `EXECUTION_WITHOUT_AUTHORIZATION:<sequence>`.
- Named tests prove denied, review-required, and blocked actions do not execute.
- Replay tests prove a tampered denied record claiming execution is detected.

## Boundary

M9 does not add new tools, deployments, writes, or external integrations. It hardens the existing governed execution contract.
