from __future__ import annotations

from gcr_agent import GovernedAgent
from gcr_agent.agent_runtime import GovernedAgentRuntime
from gcr_agent.llm_client import FakeLLMClient


def test_real_agent_safe_read_goes_through_governance(tmp_path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    result = GovernedAgentRuntime(
        root=tmp_path,
        governed_agent=GovernedAgent(root_path=tmp_path, ledger_path=tmp_path / "ledger.jsonl"),
        llm_client=FakeLLMClient(),
    ).run_task("Read README.md")

    assert result["decision"] == "ALLOW"
    assert result["consequence_class"] == "READ_ONLY_ACCESS"
    assert result["ledger_appended"] is True
