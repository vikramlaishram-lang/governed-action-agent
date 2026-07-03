from __future__ import annotations

from gcr_agent import GovernedAgent
from gcr_agent.agent_runtime import GovernedAgentRuntime
from gcr_agent.llm_client import FakeLLMClient


def test_real_agent_code_change_generates_sandbox_diff(tmp_path) -> None:
    readme = tmp_path / "README.md"
    original = "# Demo\n"
    readme.write_text(original, encoding="utf-8")
    result = GovernedAgentRuntime(
        root=tmp_path,
        governed_agent=GovernedAgent(root_path=tmp_path, ledger_path=tmp_path / "ledger.jsonl"),
        llm_client=FakeLLMClient(),
    ).run_task("Improve README with governed agent summary")

    assert result["decision"] == "REQUEST_REVIEW"
    assert result["governed_result"]["code_change_proposal"]["diff_hash"].startswith("sha256:")
    assert readme.read_text(encoding="utf-8") == original
