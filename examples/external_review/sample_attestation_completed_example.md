# Sample Attestation Completed Example

SAMPLE ONLY - NOT A REAL EXTERNAL REVIEW

Reviewer name: Example Reviewer
Reviewer affiliation: Example Lab
Reviewer email/contact: reviewer@example.invalid
Review date: 2026-07-03
Repository URL: https://github.com/vikramlaishram-lang/governed-action-agent
Commit hash reviewed: example-commit
Tag/branch reviewed: v0.14.0-local-release
Operating system: ExampleOS
Python version: 3.12.x
Installation method: python -m pip install -e .
Commands run: pytest, public demo, release validation, packet validation

Test result:
- Full pytest result: passed in sample
- Public demo result: matched expected sample
- Release validation result: matched expected sample
- External review packet validation result: matched expected sample

Observed public demo output: see attached sample log
Observed release validation output: see attached sample log
Observed external review packet validation output: see attached sample log

Reproduced claims:
- [x] Local governed action-agent loop runs.
- [x] Safe read is allowed.
- [x] Secret access is denied.
- [x] Production deploy requires review when no reviewer approval is provided.
- [x] Self-authorization is detected as CONSTITUTIONAL_VIOLATION.
- [x] Sandboxed code-change proposal does not modify the real repo.
- [x] Valid reviewer approval works within local scoped reviewer identity rules.
- [x] Ledger replay verifies.
- [x] Report generation succeeds.
- [x] Viewer generation succeeds.
- [x] Generated artifacts do not expose secrets in the demo.

Not reproduced / failed items: sample none
Open findings: sample none
Reviewer notes: sample only

Attestation statement:
I independently ran the reproduction steps above and recorded the observed results truthfully. This attestation does not certify production safety, legal compliance, or complete security.

Signature/name: Example Reviewer
Date: 2026-07-03
