from __future__ import annotations

from gcr.viewer_generator import generate_viewer_html
from m13_viewer_fixture import sample_viewer_summary


def test_m13_viewer_renders_decision_counts() -> None:
    html = generate_viewer_html(sample_viewer_summary())

    assert "ALLOW" in html
    assert "DENY" in html
    assert "REQUEST_REVIEW" in html
    assert "BLOCKED" in html
