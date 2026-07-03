# Governed Action Agent

A local governed action-agent prototype that separates AI proposals from execution authority and records decisions as verifiable receipts.

Governed Action Agent is a runnable local prototype of an AI-agent control loop. It receives a user request, converts it into a bounded Goal Contract, labels the output mode, classifies consequence, creates a Proposal Object, maps it into a Decision Envelope, verifies constitutional invariants, applies a small policy engine, simulates the allowed or blocked action, and produces a receipt.

The core invariant is:

> The agent may propose. The agent may not self-authorize execution.

The machine-checkable rule is simple: if `execution_authority_claimed == true`, the verifier returns `CONSTITUTIONAL_VIOLATION`.

## Quickstart

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_public_demo.py
PYTHONPATH=src python scripts/validate_release_package.py
```

Evaluator docs:

- [docs/EVALUATOR_QUICKSTART.md](docs/EVALUATOR_QUICKSTART.md)
- [docs/PUBLIC_DEMO.md](docs/PUBLIC_DEMO.md)
- [docs/PUBLIC_CLAIMS_AND_LIMITATIONS.md](docs/PUBLIC_CLAIMS_AND_LIMITATIONS.md)
- [docs/RELEASE_PACKAGE.md](docs/RELEASE_PACKAGE.md)

## Expected Public Demo Output

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

## What It Demonstrates

- safe read allowed
- secret access denied
- production deploy requires review
- self-authorization detected
- sandboxed code-change proposal does not modify real repo
- valid reviewer approval works within scope
- ledger replay verifies
- report and viewer generate
- secrets are not exposed

## What It Does Not Claim

- production safety
- cloud hosting
- real deployment
- real GitHub writes
- full security
- external audit
- legal/compliance certification

## Milestone Status

| Milestone | Description | Status |
| --- | --- | --- |
| M2 | Runnable governed agent loop | Complete |
| M3 | Controlled local tool boundary | Complete |
| M4 | Policy file and scoped review tokens | Complete |
| M5 | Receipt ledger and replay verifier | Complete |
| M6 | HMAC signed ledger and keyed verification | Complete |
| M7 | CLI packaging and project config | Complete |
| M8 | GitHub PR read-only integration | Complete |
| M9 | Execution authorization invariant hardening | Complete |
| M10 | Release readiness report | Complete |
| M11 | Sandboxed code-change proposals | Complete |
| M12 | Reviewer identity hardening | Complete |
| M13 | Local receipt viewer UI | Complete |
| M14 | Local release package and public demo | Complete |
| M15 | External reproduction and review packet | Prepared for external review |

## CLI Commands

- `init`
- `status`
- `ask`
- `agent`
- `propose-change`
- `inspect-pr`
- `report`
- `viewer`
- `reviewers`
- `verify-ledger`

## Artifacts

- receipt ledger: `.governed-agent/ledger.jsonl`
- report markdown/json: `.governed-agent/reports/`
- viewer index/data: `.governed-agent/viewer/`
- sample artifacts: `examples/`

## Real Agent Runtime

`gaa agent "<task>"` adds the real agent core. The runtime collects safe repository context, calls an LLM/planner interface, parses a structured model proposal, normalizes it, and routes it through the existing governance layer before any bounded tool can run.

The model proposal is untrusted. Governance still decides. The model cannot directly set `ALLOW`, cannot set execution status, and cannot self-authorize execution.

Deterministic demos and tests use `FakeLLMClient`:

```bash
PYTHONPATH=src python -m gcr_agent.cli agent "Read README.md" --fake-llm --trace
PYTHONPATH=src python demo/run_real_agent_core_demo.py
```

An optional provider can be wired later with `GAA_LLM_BASE_URL`, `GAA_LLM_API_KEY`, and `GAA_LLM_MODEL`. Public demo and release status remain local evaluation only.

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

### M12 Reviewer Identity Hardening

M12 adds:

- reviewer identity manifests
- local reviewer authority registry
- review token v0.2
- reviewer identity hash binding
- issuer binding
- active/revoked/suspended reviewer checks
- role/scope validation
- reviewer identity fields in receipts/reports
- CLI reviewer registry status

M12 still does not add:

- SSO/OIDC
- production IAM
- legal identity proof
- remote audit
- real deployment
- GitHub writes
- secret access
- destructive action

Commands:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python demo/run_m12_reviewer_identity_hardening_demo.py
```

CLI examples:

```bash
PYTHONPATH=src python -m gcr_agent.cli init
PYTHONPATH=src python -m gcr_agent.cli status
PYTHONPATH=src python -m gcr_agent.cli reviewers
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

### M13 Hosted Receipt Viewer Local UI

M13 adds:

- local receipt viewer
- static HTML output
- viewer_data.json
- CLI `gaa viewer`
- ledger integrity visualization
- decision summary visualization
- violation summary visualization
- reviewer identity visualization
- GitHub PR evidence visualization
- code-change proposal visualization
- public claims and limitations section

M13 still does not add:

- hosted cloud dashboard
- authentication
- remote sharing
- production deployment
- GitHub writes
- secret access
- patch application

Commands:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python demo/run_m13_hosted_receipt_viewer_local_ui_demo.py
```

CLI example:

```bash
PYTHONPATH=src python -m gcr_agent.cli init
PYTHONPATH=src python -m gcr_agent.cli ask "Read README.md"
PYTHONPATH=src python -m gcr_agent.cli ask "Read .env"
PYTHONPATH=src python -m gcr_agent.cli viewer
```

### M15 External Reproduction and Review Packet

Purpose: prepare an external reproduction packet so an independent reviewer can clone the repo, run local checks, compare expected outputs, and record an attestation.

Packet location:

- `docs/external_review/`
- `examples/external_review/`

Reviewer commands:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_public_demo.py
PYTHONPATH=src python scripts/validate_release_package.py
PYTHONPATH=src python scripts/validate_external_review_packet.py
```

Packet generation command:

```bash
PYTHONPATH=src python scripts/generate_external_review_packet.py
```

Packet validation command:

```bash
PYTHONPATH=src python scripts/validate_external_review_packet.py
```

Status:

```text
M15_PACKET_PREPARED_FOR_EXTERNAL_REVIEW
M15_EXTERNAL_REVIEW_NOT_YET_COMPLETE
```

M15 prepares the packet. It does not say external review is done.

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
