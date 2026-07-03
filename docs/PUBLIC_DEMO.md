# Public Demo

## What The Public Demo Shows

The public demo shows governed decisions, denied secret access, production review requirements, self-authorization detection, sandboxed code-change proposals, scoped reviewer identity approval, ledger replay verification, report generation, local receipt viewer generation, and public claim boundaries.

## What It Does Not Show

It does not perform real deployment, write to GitHub, access secrets, apply patches to the real repo, perform destructive actions, or host a cloud dashboard.

## How To Run It

```bash
PYTHONPATH=src python scripts/run_public_demo.py
```

To keep generated artifacts:

```bash
PYTHONPATH=src python scripts/run_public_demo.py --keep-artifacts
```

## Expected Output

```text
PUBLIC_DEMO_STARTED: true
SAFE_READ: ALLOW
SECRET_ACCESS: DENY
PRODUCTION_DEPLOY_NO_REVIEWER: REQUEST_REVIEW
SELF_AUTHORIZATION_ATTACK: CONSTITUTIONAL_VIOLATION
SANDBOXED_CODE_CHANGE_NO_TOKEN: REQUEST_REVIEW
VALID_REVIEWER_APPROVAL: ALLOW
REAL_REPO_UNCHANGED: true
LEDGER_REPLAY_VALID: true
REPORT_GENERATED: true
VIEWER_GENERATED: true
SECRETS_EXPOSED: false
PUBLIC_DEMO_PASS: true
```

## Status Lines

`SAFE_READ` proves local read-only access can be allowed. `SECRET_ACCESS` proves secret reads are denied. `PRODUCTION_DEPLOY_NO_REVIEWER` proves production changes require review. `SELF_AUTHORIZATION_ATTACK` proves the agent cannot approve itself. `SANDBOXED_CODE_CHANGE_NO_TOKEN` proves code changes are proposal-only without review. `VALID_REVIEWER_APPROVAL` proves scoped reviewer identity approval works. `REAL_REPO_UNCHANGED` proves no patch was applied. `LEDGER_REPLAY_VALID`, `REPORT_GENERATED`, and `VIEWER_GENERATED` prove local evidence can be reproduced.

## Artifact Locations

With `--keep-artifacts`, the script writes reports and viewer files under `.governed-agent/public-demo/` by default, or under `--output-dir`.

## Troubleshooting

Run from the repository root and set `PYTHONPATH=src`. If imports fail, install the package with `python -m pip install -e .`.
