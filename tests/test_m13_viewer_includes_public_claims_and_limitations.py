from __future__ import annotations

from gcr.viewer_generator import generate_viewer_html
from m13_viewer_fixture import sample_viewer_summary


def test_m13_viewer_includes_public_claims_and_limitations() -> None:
    html = generate_viewer_html(sample_viewer_summary())

    assert "Public Claims Allowed by Evidence" in html
    assert "Limitations / Non-Claims" in html
    assert "verifiable local receipt ledger" in html
    assert "does not prove production safety" in html
