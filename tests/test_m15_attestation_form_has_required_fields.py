from __future__ import annotations

from pathlib import Path


def test_m15_attestation_form_has_required_fields() -> None:
    text = Path("docs/external_review/REVIEWER_ATTESTATION_FORM.md").read_text(encoding="utf-8")

    for field in [
        "Reviewer name:",
        "Commit hash reviewed:",
        "Commands run:",
        "Reproduced claims:",
        "Not reproduced / failed items:",
        "Attestation statement:",
    ]:
        assert field in text
