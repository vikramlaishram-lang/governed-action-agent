# Reviewer Instructions

## Purpose

Use this packet to independently reproduce the governed-action-agent local release and record what you observed.

## What You Are Being Asked To Reproduce

You are asked to run the tests, public demo, release package validation, external review packet validation, and inspect the report/viewer artifacts.

## System Requirements

Use Python 3.12 or newer, Git, and a local shell. Network is needed only for the initial `git clone`.

## Fresh Clone Steps

```bash
git clone https://github.com/vikramlaishram-lang/governed-action-agent
cd governed-action-agent
git checkout v0.14.0-local-release
```

If you check out a later tag or branch, record the exact commit and tag in the attestation form.

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

```bash
python -m pip install -e .
```

## Test Command

```bash
PYTHONPATH=src python -m pytest -q
```

## Public Demo Command

```bash
PYTHONPATH=src python scripts/run_public_demo.py
```

## Release Validation Command

```bash
PYTHONPATH=src python scripts/validate_release_package.py
```

## External Review Packet Validation Command

```bash
PYTHONPATH=src python scripts/validate_external_review_packet.py
```

## Optional Viewer Inspection

Run the public demo with `--keep-artifacts` and open the generated viewer files, or inspect `examples/sample_viewer/index.html` and `examples/sample_viewer/viewer_data.json`.

## Expected Outputs

Compare observed output against `docs/external_review/EXPECTED_OUTPUTS.md`.

## How To Record Pass/Fail

Record each command, exit code, observed output, and whether it matched expected output.

## How To Fill Attestation

Use `docs/external_review/REVIEWER_ATTESTATION_FORM.md`. Fill in reviewer identity, environment, commit, tag, commands, outputs, reproduced claims, failed items, notes, and signature/name.

## How To Report Failures

Use `docs/external_review/FAILURE_LOG_TEMPLATE.md` and add tracked issues to `docs/external_review/EXTERNAL_FINDINGS_LEDGER.md`.

## Scope Boundaries

This review checks local reproduction only. It does not validate production safety, legal compliance, complete security, real deployment, or real GitHub write behavior.

## What Not To Infer

Do not infer that an external audit is complete. Do not infer production readiness. Do not infer legal/compliance certification.
