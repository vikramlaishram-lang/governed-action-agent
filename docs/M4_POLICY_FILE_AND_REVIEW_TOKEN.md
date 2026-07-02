# M4 Policy File And Review Token

## Purpose

M4 adds configurable policy files and scoped human review tokens. It proves that a `REQUEST_REVIEW` action can become `ALLOW` only when a valid, scoped, unexpired reviewer token matches the exact proposal.

The core invariant remains: the agent may propose, and the agent may not self-authorize execution.

## What Changed From M3

M3 added controlled local tools. M4 keeps that boundary and adds:

- `configs/policy.default.json`
- policy loading and canonical hashing
- `ReviewToken`
- review-token verification
- reviewer-role checks
- two-phase `prepare_request` and `evaluate_proposal`
- simulated execution for review-approved production changes

## Policy File Format

The default policy uses JSON schema version `policy_v0.1`. Each consequence class maps to a rule with:

- `decision`
- `review_required`
- `review_can_override`
- optional `allowed_reviewer_roles` when override is allowed

## Review Token Format

Review tokens use schema version `review_token_v0.1` and bind approval to:

- exact `proposal_id`
- exact normalized action
- exact consequence class
- approval scope
- reviewer identity and role
- expiration timestamp

## Approval Rules

A token is valid only when it is approved, unexpired, scoped to the same consequence class, issued by an allowed reviewer role, and bound to the exact proposal and normalized action.

## What Tokens Can Approve

Tokens can approve policy rules where `review_can_override` is true, such as `PRODUCTION_STATE_CHANGE`, when the reviewer role is allowed by policy.

## What Tokens Can Never Approve

Review tokens can never approve:

- `CONSTITUTIONAL_VIOLATION`
- `SECRET_ACCESS`
- `IRREVERSIBLE_DELETE`
- real production deployment
- arbitrary shell commands
- network calls

## Demo Command

```bash
PYTHONPATH=src python demo/run_m4_policy_review_token_demo.py
```

## Test Command

```bash
PYTHONPATH=src python -m pytest -q
```

## Limitations

M4 does not perform real production deployment. M4 only simulates review-approved production changes. M4 does not implement cryptographic signatures for approval tokens yet. M4 does not implement identity provider / SSO. M4 does not implement a persistent token ledger yet.

## Next Milestone Suggestion

M5 should add signed review tokens and an append-only authorization ledger so reviewer approvals can be independently verified and audited across runs.
