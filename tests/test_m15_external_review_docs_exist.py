from __future__ import annotations

from pathlib import Path


def test_m15_external_review_docs_exist() -> None:
    for path in [
        "docs/external_review/README.md",
        "docs/external_review/REVIEWER_INSTRUCTIONS.md",
        "docs/external_review/FRESH_CLONE_REPRODUCTION_CHECKLIST.md",
        "docs/external_review/EXPECTED_OUTPUTS.md",
        "docs/external_review/REVIEWER_ATTESTATION_FORM.md",
        "docs/external_review/EXTERNAL_FINDINGS_LEDGER.md",
        "docs/external_review/FAILURE_LOG_TEMPLATE.md",
        "docs/external_review/REVIEW_SCOPE_AND_LIMITATIONS.md",
        "docs/external_review/REVIEW_PACKET_MANIFEST.json",
    ]:
        assert Path(path).exists()
