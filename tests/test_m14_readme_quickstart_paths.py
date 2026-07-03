from __future__ import annotations

from pathlib import Path


def test_m14_readme_quickstart_paths() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "scripts/run_public_demo.py" in readme
    assert "scripts/validate_release_package.py" in readme
    assert "docs/EVALUATOR_QUICKSTART.md" in readme
    assert "PUBLIC_CLAIMS_AND_LIMITATIONS.md" in readme
    assert "The agent may propose. The agent may not self-authorize execution." in readme
