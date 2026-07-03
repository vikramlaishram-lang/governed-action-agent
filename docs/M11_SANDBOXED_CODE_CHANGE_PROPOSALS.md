# M11 Sandboxed Code Change Proposals

## Purpose

M11 adds sandboxed, diff-only code-change proposals. The agent can propose a patch, classify it, record it, and require review without modifying the real repository.

## What Changed From M10

M10 made the ledger human-reportable. M11 adds:

- code-change proposal artifacts
- sandbox workspace under `.governed-agent/sandbox`
- deterministic README and workflow proposal planning
- CLI `propose-change`
- code-change proposal receipt summaries
- report integration

## Sandbox Model

The sandbox may create copies and proposed files under `.governed-agent/sandbox/`. It rejects path traversal, absolute paths, sensitive files, and blocked directories. It never writes to the original target file.

## Code-Change Proposal Schema

`code_change_proposal_v0.1` records target files, change intent, sandbox path, diff hash, risk flags, review requirement, and `applied_to_real_repo=false`.

## Review Behavior

`CODE_CHANGE` and `WORKFLOW_CHANGE` request review by default. A valid scoped review token can allow sandbox artifact generation as execution, but that execution remains sandbox-only.

## CLI Usage

```bash
PYTHONPATH=src python -m gcr_agent.cli propose-change "Update README.md with governed agent summary"
```

## Receipt Fields

Receipts include a compact code-change proposal summary with artifact id, target files, change intent, diff hash, risk flags, review requirement, and `applied_to_real_repo`.

## Report Integration

Reports include a `Code Change Proposals` section and JSON `code_change_proposals` list.

## Forbidden

M11 creates sandboxed diff proposals only. M11 does not apply patches to the real repo. M11 does not merge PRs. M11 does not write to GitHub. M11 does not execute arbitrary commands. M11 does not make production changes. M11 does not certify code safety.

## Demo Command

```bash
PYTHONPATH=src python demo/run_m11_sandboxed_code_change_demo.py
```

## Test Command

```bash
PYTHONPATH=src python -m pytest -q
```

## Current Limitations

M11 supports deterministic README and workflow proposals only. Patch application to the real repository remains out of scope.

## Next Milestone Suggestion

M12 should add human review packets for sandboxed code-change proposals, including diff hashes, policy decisions, reviewer prompts, and ledger references.
