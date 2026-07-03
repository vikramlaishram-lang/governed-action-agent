from __future__ import annotations

from scripts.clean_demo_artifacts import clean_demo_artifacts


def test_m14_clean_demo_artifacts(tmp_path) -> None:
    for directory in [
        tmp_path / ".governed-agent" / "public-demo",
        tmp_path / ".governed-agent" / "demo-output",
        tmp_path / "tmp_public_demo",
        tmp_path / "examples" / "tmp",
    ]:
        directory.mkdir(parents=True)
        (directory / "artifact.txt").write_text("demo", encoding="utf-8")

    for protected in ["src", "tests", "docs", "schemas", "configs"]:
        (tmp_path / protected).mkdir()
        (tmp_path / protected / "keep.txt").write_text("keep", encoding="utf-8")

    clean_demo_artifacts(tmp_path)

    assert not (tmp_path / ".governed-agent" / "public-demo").exists()
    assert not (tmp_path / ".governed-agent" / "demo-output").exists()
    assert not (tmp_path / "tmp_public_demo").exists()
    assert not (tmp_path / "examples" / "tmp").exists()
    for protected in ["src", "tests", "docs", "schemas", "configs"]:
        assert (tmp_path / protected / "keep.txt").exists()
