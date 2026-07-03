# M15 External Reproduction And Review Packet

## Purpose

M15 creates an external reproduction and review packet so an independent reviewer can clone the repo, run the release locally, compare expected outputs, record pass/fail findings, and attest to what was reproduced.

## What Changed From M14

M14 packaged a local release and public demo. M15 adds external reviewer instructions, expected outputs, a fresh-clone checklist, attestation form, findings ledger, failure log template, review scope, manifest, packet generator, and packet validator.

## Packet Contents

- `docs/external_review/README.md`
- `docs/external_review/REVIEWER_INSTRUCTIONS.md`
- `docs/external_review/FRESH_CLONE_REPRODUCTION_CHECKLIST.md`
- `docs/external_review/EXPECTED_OUTPUTS.md`
- `docs/external_review/REVIEWER_ATTESTATION_FORM.md`
- `docs/external_review/EXTERNAL_FINDINGS_LEDGER.md`
- `docs/external_review/FAILURE_LOG_TEMPLATE.md`
- `docs/external_review/REVIEW_SCOPE_AND_LIMITATIONS.md`
- `docs/external_review/REVIEW_PACKET_MANIFEST.json`
- `examples/external_review/`

## Reviewer Workflow

The reviewer clones the public repository, checks out the documented tag or records a later commit/tag, creates a virtual environment, installs locally, runs tests, runs the public demo, runs release validation, runs packet validation, inspects report/viewer artifacts, and records results.

## Expected Outputs

Expected outputs live in `docs/external_review/EXPECTED_OUTPUTS.md` and `examples/external_review/`.

## Attestation Process

Reviewers fill out `docs/external_review/REVIEWER_ATTESTATION_FORM.md` with environment, commit, tag, commands, observed outputs, reproduced claims, failures, notes, and signature/name.

## Findings Ledger Process

Findings are recorded in `docs/external_review/EXTERNAL_FINDINGS_LEDGER.md` with severity, status, expected behavior, observed behavior, reproduction steps, and resolution commit.

## Failure Reporting

Failures should be captured with `docs/external_review/FAILURE_LOG_TEMPLATE.md`.

## Validation Script

```bash
PYTHONPATH=src python scripts/validate_external_review_packet.py
```

## Packet Generation Script

```bash
PYTHONPATH=src python scripts/generate_external_review_packet.py
```

## What M15 Proves

M15 proves that the external reproduction packet exists, is structured, has expected outputs, has attestation and findings templates, has scope boundaries, and can be validated locally.

## What M15 Does Not Prove

M15 does not add new agent authority. M15 does not add enforcement. M15 does not add cloud hosting. M15 does not claim external validation has already happened. M15 does not prove production readiness, complete security, legal/compliance certification, real deployment control, or real GitHub write integration.

## Current Status

M15_PACKET_PREPARED_FOR_EXTERNAL_REVIEW

M15_EXTERNAL_REVIEW_NOT_YET_COMPLETE

M15 prepares the evidence packet for independent reproduction.
M15 does not itself constitute independent reproduction.
M15 cannot be called externally validated until a reviewer completes the attestation form.

## Next Milestone Suggestion

M16 should record the first independent external reviewer attestation and findings response without expanding agent execution authority.
