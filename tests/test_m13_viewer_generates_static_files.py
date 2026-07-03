from __future__ import annotations

from gcr.viewer_generator import generate_viewer_html, write_viewer_bundle
from m13_viewer_fixture import sample_viewer_summary


def test_m13_viewer_generates_static_files(tmp_path) -> None:
    written = write_viewer_bundle(summary=sample_viewer_summary(), output_dir=tmp_path)

    assert written["viewer_generated"] is True
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "viewer_data.json").exists()


def test_m13_viewer_html_contains_required_sections() -> None:
    html = generate_viewer_html(sample_viewer_summary())

    assert "Governed Action Agent Receipt Viewer" in html
    for section in [
        "Project Summary",
        "Ledger Integrity",
        "Decision Summary",
        "Violations",
        "Reviewer Identity",
        "Review-Approved Actions",
        "Denied Actions",
        "Request-Review Actions",
        "GitHub PR Evidence",
        "Code Change Proposals",
        "Public Claims Allowed by Evidence",
        "Limitations / Non-Claims",
        "Latest Hash",
    ]:
        assert section in html
