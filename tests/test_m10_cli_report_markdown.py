from __future__ import annotations

from gcr_agent.cli import main


def test_m10_cli_report_markdown(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("# Temp\n", encoding="utf-8")
    assert main(["init"]) == 0
    assert main(["ask", "Read README.md"]) == 0
    capsys.readouterr()
    assert main(["report", "--format", "markdown"]) == 0
    output = capsys.readouterr().out

    assert "# Governed Action Agent Report" in output
    assert (tmp_path / ".governed-agent" / "reports" / "governed_agent_report.md").exists()
    assert (tmp_path / ".governed-agent" / "reports" / "governed_agent_report.json").exists()
