from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m3_list_files_allowed() -> None:
    result = GovernedAgent(root_path=".").handle_request("List files")

    assert result["proposal"]["consequence_class"] == "READ_ONLY_ACCESS"
    assert result["envelope"]["decision"] == "ALLOW"
    assert result["envelope"]["execution_status"] == "EXECUTED"
    assert result["tool_result"]["tool_name"] == "list_files_real"
    assert result["tool_result"]["tool_executed"] is True
    assert "README.md" in result["tool_result"]["entries"]
    assert result["receipt"]["receipt_id"]
