# M14 Local Release Package And Public Demo

## Purpose

M14 packages the governed-action-agent repo for public local evaluation by reviewers, judges, investors, and developers.

## What Changed From M13

M13 added a local receipt viewer. M14 adds release packaging, a deterministic public demo, sanitized sample artifacts, quickstart docs, claim boundaries, validation, and cleanup scripts.

## Public Demo Sequence

The demo performs safe read, secret denial, production review request, self-authorization detection, sandboxed code-change proposal, valid scoped reviewer approval, ledger replay, report generation, viewer generation, and sanitization checks.

## Release Package Contents

- `scripts/run_public_demo.py`
- `scripts/validate_release_package.py`
- `scripts/clean_demo_artifacts.py`
- `examples/public_demo_expected_output.txt`
- `examples/sample_governed_agent_report.md`
- `examples/sample_governed_agent_report.json`
- `examples/sample_viewer/index.html`
- `examples/sample_viewer/viewer_data.json`
- public evaluator docs

## Example Artifacts

The example report and viewer are sanitized, parseable, and stable enough for public inspection. They do not include secrets, tokens, private keys, full patches, or machine-specific local paths.

## Sanitization Rules

Public artifacts must not contain HMAC keys, GitHub tokens, authorization headers, bearer tokens, full patches, secret file contents, private key markers, or local machine paths.

## Public Claims Allowed

The project demonstrates a local governed action agent loop, proposal/authorization separation, receipt ledger records, local replay verification, optional HMAC authentication, secret denial, self-authorization detection, scoped review tokens, reviewer identity hardening, sandboxed code-change proposals, reports, and a static local viewer.

## Public Claims Forbidden

Do not claim production safety, complete security, tamper-proof ledger, legal certification, external audit completion, SSO/OIDC identity verification, GitHub write integration, deployment control, total violation detection, autonomous real-repo code modification, or cloud-hosted dashboard.

## Commands

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_public_demo.py
PYTHONPATH=src python scripts/validate_release_package.py
```

## Tests

M14 adds tests for the public demo, release validation, sample artifact sanitization, expected output, claims docs, cleanup safety, and README quickstart paths.

## Current Limitations

M14 is local packaging. It does not add new authority, enforcement, cloud hosting, deployment, GitHub writes, secret access, or real patch application.

## Next Milestone Suggestion

M15 should add a portable audit bundle with checksums and reproduction instructions for external evaluators.
