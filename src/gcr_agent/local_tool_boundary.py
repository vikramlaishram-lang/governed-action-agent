from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


MAX_TEXT_BYTES = 200_000
MAX_LIST_ENTRIES = 500

BLOCKED_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "secrets.json",
    "credentials.json",
    "id_rsa",
    "id_ed25519",
}
BLOCKED_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}
SECRET_MARKERS = ("secret", "credential", "token", "private_key")


class ToolBoundaryError(ValueError):
    """Raised when a requested local tool action crosses the M3 boundary."""


class LocalToolBoundary:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()

    def list_files(self, root: Path | str | None = None) -> dict:
        path = self._resolve_inside_root(root or self.root)
        if not path.exists():
            raise ToolBoundaryError(f"Path does not exist: {path}")
        if not path.is_dir():
            raise ToolBoundaryError(f"Path is not a directory: {path}")

        entries: list[str] = []
        for current_root, dirnames, filenames in os.walk(path):
            dirnames[:] = [name for name in sorted(dirnames) if name not in BLOCKED_DIRS]
            for filename in sorted(filenames):
                file_path = Path(current_root) / filename
                entries.append(file_path.resolve().relative_to(self.root).as_posix())
                if len(entries) >= MAX_LIST_ENTRIES:
                    return {
                        "tool_name": "list_files_real",
                        "tool_executed": True,
                        "tool_status": "SUCCESS",
                        "path": str(path),
                        "entries": entries,
                        "truncated": True,
                        "summary": f"listed {len(entries)} files",
                    }
        return {
            "tool_name": "list_files_real",
            "tool_executed": True,
            "tool_status": "SUCCESS",
            "path": str(path),
            "entries": entries,
            "truncated": False,
            "summary": f"listed {len(entries)} files",
        }

    def read_file(self, root: Path | str | None, relative_path: str) -> dict:
        path = self._resolve_inside_root(relative_path, base=root or self.root)
        self._reject_blocked_path(path)
        if not path.is_file():
            raise ToolBoundaryError(f"File does not exist: {relative_path}")

        data = path.read_bytes()
        truncated = len(data) > MAX_TEXT_BYTES
        content = data[:MAX_TEXT_BYTES].decode("utf-8", errors="replace")
        return {
            "tool_name": "read_file_real",
            "tool_executed": True,
            "tool_status": "SUCCESS",
            "path": str(path),
            "bytes_read": min(len(data), MAX_TEXT_BYTES),
            "truncated": truncated,
            "content": content,
            "preview": content[:1000],
            "summary": f"read {min(len(data), MAX_TEXT_BYTES)} bytes from {path.name}",
        }

    def run_tests(self, root: Path | str | None = None) -> dict:
        cwd = self._resolve_inside_root(root or self.root)
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ, "GAA_TOOL_BOUNDARY_INNER_TEST": "1"},
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

    def git_diff(self, root: Path | str | None = None) -> dict:
        cwd = self._resolve_inside_root(root or self.root)
        diff = subprocess.run(
            ["git", "diff", "--stat"],
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        status = subprocess.run(
            ["git", "status", "--short"],
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        clean_message = "clean tree" if not diff.stdout and not status.stdout else ""
        return {
            "tool_name": "git_diff_real",
            "tool_executed": True,
            "tool_status": "SUCCESS" if diff.returncode == 0 and status.returncode == 0 else "FAILED",
            "returncode": diff.returncode if diff.returncode != 0 else status.returncode,
            "stdout": diff.stdout or clean_message,
            "status_stdout": status.stdout,
            "stderr": diff.stderr + status.stderr,
            "summary": clean_message or "git diff/status captured",
        }

    def execute_tool(
        self,
        action: str,
        normalized_action: str,
        decision: str,
        consequence_class: str,
        constitutional_errors: list[str] | None = None,
    ) -> dict:
        if constitutional_errors and "CONSTITUTIONAL_VIOLATION" in constitutional_errors:
            return self._not_invoked("Constitutional violation")
        if decision != "ALLOW":
            return self._not_invoked(f"Decision is {decision}")

        lowered = normalized_action.lower()
        try:
            if any(term in lowered for term in ("run tests", "pytest", "test suite")):
                return self.run_tests(self.root)
            if any(term in lowered for term in ("git diff", "show diff", "status")):
                return self.git_diff(self.root)
            if any(term in lowered for term in ("list files", "show files")) or lowered == "ls":
                return self.list_files(self.root)
            if any(term in lowered for term in ("read ", "open ", "show ")):
                return self.read_file(self.root, self._extract_requested_file(action))
        except (ToolBoundaryError, subprocess.TimeoutExpired) as exc:
            return {
                "tool_name": self._tool_name_for_action(lowered),
                "tool_executed": False,
                "tool_status": "BLOCKED",
                "reason": str(exc),
                "summary": f"blocked: {exc}",
            }

        return self._not_invoked("No M3 controlled local tool matched the request")

    def _resolve_inside_root(self, requested_path: Path | str, base: Path | str | None = None) -> Path:
        requested = Path(requested_path)
        if ".." in requested.parts:
            raise ToolBoundaryError(f"Path traversal is blocked: {requested_path}")
        if not requested.is_absolute():
            requested = Path(base or self.root) / requested
        resolved = requested.resolve()
        if resolved != self.root and self.root not in resolved.parents:
            raise ToolBoundaryError(f"Path escapes governed root: {requested_path}")
        return resolved

    def _reject_blocked_path(self, path: Path) -> None:
        lower_parts = [part.lower() for part in path.relative_to(self.root).parts]
        filename = path.name.lower()
        if filename in BLOCKED_FILENAMES:
            raise ToolBoundaryError(f"Secret-like file reads are blocked: {path.name}")
        if any(part in BLOCKED_DIRS for part in lower_parts):
            raise ToolBoundaryError(f"Blocked directory reads are not allowed: {path}")
        if any(marker in filename for marker in SECRET_MARKERS):
            raise ToolBoundaryError(f"Secret-like file reads are blocked: {path.name}")

    def _not_invoked(self, reason: str) -> dict:
        return {
            "tool_name": None,
            "tool_executed": False,
            "tool_status": "NOT_INVOKED",
            "reason": reason,
            "summary": reason,
        }

    def _tool_name_for_action(self, lowered_action: str) -> str | None:
        if "test" in lowered_action or "pytest" in lowered_action:
            return "run_tests_real"
        if "git diff" in lowered_action or "show diff" in lowered_action or "status" in lowered_action:
            return "git_diff_real"
        if "list files" in lowered_action or "show files" in lowered_action or lowered_action == "ls":
            return "list_files_real"
        if any(term in lowered_action for term in ("read ", "open ", "show ")):
            return "read_file_real"
        return None

    def _extract_requested_file(self, user_request: str) -> str:
        tokens = user_request.strip().split()
        if not tokens:
            return "."
        return tokens[-1].strip("'\"")
