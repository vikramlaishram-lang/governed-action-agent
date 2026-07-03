# M13 Hosted Receipt Viewer Local UI

## Purpose

M13 adds a local static receipt viewer that renders the governed agent ledger report into browser-readable files.

## What Changed From M12

M12 hardened reviewer identity validation. M13 adds local explainability UI over the existing report summary. It does not add a new verifier, executor, GitHub writer, deployment path, or approval authority.

## Local Viewer Model

The viewer is generated from `generate_report_summary`. It writes static files to a local directory and can be opened in a browser. The viewer is read-only and never modifies the ledger.

## Viewer Files

Default CLI output:

```text
.governed-agent/viewer/index.html
.governed-agent/viewer/viewer_data.json
```

## CLI Usage

```bash
PYTHONPATH=src python -m gcr_agent.cli init
PYTHONPATH=src python -m gcr_agent.cli ask "Read README.md"
PYTHONPATH=src python -m gcr_agent.cli ask "Read .env"
PYTHONPATH=src python -m gcr_agent.cli viewer
```

Optional output directory:

```bash
PYTHONPATH=src python -m gcr_agent.cli viewer --output-dir .governed-agent/viewer
```

`--serve` uses Python standard library `http.server` for local viewing only.

## Data Sanitization

Viewer data is sanitized before writing JSON or HTML. It redacts HMAC key material, GitHub tokens, authorization values, token secrets, full diff text, patch text, private keys, credential-like values, and secret-like `.env` contents.

Allowed evidence includes key ids, record hashes, MAC presence through summary counts, diff hashes, evidence hashes, proposal ids, receipt ids, reviewer ids and roles, risk flags, public claims, and limitations.

## Sections Rendered

- Project Summary
- Ledger Integrity
- Decision Summary
- Violations
- Reviewer Identity
- Review-Approved Actions
- Denied Actions
- Request-Review Actions
- GitHub PR Evidence
- Code Change Proposals
- Public Claims Allowed by Evidence
- Limitations / Non-Claims
- Latest Hash

## What The Viewer Can Prove

The viewer can show the local report summary, ledger integrity status, decision counts, violation counts, reviewer identity summary, read-only GitHub PR evidence summaries, sandboxed code-change proposal summaries, public claims, limitations, and latest hash.

## What It Cannot Prove

M13 is a local static viewer. M13 is not a cloud dashboard. M13 does not add execution authority. M13 does not certify production safety. M13 does not replace external review. M13 does not expose secrets or tokens. M13 does not perform GitHub writes. M13 does not perform deployment.

## Demo Command

```bash
PYTHONPATH=src python demo/run_m13_hosted_receipt_viewer_local_ui_demo.py
```

## Test Command

```bash
PYTHONPATH=src python -m pytest -q
```

## Current Limitations

The viewer is static and local. It has no authentication, no remote sharing, no cloud hosting, no incremental refresh, and no external reviewer workflow.

## Next Milestone Suggestion

M14 should add portable audit bundle export containing policy, reviewer registry, ledger, reports, viewer output, schemas, checksums, and replay instructions for external reproduction.
