from __future__ import annotations

from gcr.viewer_generator import generate_viewer_html
from m13_viewer_fixture import sample_viewer_summary


def test_m13_viewer_renders_code_change_proposals() -> None:
    html = generate_viewer_html(sample_viewer_summary())

    assert "Code Change Proposals" in html
    assert "code-change-1" in html
    assert "sha256:diff" in html
    assert "Governed Action Agent Note" not in html
