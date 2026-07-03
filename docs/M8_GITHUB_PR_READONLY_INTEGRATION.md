# M8 GitHub PR Read-Only Integration

## Purpose

M8 adds read-only GitHub pull request inspection as governed evidence ingestion. The agent can inspect PR metadata, changed-file metadata, and checks/status evidence, then produce receipts and ledger records without writing to GitHub.

## What Changed From M7

M7 added local CLI packaging and project config. M8 adds:

- GitHub PR URL parsing
- fixture-based PR snapshot ingestion
- optional live GitHub API GET support
- changed-file metadata snapshots
- checks/status evidence
- risk flags
- PR evidence hashes
- CLI `inspect-pr`
- ledger append/replay for PR inspections

## Read-Only Evidence Ingestion

PR inspection only collects metadata. It does not comment, approve, merge, dispatch workflows, update statuses, write branches, or perform release actions.

## Fixture Mode

Fixture mode is deterministic and used by tests and demos:

```bash
PYTHONPATH=src python -m gcr_agent.cli inspect-pr https://github.com/owner/repo/pull/42 --fixture tests/fixtures/github/pr_ready.json
```

## Optional Live GitHub API Mode

Live mode uses standard-library `urllib` and only GET requests. If `GITHUB_TOKEN` is set, it is used as an Authorization header but is never stored in snapshots, envelopes, receipts, config, or ledger records.

## CLI Command

```bash
PYTHONPATH=src python -m gcr_agent.cli inspect-pr https://github.com/vikramlaishram-lang/governed-action-agent/pull/42 --fixture tests/fixtures/github/pr_ready.json
```

## Receipt Fields

PR receipts include evidence references, evidence gaps, and a compact `github_pr` summary with owner, repo, PR number, evidence hash, checks status, and risk flags.

## Risk Flags

- `SENSITIVE_FILE_TOUCHED`
- `CHECKS_NOT_PASSING`
- `LARGE_CHANGESET`
- `PR_NOT_OPEN`

## Explicitly Forbidden

M8 does not write to GitHub. M8 does not comment on PRs. M8 does not approve PRs. M8 does not merge PRs. M8 does not run workflows. M8 does not expose patches/secrets in receipts. M8 does not make production release decisions.

## Test Command

```bash
PYTHONPATH=src python -m pytest -q
```

## Demo Command

```bash
PYTHONPATH=src python demo/run_m8_github_pr_readonly_demo.py
```

## Current Limitations

Live GitHub support is intentionally minimal and read-only. Fixture mode is the primary deterministic integration surface for M8.

## Next Milestone Suggestion

M9 should add governed PR review packet generation: a local artifact summarizing evidence, risks, ledger hashes, and suggested reviewer questions, still without writing to GitHub.
