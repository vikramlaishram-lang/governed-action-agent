from __future__ import annotations

from pathlib import Path


def test_m14_docs_include_claim_boundaries() -> None:
    doc = Path("docs/PUBLIC_CLAIMS_AND_LIMITATIONS.md").read_text(encoding="utf-8")

    assert "The project demonstrates a local governed action agent loop." in doc
    assert "The agent separates proposal from authorization." in doc
    assert "The agent can generate a local static receipt viewer." in doc
    assert "Do not claim production safety." in doc
    assert "Do not claim real GitHub write integration." in doc
    assert "Do not claim cloud-hosted dashboard." in doc
