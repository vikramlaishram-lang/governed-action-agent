from __future__ import annotations

from pathlib import Path

from gcr_agent import GovernedAgent
from gcr_agent.local_tool_boundary import LocalToolBoundary, ToolBoundaryError


def test_m3_secret_file_denied_before_tool_execution() -> None:
    result = GovernedAgent(root_path=".").handle_request("Read .env")

    assert result["proposal"]["consequence_class"] == "SECRET_ACCESS"
    assert result["envelope"]["decision"] == "DENY"
    assert result["envelope"]["execution_status"] == "NOT_EXECUTED"
    assert result["tool_result"]["tool_executed"] is False
    assert "content" not in result["tool_result"]
    assert result["receipt"]["receipt_id"]


def test_m3_boundary_blocks_secret_direct_read(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("TOKEN=blocked", encoding="utf-8")
    boundary = LocalToolBoundary(tmp_path)

    try:
        boundary.read_file(tmp_path, ".env")
    except ToolBoundaryError as exc:
        assert "Secret-like file reads are blocked" in str(exc)
    else:
        raise AssertionError("LocalToolBoundary should block .env reads")
