# Reviewer Attestation Form

Reviewer name:
Reviewer affiliation:
Reviewer email/contact:
Review date:
Repository URL:
Commit hash reviewed:
Tag/branch reviewed:
Operating system:
Python version:
Installation method:
Commands run:

Test result:
- Full pytest result:
- Public demo result:
- Release validation result:
- External review packet validation result:

Observed public demo output:
Observed release validation output:
Observed external review packet validation output:

Reproduced claims:
- [ ] Local governed action-agent loop runs.
- [ ] Safe read is allowed.
- [ ] Secret access is denied.
- [ ] Production deploy requires review when no reviewer approval is provided.
- [ ] Self-authorization is detected as CONSTITUTIONAL_VIOLATION.
- [ ] Sandboxed code-change proposal does not modify the real repo.
- [ ] Valid reviewer approval works within local scoped reviewer identity rules.
- [ ] Ledger replay verifies.
- [ ] Report generation succeeds.
- [ ] Viewer generation succeeds.
- [ ] Generated artifacts do not expose secrets in the demo.

Not reproduced / failed items:
Open findings:
Reviewer notes:

Attestation statement:
I independently ran the reproduction steps above and recorded the observed results truthfully. This attestation does not certify production safety, legal compliance, or complete security.

Signature/name:
Date:
