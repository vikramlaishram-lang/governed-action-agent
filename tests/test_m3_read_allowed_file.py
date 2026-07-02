from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m3_read_allowed_file() -> None:
    result = GovernedAgent(root_path=".").handle_request("Read README.md")

    assert result["proposal"]["consequence_class"] == "READ_ONLY_ACCESS"
    assert result["envelope"]["decision"] == "ALLOW"
    assert result["envelope"]["execution_status"] == "EXECUTED"
    assert result["tool_result"]["tool_name"] == "read_file_real"
    assert result["tool_result"]["tool_executed"] is True
    assert "# Governed Action Agent" in result["tool_result"]["content"]
    assert result["receipt"]["tool_result_summary"]
