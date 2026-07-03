from __future__ import annotations

from pathlib import Path


def test_m15_review_scope_does_not_claim_external_audit_complete() -> None:
    scope = Path("docs/external_review/REVIEW_SCOPE_AND_LIMITATIONS.md").read_text(encoding="utf-8")
    docs = "\n".join(path.read_text(encoding="utf-8") for path in Path("docs/external_review").glob("*.md"))
    lowered = docs.lower()

    assert "This packet prepares external reproduction. It is not itself external validation." in scope
    assert "external audit completed" not in lowered
    assert "production-safe" not in lowered
    assert "legally certified" not in lowered
    assert "compliance certified" not in lowered
