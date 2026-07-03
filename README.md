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

### M4 Policy File And Review Tokens

M4 adds:

- configurable policy file
- scoped review token
- approval validation
- reviewer-role checks
- approved simulated production change

M4 still blocks:

- self-authorization
- secret access
- destructive delete
- real deployment
- arbitrary shell commands
- network calls

Commands:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python demo/run_governed_agent_demo.py
PYTHONPATH=src python demo/run_m3_controlled_local_tool_demo.py
PYTHONPATH=src python demo/run_m4_policy_review_token_demo.py
```

### M5 Receipt Ledger And Replay Verifier

M5 adds:

- persistent local receipt ledger
- append-only JSONL records
- hash chain
- replay verifier
- tamper detection
- constitutional violation detection during replay

M5 still does not add:

- real production deployment
- secret access
- destructive actions
- network calls
- cryptographic signing/HMAC
- remote audit storage

Commands:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python demo/run_governed_agent_demo.py
PYTHONPATH=src python demo/run_m3_controlled_local_tool_demo.py
PYTHONPATH=src python demo/run_m4_policy_review_token_demo.py
PYTHONPATH=src python demo/run_m5_receipt_ledger_replay_demo.py
```

### M6 HMAC Signed Ledger Verification

M6 adds:

- HMAC-SHA256 ledger authentication
- key_id
- record_mac
- keyed replay verification
- wrong-key rejection
- recomputed-hash tamper detection
- production guard requiring HMAC mode

M6 still does not add:

- real production deployment
- secret access
- destructive actions
- network calls
- cloud KMS
- public-key signatures
- remote notarization

Commands:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python demo/run_governed_agent_demo.py
PYTHONPATH=src python demo/run_m3_controlled_local_tool_demo.py
PYTHONPATH=src python demo/run_m4_policy_review_token_demo.py
PYTHONPATH=src python demo/run_m5_receipt_ledger_replay_demo.py
PYTHONPATH=src python demo/run_m6_hmac_signed_ledger_demo.py
```

### M7 CLI Packaging And Project Config

M7 adds a local CLI and per-project `.governed-agent/` directory:

```text
.governed-agent/
  config.json
  policy.json
  ledger.jsonl
```

CLI commands:

```bash
PYTHONPATH=src python -m gcr_agent.cli init
PYTHONPATH=src python -m gcr_agent.cli status
PYTHONPATH=src python -m gcr_agent.cli ask "Read README.md"
PYTHONPATH=src python -m gcr_agent.cli ask "Read .env"
PYTHONPATH=src python -m gcr_agent.cli verify-ledger
PYTHONPATH=src python -m gcr_agent.cli demo
```

If installed:

```bash
gaa init
gaa ask "Read README.md"
gaa verify-ledger
```

M7 still blocks real deployment, secret access, destructive actions, network calls, and arbitrary shell execution.

### M8 GitHub PR Read-Only Integration

M8 adds:

- read-only GitHub PR inspection
- PR evidence snapshots
- changed-file metadata
- checks/status evidence
- risk flags
- PR receipts
- ledger append/replay for PR inspection

M8 still does not add:

- comments
- merges
- PR approvals
- workflow dispatch
- GitHub writes
- production release execution

Commands:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python demo/run_governed_agent_demo.py
PYTHONPATH=src python demo/run_m3_controlled_local_tool_demo.py
PYTHONPATH=src python demo/run_m4_policy_review_token_demo.py
PYTHONPATH=src python demo/run_m5_receipt_ledger_replay_demo.py
PYTHONPATH=src python demo/run_m6_hmac_signed_ledger_demo.py
PYTHONPATH=src python demo/run_m7_cli_packaging_demo.py
PYTHONPATH=src python demo/run_m8_github_pr_readonly_demo.py
```

CLI example:

```bash
PYTHONPATH=src python -m gcr_agent.cli init
PYTHONPATH=src python -m gcr_agent.cli inspect-pr https://github.com/vikramlaishram-lang/governed-action-agent/pull/42 --fixture tests/fixtures/github/pr_ready.json
PYTHONPATH=src python -m gcr_agent.cli verify-ledger
```

### M10 Release Readiness Report

M10 adds:

- `gaa report`
- Markdown report
- JSON report
- ledger integrity summary
- decision counts
- violation counts
- review-approved action summary
- GitHub PR evidence summary
- evidence-bound public claims
- limitations/non-claims

Commands:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python demo/run_m10_release_readiness_report_demo.py
```

CLI example:

```bash
PYTHONPATH=src python -m gcr_agent.cli init
PYTHONPATH=src python -m gcr_agent.cli ask "Read README.md"
PYTHONPATH=src python -m gcr_agent.cli ask "Read .env"
PYTHONPATH=src python -m gcr_agent.cli report
```

### M11 Sandboxed Code Change Proposals

M11 adds:

- sandboxed code-change proposals
- diff-only artifacts
- no real repo modification
- review-required CODE_CHANGE
- CLI propose-change
- code-change proposal receipts
- report inclusion

M11 still does not add:

- real file writes
- patch application
- PR creation
- GitHub writes
- merge
- deployment
- arbitrary shell

Commands:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python demo/run_m11_sandboxed_code_change_demo.py
```

CLI example:

```bash
PYTHONPATH=src python -m gcr_agent.cli init
PYTHONPATH=src python -m gcr_agent.cli propose-change "Update README.md with governed agent summary"
PYTHONPATH=src python -m gcr_agent.cli report
```

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
