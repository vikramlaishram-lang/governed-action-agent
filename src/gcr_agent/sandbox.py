from __future__ import annotations

import difflib
import shutil
from pathlib import Path


BLOCKED_FILENAMES = {".env", ".env.local", ".env.production", "secrets.json", "credentials.json", "id_rsa", "id_ed25519"}
BLOCKED_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}


class SandboxBoundaryError(ValueError):
    pass


class SandboxWorkspace:
    def __init__(self, root: Path, sandbox_dir: str = ".governed-agent/sandbox") -> None:
        self.root = Path(root).resolve()
        self.sandbox_root = (self.root / sandbox_dir).resolve()

    def create_workspace(self) -> Path:
        self.sandbox_root.mkdir(parents=True, exist_ok=True)
        return self.sandbox_root

    def clear_workspace(self) -> None:
        if self.sandbox_root.exists():
            shutil.rmtree(self.sandbox_root)
        self.create_workspace()

    def copy_allowed_file(self, relative_path: str) -> Path:
        source = self._resolve_repo_file(relative_path)
        target = self.sandbox_root / relative_path
        self.ensure_inside_sandbox(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, target)
        else:
            target.write_text("", encoding="utf-8")
        return target

    def write_sandbox_file(self, relative_path: str, content: str) -> Path:
        self._validate_relative_path(relative_path)
        target = self.sandbox_root / relative_path
        self.ensure_inside_sandbox(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def read_sandbox_file(self, relative_path: str) -> str:
        self._validate_relative_path(relative_path)
        path = self.ensure_inside_sandbox(self.sandbox_root / relative_path)
        return path.read_text(encoding="utf-8")

    def generate_unified_diff(self, relative_path: str, original_text: str, proposed_text: str) -> str:
        diff = difflib.unified_diff(
            original_text.splitlines(keepends=True),
            proposed_text.splitlines(keepends=True),
            fromfile=f"a/{relative_path}",
            tofile=f"b/{relative_path}",
        )
        return "".join(diff)

    def ensure_inside_sandbox(self, path: Path) -> Path:
        resolved = Path(path).resolve()
        if resolved != self.sandbox_root and self.sandbox_root not in resolved.parents:
            raise SandboxBoundaryError(f"Path escapes sandbox: {path}")
        return resolved

    def _resolve_repo_file(self, relative_path: str) -> Path:
        self._validate_relative_path(relative_path)
        path = (self.root / relative_path).resolve()
        if path != self.root and self.root not in path.parents:
            raise SandboxBoundaryError(f"Path escapes repo: {relative_path}")
        return path

    def _validate_relative_path(self, relative_path: str) -> None:
        path = Path(relative_path)
        if path.is_absolute() or ".." in path.parts:
            raise SandboxBoundaryError(f"Invalid sandbox target path: {relative_path}")
        lower_parts = [part.lower() for part in path.parts]
        if any(part in BLOCKED_DIRS for part in lower_parts):
            raise SandboxBoundaryError(f"Blocked sandbox directory target: {relative_path}")
        name = path.name.lower()
        if name in BLOCKED_FILENAMES or "secret" in str(path).lower() or "credential" in str(path).lower():
            raise SandboxBoundaryError(f"Blocked sensitive sandbox target: {relative_path}")
