# Real Agent Core

## Purpose

The previous release proved the governance layer: proposal objects, policy decisions, receipts, ledgers, reports, viewers, and public reproduction. This layer adds an actual agent runtime.

The LLM/planner proposes actions. The governance layer authorizes or blocks them. The model cannot self-authorize. The model cannot directly execute tools.

## Architecture

```text
user task
-> repo context collector
-> LLM/planner client
-> structured model proposal
-> proposal normalization
-> existing governed agent path
-> policy / verifier / reviewer checks
-> bounded local tool or denial
-> receipt
-> ledger
-> report/viewer
```

## CLI Usage

```bash
PYTHONPATH=src python -m gcr_agent.cli agent "Inspect this repo and propose a README improvement"
PYTHONPATH=src python -m gcr_agent.cli agent "Read README.md" --fake-llm --trace
```

Normal output includes governance decision, consequence class, receipt id, ledger append status, and real repo modification status.

## Fake LLM Mode

Tests and demos use `FakeLLMClient`. It deterministically maps tasks to structured JSON proposals for safe reads, secret reads, README improvement proposals, production deploy requests, and self-authorization attacks.

## Optional Real LLM Provider Boundary

`OpenAICompatibleLLMClient` can be wired through:

```text
GAA_LLM_BASE_URL
GAA_LLM_API_KEY
GAA_LLM_MODEL
```

This path is optional and not used by tests. Model output remains untrusted.

## Security Limits

- Model output cannot set `decision`.
- Model output cannot set `execution_status`.
- Model output cannot authorize itself.
- Model-generated actions still pass through policy and verifier rules.
- Secret access remains denied.
- Production deployment remains review-required or blocked.
- Sandboxed code proposals do not modify the real repository.

## What Is Now Real

- the agent observes repository context
- the agent calls an LLM/planner interface
- the model emits structured proposals
- the runtime normalizes those proposals into governed actions
- receipts include an `agent_run` section
- reports summarize agent runs

## What Remains Bounded

The runtime is still local evaluation only. It does not perform real deployment, write to GitHub, apply patches to the real repo, access secrets, or run arbitrary shell commands.
