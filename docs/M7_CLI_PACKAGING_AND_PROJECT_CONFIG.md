# M7 CLI Packaging And Project Config

## Purpose

M7 makes the Governed Action Agent usable from a local command line against any local repository.

## What Changed From M6

M6 added HMAC-authenticated ledger verification. M7 keeps the governed agent spine and adds:

- installable `gaa` console script
- `python -m gcr_agent.cli` support
- local `.governed-agent/` project directory
- project config file
- project policy copy
- project ledger path management
- HMAC metadata support
- ask, status, verify-ledger, and demo commands

## CLI Commands

```bash
gaa init
gaa init --hmac --key-id local-dev-key
gaa status
gaa ask "Read README.md"
gaa ask "Run tests"
gaa verify-ledger
gaa demo
```

The module form also works:

```bash
PYTHONPATH=src python -m gcr_agent.cli ask "Read README.md"
```

## Project Directory Structure

```text
.governed-agent/
  config.json
  policy.json
  ledger.jsonl
```

## Config Format

`config.json` stores project metadata, ledger path, policy path, auth mode, and key id. It never stores the HMAC key.

## HMAC Mode Behavior

For HMAC projects, `GAA_LEDGER_HMAC_KEY` must be set for `ask` and `verify-ledger`. If it is missing, the CLI exits nonzero and prints `GAA_ERROR: HMAC_KEY_MISSING`.

## Environment Variables

- `GAA_LEDGER_HMAC_KEY`
- `GAA_LEDGER_HMAC_KEY_ID`
- `GAA_LEDGER_AUTH_MODE`
- `GAA_RUNTIME_MODE`

## Example Usage

```bash
PYTHONPATH=src python -m gcr_agent.cli init
PYTHONPATH=src python -m gcr_agent.cli ask "Read README.md"
PYTHONPATH=src python -m gcr_agent.cli verify-ledger
```

## Test Command

```bash
PYTHONPATH=src python -m pytest -q
```

## Demo Command

```bash
PYTHONPATH=src python demo/run_m7_cli_packaging_demo.py
```

## Limitations

M7 makes the agent usable from a local CLI. M7 still does not do real deployment. M7 still blocks secret access. M7 still blocks self-authorization. M7 does not provide cloud service, GUI, or hosted dashboard. M7 HMAC key handling is local/dev only, not production KMS.

## Next Milestone Suggestion

M8 should add portable audit bundle export and import so a reviewer can reproduce policy, ledger, receipts, and replay verification outside the original project directory.
