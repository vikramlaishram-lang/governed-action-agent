from __future__ import annotations

from pathlib import Path


FORBIDDEN_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}
FORBIDDEN_FILES = {".env", "secrets.json", "credentials.json", "id_rsa", "id_ed25519"}


def collect_repo_context(root: Path) -> dict:
    root = Path(root).resolve()
    entries = []
    for item in sorted(root.iterdir(), key=lambda path: path.name.lower()):
        if item.name in FORBIDDEN_DIRS or item.name in FORBIDDEN_FILES:
            continue
        if item.name == ".governed-agent" and (item / "sandbox").exists():
            entries.append(item.name)
            continue
        entries.append(item.name)
    readme = root / "README.md"
    return {
        "root_name": root.name,
        "readme_exists": readme.exists(),
        "top_level_files": entries,
        "pyproject_exists": (root / "pyproject.toml").exists(),
        "tests_exists": (root / "tests").exists(),
        "docs_exists": (root / "docs").exists(),
        "governed_agent_exists": (root / ".governed-agent").exists(),
        "readme_summary": _readme_summary(readme) if readme.exists() else None,
    }


def _readme_summary(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    return " ".join(text.split())[:240]
