# Deployment Plan

## Product

Governed Action Agent is a local governed action-agent prototype for AI coding and release workflows.

It separates proposal from execution authority. The agent may propose an action, but authorization is decided by policy, reviewer scope, and verifier rules. Each decision is recorded as a receipt and appended to a replay-verifiable ledger.

## Current Deployment Status

Current approved deployment mode:

```text
LOCAL_EVALUATION_ONLY
```

Current release tag:

```text
v0.15.0-external-review-packet
```

This release is ready for local evaluation, public demo, and independent reproduction.

It is not approved for production deployment.

```text
DEPLOYMENT_MODE: LOCAL_EVALUATION_ONLY
NEXT_SAFE_MODE: CONTROLLED_LOCAL_PILOT_READ_ONLY
PRODUCTION_DEPLOYMENT: NOT_APPROVED
```

## What Runs

The local deployment includes:

- CLI: `gaa`
- governed request handling
- local tool boundary
- policy engine
- reviewer token validation
- reviewer identity registry
- receipt ledger
- HMAC verification path
- replay verifier
- release-readiness report generator
- local static receipt viewer
- sandboxed code-change proposal generator
- public demo script
- external review packet

## What It Is Allowed To Do

In the current deployment mode, the system may:

- read allowed local files
- deny secret-file access
- classify consequential requests
- request review for sensitive actions
- validate scoped reviewer approvals
- generate sandboxed code-change diffs
- inspect fixture or read-only PR evidence
- append local receipts
- verify the local ledger
- generate Markdown/JSON reports
- generate a local static receipt viewer

## What It Is Not Allowed To Do

In the current deployment mode, the system must not:

- perform real production deployment
- write to GitHub
- create pull requests
- merge pull requests
- dispatch workflows
- apply patches to the real repository
- edit real project files through the agent
- access secrets
- run arbitrary shell commands
- claim production safety
- claim legal or compliance certification
- claim external audit completion

## Deployment Target

The current deployment target is a developer or evaluator machine.

Supported deployment surface:

```text
local clone
local Python environment
local CLI
local demo project
local ledger/report/viewer artifacts
```

No hosted service is required.

No cloud account is required.

No external API is required for the public demo.

## Installation

Fresh evaluator path:

```bash
git clone https://github.com/vikramlaishram-lang/governed-action-agent
cd governed-action-agent
git checkout v0.15.0-external-review-packet
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install:

```bash
python -m pip install -e .
```

Validate:

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_public_demo.py
PYTHONPATH=src python scripts/validate_release_package.py
PYTHONPATH=src python scripts/validate_external_review_packet.py
```

## Public Demo Deployment

The public demo is the primary deployment proof.

Run:

```bash
PYTHONPATH=src python scripts/run_public_demo.py
```

Expected proof lines:

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

## Local Project Deployment

For a local project:

```bash
PYTHONPATH=src python -m gcr_agent.cli init
PYTHONPATH=src python -m gcr_agent.cli status
PYTHONPATH=src python -m gcr_agent.cli ask "Read README.md"
PYTHONPATH=src python -m gcr_agent.cli ask "Read .env"
PYTHONPATH=src python -m gcr_agent.cli propose-change "Update README.md with governed agent summary"
PYTHONPATH=src python -m gcr_agent.cli report
PYTHONPATH=src python -m gcr_agent.cli viewer
PYTHONPATH=src python -m gcr_agent.cli verify-ledger
```

Generated local artifacts:

```text
.governed-agent/config.json
.governed-agent/policy.json
.governed-agent/reviewers.json
.governed-agent/ledger.jsonl
.governed-agent/reports/
.governed-agent/viewer/
.governed-agent/sandbox/
```

## Data Boundary

The system may process only local project files that are allowed by the local tool boundary.

Secret-like files are denied, including:

```text
.env
secrets.json
credentials.json
id_rsa
id_ed25519
```

The public demo must not expose secrets.

The viewer and report must not expose:

```text
HMAC keys
GitHub tokens
authorization headers
bearer tokens
private keys
full patch text
secret file contents
```

## Key Management

Default local evaluation can run in unkeyed hash-chain mode.

For stronger local verification, use HMAC mode.

HMAC keys must be provided through environment variables and must not be committed.

Example:

```bash
set GAA_LEDGER_HMAC_KEY=local-dev-only-key
```

or on macOS/Linux:

```bash
export GAA_LEDGER_HMAC_KEY=local-dev-only-key
```

The ledger may store `key_id`, but must not store the HMAC secret.

## Reviewer Authority

Reviewer identity is local.

Reviewer registry:

```text
.governed-agent/reviewers.json
```

A reviewer approval is valid only if:

- reviewer exists in registry
- reviewer status is `ACTIVE`
- reviewer role is authorized
- reviewer scope matches the action
- reviewer identity hash matches
- token is bound to the proposal/action
- token is not expired
- action is overridable

Reviewer approval cannot override:

```text
CONSTITUTIONAL_VIOLATION
SECRET_ACCESS
IRREVERSIBLE_DELETE
```

## Operational Use

Approved current use:

```text
local evaluation
demo reproduction
reviewer reproduction
read-only pilot exploration
sandboxed proposal review
```

Not approved:

```text
production enforcement
real deployment approval
automated merge
GitHub write automation
regulated audit reliance
security certification
```

## Deployment Success Criteria

A local deployment is successful if:

```text
tests pass
public demo passes
release validation passes
external review packet validation passes
ledger replay verifies
report is generated
viewer is generated
secret exposure check is false
real repo remains unchanged during sandboxed code proposal
```

## Failure Handling

If any validation fails:

1. Stop.
2. Do not claim deployment success.
3. Record command, expected output, observed output, exit code, and traceback.
4. Use the failure log template in:

```text
docs/external_review/FAILURE_LOG_TEMPLATE.md
```

5. Do not proceed to pilot use until the failure is explained or fixed.

## Current Deployment Decision

The current release is approved for:

```text
LOCAL_EVALUATION_ONLY
```

The current release is not approved for:

```text
PRODUCTION_DEPLOYMENT
CONTROLLED_ENFORCEMENT
REAL_GITHUB_WRITE_MODE
REAL_PATCH_APPLICATION
```

## Next Allowed Deployment Step

The next allowed step is:

```text
CONTROLLED_LOCAL_PILOT_READ_ONLY
```

Entry conditions:

- at least one clean local reproduction
- no failed public demo checks
- no secret exposure
- ledger replay valid
- reviewer understands limitations
- target repo owner accepts read-only/sandbox-only boundary

Allowed in that pilot:

- read allowed files
- inspect repository state
- inspect PR evidence read-only
- generate sandboxed diffs
- generate receipts
- generate reports/viewer

Still forbidden:

- applying code changes
- pushing commits
- creating PRs
- commenting on GitHub
- merging
- deployment
- modifying production state

## Final Boundary

Governed Action Agent is currently deployable as a local evaluation and controlled read-only pilot tool.

It is not yet a production deployment system.
