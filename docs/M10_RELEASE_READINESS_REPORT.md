# M10 Release Readiness Report

## Purpose

M10 makes the governed agent audit trail legible to humans and machines by generating Markdown and JSON reports from the local receipt ledger.

## What Changed From M9

M9 hardened execution authorization invariants. M10 adds a read-only reporting layer over replay verification:

- `gaa report`
- Markdown report
- JSON summary
- ledger integrity summary
- decision counts
- violation counts
- review-approved action summary
- GitHub PR evidence summary
- evidence-bound public claims
- limitations and non-claims

## Report Contents

Reports include project metadata, ledger verification status, auth modes, record count, latest hash, decision counts, violations, reviewed actions, denied actions, request-review actions, GitHub PR evidence, public claims, and limitations.

## Markdown Report

The Markdown report is intended for human review and includes structured sections for integrity, decisions, violations, PR evidence, public claims, and non-claims.

## JSON Summary

The JSON summary is intended for automation and uses schema version `governed_agent_report_v0.1`.

## Public Claims Allowed By Evidence

Claims are conservative and derived only from replayed ledger evidence. The report never claims production safety, complete security, tamper-proof storage, external audit completion, or legal/compliance certification.

## Limitations / Non-Claims

M10 makes the audit trail legible. M10 does not add new execution authority. M10 does not certify production safety. M10 does not replace external review. M10 does not perform real deployment. M10 does not create legal/compliance certification.

## CLI Usage

```bash
PYTHONPATH=src python -m gcr_agent.cli report
PYTHONPATH=src python -m gcr_agent.cli report --format markdown
PYTHONPATH=src python -m gcr_agent.cli report --format json
```

## Demo Command

```bash
PYTHONPATH=src python demo/run_m10_release_readiness_report_demo.py
```

## Test Command

```bash
PYTHONPATH=src python -m pytest -q
```

## Current Limitations

Reports are generated from local ledger records and are only as strong as the available ledger and key material.

## Next Milestone Suggestion

M11 should add exportable audit bundles containing policy, config, ledger, reports, and replay metadata for external reproduction.
