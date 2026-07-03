from __future__ import annotations

from gcr.viewer_generator import generate_viewer_html
from m13_viewer_fixture import sample_viewer_summary


def test_m13_viewer_renders_reviewer_identity() -> None:
    html = generate_viewer_html(sample_viewer_summary())

    assert "Reviewer Identity" in html
    assert "local-reviewer-registry" in html
    assert "alice-release" in html
