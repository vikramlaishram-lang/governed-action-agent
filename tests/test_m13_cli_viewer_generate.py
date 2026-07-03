from __future__ import annotations

from gcr_agent.cli import main


def test_m13_cli_viewer_generate(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")

    assert main(["init"]) == 0
    assert main(["ask", "Read README.md"]) == 0
    assert main(["viewer"]) == 0
    output = capsys.readouterr().out

    assert "VIEWER_GENERATED: true" in output
    assert "LEDGER_VALID: true" in output
    assert "TOTAL_RECORDS: 1" in output
    assert (tmp_path / ".governed-agent" / "viewer" / "index.html").exists()
    assert (tmp_path / ".governed-agent" / "viewer" / "viewer_data.json").exists()
