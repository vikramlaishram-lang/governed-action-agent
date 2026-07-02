# Governed Action Agent

Governed Action Agent is a runnable local prototype of an AI-agent control loop. It receives a user request, converts it into a bounded Goal Contract, labels the output mode, classifies consequence, creates a Proposal Object, maps it into a Decision Envelope, verifies constitutional invariants, applies a small policy engine, simulates the allowed or blocked action, and produces a receipt.

The core invariant is:

> The agent may propose. The agent may not self-authorize execution.

The machine-checkable rule is simple: if `execution_authority_claimed == true`, the verifier returns `CONSTITUTIONAL_VIOLATION`.

## Problem It Solves

Modern coding and release agents can plan useful work, but their action boundaries need to be explicit and auditable. This prototype shows one way to separate proposal from authorization. Each request is turned into a durable envelope with policy results, invariant checks, execution status, outcome status, and a receipt that can be inspected after the fact.

## Current Scope

This project is a local governed coding and release agent prototype. It supports four demonstration paths:

- safe read requests
- secret access denial
- production deployment review requests
- self-authorization attack detection

M2 actions are simulated locally. M3 adds a controlled real local tool boundary for read-only and development feedback actions:

- `read_file_real`
- `list_files_real`
- `git_diff_real`
- `run_tests_real`

These tools are only invoked after the policy decision is `ALLOW` and constitutional verification has passed. The boundary blocks secret-like file reads, path traversal outside the governed root, shell execution, production deployment, and destructive filesystem actions. Denied, review-required, and constitutional-violation paths do not invoke tools.

### M3 Commands

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python demo/run_governed_agent_demo.py
PYTHONPATH=src python demo/run_m3_controlled_local_tool_demo.py
```

M3 does not allow secrets access, deployment, deletion, arbitrary shell commands, or network calls.

## Out Of Scope

- live production deployment
- real secrets access
- destructive writes
- persistent service operation
- external reviewer closure
- external agent frameworks

## Install

Use Python 3.12 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
```

## Run Tests

```bash
PYTHONPATH=src python -m pytest -q
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q
```

## Run Demo

```bash
PYTHONPATH=src python demo/run_governed_agent_demo.py
```

Expected output:

```text
SAFE_READ: ALLOW
SECRET_ACCESS: DENY
PRODUCTION_DEPLOY: REQUEST_REVIEW
SELF_AUTHORIZATION_ATTACK: CONSTITUTIONAL_VIOLATION
RECEIPTS_GENERATED: 4
```
