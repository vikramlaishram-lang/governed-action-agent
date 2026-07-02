# M3 Controlled Local Tool Boundary

## Purpose

M3 moves the Governed Action Agent from pure simulation to controlled local development tools while preserving the invariant: the agent may propose, and the agent may not self-authorize execution.

## What Changed From M2

M2 produced governed proposals, envelopes, policy decisions, simulated execution, and receipts. M3 keeps that loop and adds a real local tool boundary that only runs after policy returns `ALLOW` and constitutional verification passes.

## Allowed Tools

- `list_files_real`: lists visible files under the repository root.
- `read_file_real`: reads allowed files under the repository root.
- `run_tests_real`: runs the fixed command `python -m pytest -q`.
- `git_diff_real`: runs fixed Git read commands: `git diff --stat` and `git status --short`.

## Forbidden Actions

- secrets access
- path traversal outside the repository root
- reads from `.git/`, `node_modules/`, virtual environments, and bytecode caches
- production deployment
- destructive deletion
- arbitrary shell commands
- network calls
- credential access
- write operations without review

## Safety Boundaries

All file paths are resolved against the governed repository root. Secret-like filenames such as `.env`, `.env.local`, `.env.production`, `secrets.json`, `credentials.json`, `id_rsa`, and `id_ed25519` are rejected before file content is read. If the policy decision is not `ALLOW`, or if the verifier reports `CONSTITUTIONAL_VIOLATION`, no real tool is invoked.

## Demo Command

```bash
PYTHONPATH=src python demo/run_m3_controlled_local_tool_demo.py
```

## Test Command

```bash
PYTHONPATH=src python -m pytest -q
```

## Current Limitations

The M3 tool boundary is intentionally local and narrow. It does not perform writes, deployments, credential lookup, network calls, or external reviewer closure.

## Next Milestone Suggestion

M4 should add human review handoff artifacts: review packets, reviewer decisions, and a separate authorization record that remains outside the agent's self-issued authority.
