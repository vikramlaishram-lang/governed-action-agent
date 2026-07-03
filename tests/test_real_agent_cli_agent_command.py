from __future__ import annotations

from gcr_agent.cli import main


def test_real_agent_cli_agent_command(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")

    assert main(["init"]) == 0
    assert main(["agent", "Read README.md", "--fake-llm", "--trace"]) == 0
    output = capsys.readouterr().out

    assert "AGENT_RUN: true" in output
    assert "MODEL_PROPOSAL_PARSED: true" in output
    assert "GOVERNANCE_DECISION: ALLOW" in output
    assert "REAL_REPO_MODIFIED: false" in output
    assert "TRACE_ID: agent_trace_" in output
