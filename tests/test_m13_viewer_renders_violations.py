from __future__ import annotations

from gcr.viewer_generator import generate_viewer_html
from m13_viewer_fixture import sample_viewer_summary


def test_m13_viewer_renders_violations() -> None:
    html = generate_viewer_html(sample_viewer_summary())

    assert "Constitutional violations" in html
    assert "Execution authorization violations" in html
