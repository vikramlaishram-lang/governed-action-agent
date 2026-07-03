# M12 Reviewer Identity Hardening

## Purpose

M12 hardens reviewer authority so a review token is accepted only when the reviewer identity is known, active, scoped, role-authorized, and bound to the exact proposal/action.

## What Changed From M11

M11 added sandboxed code-change proposals. M12 adds a local reviewer authority registry, reviewer identity manifests, review token v0.2, identity hash binding, issuer binding, and reviewer identity fields in receipts and reports.

## Reviewer Identity Manifest

Each reviewer has an identity manifest with reviewer id, display name, status, roles, allowed scopes, creation time, and deterministic identity hash.

## Reviewer Authority Registry

The local registry lives in `configs/reviewers.default.json` or `.governed-agent/reviewers.json` for CLI projects. It lists reviewers and registry issuer metadata.

## Review Token v0.2

Review token v0.2 adds `reviewer_identity_hash` and `issuer_id`. When a reviewer registry is configured, v0.2 is required.

## Identity Hash And Issuer Binding

The reviewer identity hash is computed over canonical JSON excluding `identity_hash`. Tokens must match the registry issuer and identity hash.

## Status, Scope, And Role Checks

Only ACTIVE reviewers can approve. The token role must exist in reviewer roles. The approval scope must be in reviewer allowed scopes and must match the proposal consequence class.

## What Tokens Can Approve

Tokens may approve only policy-overridable review-required actions within reviewer scope and role.

## What Tokens Can Never Approve

Tokens can never override constitutional violations, secret access, irreversible delete, real deployment restrictions, or self-authorization.

## CLI Behavior

```bash
PYTHONPATH=src python -m gcr_agent.cli init
PYTHONPATH=src python -m gcr_agent.cli status
PYTHONPATH=src python -m gcr_agent.cli reviewers
```

## Receipt And Report Fields

Receipts include reviewer identity verification status, errors, identity hash, registry version, and issuer id. Reports summarize verified reviewer-approved actions and reviewer identity errors.

## Demo Command

```bash
PYTHONPATH=src python demo/run_m12_reviewer_identity_hardening_demo.py
```

## Test Command

```bash
PYTHONPATH=src python -m pytest -q
```

## Current Limitations

M12 uses a local reviewer registry. M12 does not implement SSO/OIDC. M12 does not prove legal identity. M12 does not provide production IAM. M12 does not create remote audit. M12 does not permit real production deployment. M12 does not allow reviewer tokens to override constitutional violations.

## Next Milestone Suggestion

M13 should add a local static receipt viewer that renders ledger/report evidence without adding execution authority.
