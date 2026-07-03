from __future__ import annotations

from gcr.report_generator import generate_markdown_report, generate_report_summary
from gcr_agent import GovernedAgent
from gcr_agent.agent_runtime import GovernedAgentRuntime
from gcr_agent.llm_client import FakeLLMClient


def test_real_agent_report_includes_agent_runs(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    GovernedAgentRuntime(
        root=tmp_path,
        governed_agent=GovernedAgent(root_path=tmp_path, ledger_path=ledger_path),
        llm_client=FakeLLMClient(),
    ).run_task("Read README.md")

    summary = generate_report_summary(ledger_path=ledger_path)
    markdown = generate_markdown_report(summary)

    assert summary["agent_runs"]["total_agent_runs"] == 1
    assert "## Agent Runs" in markdown
