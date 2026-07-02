from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m3_git_diff_allowed() -> None:
    result = GovernedAgent(root_path=".").handle_request("Show git diff")

    assert result["proposal"]["consequence_class"] == "READ_ONLY_ACCESS"
    assert result["envelope"]["decision"] == "ALLOW"
    assert result["envelope"]["execution_status"] == "EXECUTED"
    assert result["tool_result"]["tool_name"] == "git_diff_real"
    assert result["tool_result"]["tool_executed"] is True
    assert "stdout" in result["tool_result"]
    assert result["receipt"]["receipt_id"]
