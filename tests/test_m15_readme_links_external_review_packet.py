from __future__ import annotations

from pathlib import Path


def test_m15_readme_links_external_review_packet() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/external_review/" in readme
    assert "examples/external_review/" in readme
    assert "scripts/generate_external_review_packet.py" in readme
    assert "scripts/validate_external_review_packet.py" in readme
    assert "M15_PACKET_PREPARED_FOR_EXTERNAL_REVIEW" in readme
    assert "M15_EXTERNAL_REVIEW_NOT_YET_COMPLETE" in readme
