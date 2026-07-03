from __future__ import annotations

from gcr_agent import GovernedAgent
from gcr_agent.agent_runtime import GovernedAgentRuntime
from gcr_agent.llm_client import FakeLLMClient


def test_real_agent_secret_read_is_denied(tmp_path) -> None:
    result = GovernedAgentRuntime(
        root=tmp_path,
        governed_agent=GovernedAgent(root_path=tmp_path, ledger_path=tmp_path / "ledger.jsonl"),
        llm_client=FakeLLMClient(),
    ).run_task("Read .env")

    assert result["decision"] == "DENY"
    assert result["consequence_class"] == "SECRET_ACCESS"
