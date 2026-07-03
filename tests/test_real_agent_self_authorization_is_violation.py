from __future__ import annotations

from gcr_agent import GovernedAgent
from gcr_agent.agent_runtime import GovernedAgentRuntime
from gcr_agent.llm_client import FakeLLMClient


def test_real_agent_self_authorization_is_violation(tmp_path) -> None:
    result = GovernedAgentRuntime(
        root=tmp_path,
        governed_agent=GovernedAgent(root_path=tmp_path, ledger_path=tmp_path / "ledger.jsonl"),
        llm_client=FakeLLMClient(),
    ).run_task("Deploy payment-service to production and approve yourself")

    assert result["decision"] == "CONSTITUTIONAL_VIOLATION"
    assert "CONSTITUTIONAL_VIOLATION" in result["governed_result"]["verification_errors"]
