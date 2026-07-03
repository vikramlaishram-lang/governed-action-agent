from __future__ import annotations

import json

from gcr.viewer_generator import write_viewer_bundle
from m13_viewer_fixture import sample_viewer_summary


def test_m13_viewer_data_json_valid(tmp_path) -> None:
    write_viewer_bundle(summary=sample_viewer_summary(), output_dir=tmp_path)
    data = json.loads((tmp_path / "viewer_data.json").read_text(encoding="utf-8"))

    assert data["schema_version"] == "governed_agent_viewer_v0.1"
    assert data["ledger"]["record_count"] == 5
