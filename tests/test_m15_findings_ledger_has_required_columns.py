from __future__ import annotations

from pathlib import Path


def test_m15_findings_ledger_has_required_columns() -> None:
    text = Path("docs/external_review/EXTERNAL_FINDINGS_LEDGER.md").read_text(encoding="utf-8")

    for column in [
        "Finding ID",
        "Date",
        "Reviewer",
        "Commit",
        "Severity",
        "Area",
        "Expected",
        "Observed",
        "Reproduction steps",
        "Status",
        "Resolution commit",
        "Notes",
    ]:
        assert column in text
