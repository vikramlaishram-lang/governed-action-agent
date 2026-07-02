from __future__ import annotations

import os

import pytest

from gcr_agent import GovernedAgent


@pytest.mark.skipif(
    os.environ.get("GAA_TOOL_BOUNDARY_INNER_TEST") == "1",
    reason="avoid recursive pytest launch inside run_tests_real subprocess",
)
def test_m3_run_tests_allowed() -> None:
    result = GovernedAgent(root_path=".").handle_request("Run tests")

    assert result["proposal"]["consequence_class"] == "LOCAL_COMPUTATION"
    assert result["envelope"]["decision"] == "ALLOW"
    assert result["envelope"]["execution_status"] == "EXECUTED"
    assert result["tool_result"]["tool_name"] == "run_tests_real"
    assert result["tool_result"]["tool_executed"] is True
    assert result["tool_result"]["returncode"] == 0
    assert result["receipt"]["receipt_id"]
