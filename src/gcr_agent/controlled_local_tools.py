from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .consequence_classifier import classify_consequence
from .local_tool_boundary import LocalToolBoundary, ToolBoundaryError


def read_file_real(root_path: str | Path, requested_path: str) -> dict:
    return LocalToolBoundary(root_path).read_file(root_path, requested_path)


def list_files_real(root_path: str | Path, requested_path: str = ".") -> dict:
    boundary = LocalToolBoundary(root_path)
    path = boundary._resolve_inside_root(requested_path)
    return boundary.list_files(path)


def git_diff_real(root_path: str | Path) -> dict:
    return LocalToolBoundary(root_path).git_diff(root_path)


def run_tests_real(root_path: str | Path, args: list[str] | None = None) -> dict:
    root = Path(root_path).resolve()
    command = args or [sys.executable, "-m", "pytest", "-q"]
    completed = subprocess.run(
        command,
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return {
        "tool_name": "run_tests_real",
        "tool_executed": True,
        "tool_status": "SUCCESS" if completed.returncode == 0 else "FAILED",
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "summary": f"pytest returncode {completed.returncode}",
    }


def choose_tool_for_request(user_request: str) -> tuple[str | None, dict]:
    lowered = user_request.lower()
    if "git diff" in lowered or "show diff" in lowered:
        return "git_diff_real", {}
    if "run tests" in lowered or "pytest" in lowered:
        return "run_tests_real", {}
    if "list files" in lowered or "show files" in lowered:
        return "list_files_real", {"requested_path": "."}
    if any(term in lowered for term in ("read ", "open ", "show ")):
        return "read_file_real", {"requested_path": _extract_requested_file(user_request)}
    return None, {}


def execute_controlled_tool(root_path: str | Path, user_request: str) -> dict:
    return LocalToolBoundary(root_path).execute_tool(
        user_request,
        user_request.lower(),
        "ALLOW",
        classify_consequence(user_request),
    )


def _extract_requested_file(user_request: str) -> str:
    tokens = user_request.strip().split()
    if not tokens:
        return "."
    return tokens[-1].strip("'\"")
