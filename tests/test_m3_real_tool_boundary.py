from __future__ import annotations

import sys

from gcr_agent import GovernedAgent
from gcr_agent.controlled_local_tools import (
    ToolBoundaryError,
    git_diff_real,
    list_files_real,
    read_file_real,
    run_tests_real,
)


def test_safe_read_invokes_real_read_tool() -> None:
    result = GovernedAgent(root_path=".").handle_request("Read README.md")

    assert result["envelope"]["decision"] == "ALLOW"
    assert result["tool_result"]["tool_name"] == "read_file_real"
    assert result["tool_result"]["tool_status"] == "SUCCESS"
    assert "# Governed Action Agent" in result["tool_result"]["content"]
    assert result["receipt"]["tool_name"] == "read_file_real"


def test_secret_read_never_invokes_real_read_tool() -> None:
    result = GovernedAgent(root_path=".").handle_request("Read .env")

    assert result["envelope"]["decision"] == "DENY"
    assert result["tool_result"]["tool_status"] == "NOT_INVOKED"
    assert result["receipt"]["execution_status"] == "NOT_EXECUTED"


def test_read_file_real_blocks_secret_like_paths() -> None:
    try:
        read_file_real(".", ".env")
    except ToolBoundaryError as exc:
        assert "Secret-like file reads are blocked" in str(exc)
    else:
        raise AssertionError("read_file_real should block .env")


def test_list_files_real_lists_repo_files() -> None:
    result = list_files_real(".")

    assert result["tool_name"] == "list_files_real"
    assert result["tool_status"] == "SUCCESS"
    assert "README.md" in result["entries"]


def test_git_diff_real_is_read_only() -> None:
    result = git_diff_real(".")

    assert result["tool_name"] == "git_diff_real"
    assert result["tool_status"] == "SUCCESS"
    assert "stdout" in result


def test_run_tests_real_uses_non_shell_command_boundary() -> None:
    result = run_tests_real(".", [sys.executable, "-c", "print('m3-ok')"])

    assert result["tool_name"] == "run_tests_real"
    assert result["tool_status"] == "SUCCESS"
    assert result["returncode"] == 0
    assert result["stdout"].strip() == "m3-ok"


def test_agent_can_route_list_files_and_git_diff() -> None:
    agent = GovernedAgent(root_path=".")

    listed = agent.handle_request("List files")
    diffed = agent.handle_request("Show git diff")

    assert listed["envelope"]["decision"] == "ALLOW"
    assert listed["tool_result"]["tool_name"] == "list_files_real"
    assert diffed["envelope"]["decision"] == "ALLOW"
    assert diffed["tool_result"]["tool_name"] == "git_diff_real"
