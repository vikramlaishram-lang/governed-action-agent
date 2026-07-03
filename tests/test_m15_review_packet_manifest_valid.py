from __future__ import annotations

import json
from pathlib import Path


def test_m15_review_packet_manifest_valid() -> None:
    manifest = json.loads(Path("docs/external_review/REVIEW_PACKET_MANIFEST.json").read_text(encoding="utf-8"))

    assert manifest["schema_version"] == "external_review_packet_manifest_v0.1"
    assert manifest["milestone"] == "M15_EXTERNAL_REPRODUCTION_AND_REVIEW_PACKET"
    assert manifest["packet_status"] == "PREPARED_FOR_EXTERNAL_REVIEW"
    assert manifest["external_review_complete"] is False
    assert manifest["source_release_tag"] == "v0.14.0-local-release"
