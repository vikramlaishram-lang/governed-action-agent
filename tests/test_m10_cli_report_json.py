from __future__ import annotations

import json

from gcr_agent.cli import main


def test_m10_cli_report_json(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("# Temp\n", encoding="utf-8")
    assert main(["init"]) == 0
    assert main(["ask", "Read README.md"]) == 0
    capsys.readouterr()
    assert main(["report", "--format", "json"]) == 0
    summary = json.loads(capsys.readouterr().out)

    assert summary["schema_version"] == "governed_agent_report_v0.1"
    assert summary["ledger"]["record_count"] == 1
