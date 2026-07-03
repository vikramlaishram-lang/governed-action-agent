from __future__ import annotations

import subprocess
import sys


def test_m15_generate_external_review_packet(tmp_path) -> None:
    output_dir = tmp_path / "packet"
    result = subprocess.run(
        [sys.executable, "scripts/generate_external_review_packet.py", "--output-dir", str(output_dir)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "EXTERNAL_REVIEW_PACKET_GENERATED: true" in result.stdout
    assert "PACKET_INDEX_READY: true" in result.stdout
    assert (output_dir / "PACKET_INDEX.md").exists()
    assert (output_dir / "docs" / "external_review" / "REVIEWER_INSTRUCTIONS.md").exists()
    assert (output_dir / "examples" / "external_review" / "expected_public_demo_output.txt").exists()
