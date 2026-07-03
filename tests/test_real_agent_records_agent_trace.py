from __future__ import annotations

from gcr_agent import GovernedAgent
from gcr_agent.agent_runtime import GovernedAgentRuntime
from gcr_agent.llm_client import FakeLLMClient


def test_real_agent_records_agent_trace(tmp_path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    result = GovernedAgentRuntime(
        root=tmp_path,
        governed_agent=GovernedAgent(root_path=tmp_path, ledger_path=tmp_path / "ledger.jsonl"),
        llm_client=FakeLLMClient(),
    ).run_task("Read README.md")

    assert result["trace"]["trace_id"].startswith("agent_trace_")
    assert result["governed_result"]["receipt"]["agent_run"]["trace_id"] == result["trace"]["trace_id"]
