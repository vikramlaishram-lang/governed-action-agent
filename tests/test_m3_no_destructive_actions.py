from __future__ import annotations

from pathlib import Path

from gcr_agent import GovernedAgent
from gcr_agent.local_tool_boundary import LocalToolBoundary, ToolBoundaryError


def test_m3_no_destructive_actions_possible() -> None:
    result = GovernedAgent(root_path=".").handle_request("Delete README.md")

    assert result["proposal"]["consequence_class"] == "IRREVERSIBLE_DELETE"
    assert result["envelope"]["decision"] == "DENY"
    assert result["envelope"]["execution_status"] == "NOT_EXECUTED"
    assert result["tool_result"]["tool_executed"] is False


def test_m3_path_traversal_is_blocked(tmp_path: Path) -> None:
    boundary = LocalToolBoundary(tmp_path)

    try:
        boundary.read_file(tmp_path, "../outside.txt")
    except ToolBoundaryError as exc:
        assert "Path traversal is blocked" in str(exc)
    else:
        raise AssertionError("Path traversal should be blocked")
