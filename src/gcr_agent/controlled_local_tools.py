from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


MAX_TEXT_BYTES = 200_000
MAX_LIST_ENTRIES = 500

SECRET_FILENAMES = {".env", ".env.local", ".env.production", "secrets.json"}
SECRET_MARKERS = ("secret", "credential", "token", "private_key")


class ToolBoundaryError(ValueError):
    """Raised when a requested local tool action crosses the M3 boundary."""


def _repo_root(root_path: str | Path) -> Path:
    return Path(root_path).resolve()


def _resolve_inside_root(root_path: str | Path, requested_path: str | Path) -> Path:
    root = _repo_root(root_path)
    candidate = Path(requested_path)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    if resolved != root and root not in resolved.parents:
        raise ToolBoundaryError(f"Path escapes governed root: {requested_path}")
    return resolved


def _is_secret_path(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    return name in SECRET_FILENAMES or any(marker in parts or marker in name for marker in SECRET_MARKERS)


def read_file_real(root_path: str | Path, requested_path: str) -> dict:
    path = _resolve_inside_root(root_path, requested_path)
    if _is_secret_path(path):
        raise ToolBoundaryError(f"Secret-like file reads are blocked: {requested_path}")
    if not path.is_file():
        raise ToolBoundaryError(f"File does not exist: {requested_path}")

    data = path.read_bytes()
    truncated = len(data) > MAX_TEXT_BYTES
    text = data[:MAX_TEXT_BYTES].decode("utf-8", errors="replace")
    return {
        "tool_name": "read_file_real",
        "tool_status": "SUCCESS",
        "path": str(path),
        "bytes_read": min(len(data), MAX_TEXT_BYTES),
        "truncated": truncated,
        "content": text,
    }


def list_files_real(root_path: str | Path, requested_path: str = ".") -> dict:
    path = _resolve_inside_root(root_path, requested_path)
    if not path.exists():
        raise ToolBoundaryError(f"Path does not exist: {requested_path}")
    if not path.is_dir():
        raise ToolBoundaryError(f"Path is not a directory: {requested_path}")

    root = _repo_root(root_path)
    entries: list[str] = []
    for current_root, dirnames, filenames in os.walk(path):
        dirnames[:] = [name for name in sorted(dirnames) if name not in {".git", "__pycache__", ".pytest_cache"}]
        for filename in sorted(filenames):
            file_path = Path(current_root) / filename
            entries.append(file_path.resolve().relative_to(root).as_posix())
            if len(entries) >= MAX_LIST_ENTRIES:
                return {
                    "tool_name": "list_files_real",
                    "tool_status": "SUCCESS",
                    "path": str(path),
                    "entries": entries,
                    "truncated": True,
                }
    return {
        "tool_name": "list_files_real",
        "tool_status": "SUCCESS",
        "path": str(path),
        "entries": entries,
        "truncated": False,
    }


def git_diff_real(root_path: str | Path) -> dict:
    root = _repo_root(root_path)
    completed = subprocess.run(
        ["git", "diff", "--no-ext-diff", "--"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return {
        "tool_name": "git_diff_real",
        "tool_status": "SUCCESS" if completed.returncode == 0 else "FAILED",
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def run_tests_real(root_path: str | Path, args: list[str] | None = None) -> dict:
    root = _repo_root(root_path)
    command = args or [sys.executable, "-m", "pytest", "-q"]
    completed = subprocess.run(
        command,
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    return {
        "tool_name": "run_tests_real",
        "tool_status": "SUCCESS" if completed.returncode == 0 else "FAILED",
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
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
    tool_name, kwargs = choose_tool_for_request(user_request)
    if tool_name is None:
        return {
            "tool_name": None,
            "tool_status": "SKIPPED",
            "reason": "No M3 controlled local tool matched the request",
        }
    try:
        if tool_name == "read_file_real":
            return read_file_real(root_path, kwargs["requested_path"])
        if tool_name == "list_files_real":
            return list_files_real(root_path, kwargs["requested_path"])
        if tool_name == "git_diff_real":
            return git_diff_real(root_path)
        if tool_name == "run_tests_real":
            return run_tests_real(root_path)
    except ToolBoundaryError as exc:
        return {"tool_name": tool_name, "tool_status": "BLOCKED", "reason": str(exc)}
    return {"tool_name": tool_name, "tool_status": "FAILED", "reason": "Unknown tool dispatch failure"}


def _extract_requested_file(user_request: str) -> str:
    tokens = user_request.strip().split()
    if not tokens:
        return "."
    return tokens[-1].strip("'\"")
