from __future__ import annotations

from gcr.viewer_generator import write_viewer_bundle
from m13_viewer_fixture import sample_viewer_summary


def test_m13_viewer_does_not_expose_tokens_or_secrets(tmp_path) -> None:
    write_viewer_bundle(summary=sample_viewer_summary(), output_dir=tmp_path)
    combined = (
        (tmp_path / "index.html").read_text(encoding="utf-8")
        + (tmp_path / "viewer_data.json").read_text(encoding="utf-8")
    )

    for forbidden in [
        "super-secret-key",
        "ghp_not_allowed",
        "Bearer secret",
        "do not persist this patch",
        "Governed Action Agent Note",
        "full patch text",
        "SECRET=do-not-expose",
    ]:
        assert forbidden not in combined

    assert "sha256:diff" in combined
    assert "sha256:evidence" in combined
