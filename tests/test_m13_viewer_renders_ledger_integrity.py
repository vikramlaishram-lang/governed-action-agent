from __future__ import annotations

from gcr.viewer_generator import generate_viewer_html
from m13_viewer_fixture import sample_viewer_summary


def test_m13_viewer_renders_ledger_integrity() -> None:
    html = generate_viewer_html(sample_viewer_summary())

    assert "Ledger valid" in html
    assert "true" in html
    assert "Record count" in html
    assert "Latest hash present" in html
    assert "HMAC_SHA256_V1" in html
