from __future__ import annotations

import json
import shutil
from pathlib import Path


DEFAULT_CONFIG_DIR = ".governed-agent"
DEFAULT_CONFIG_FILE = "config.json"
DEFAULT_POLICY_FILE = "policy.json"
DEFAULT_LEDGER_FILE = "ledger.jsonl"


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if (candidate / DEFAULT_CONFIG_DIR / DEFAULT_CONFIG_FILE).exists():
            return candidate
    return current


def init_project(
    root: Path,
    *,
    auth_mode: str = "UNKEYED_HASH_CHAIN",
    key_id: str | None = None,
    force: bool = False,
) -> dict:
    root = root.resolve()
    config_dir = root / DEFAULT_CONFIG_DIR
    config_path = config_dir / DEFAULT_CONFIG_FILE
    policy_path = config_dir / DEFAULT_POLICY_FILE
    ledger_path = config_dir / DEFAULT_LEDGER_FILE

    if config_path.exists() and not force:
        raise FileExistsError(f"Project config already exists: {config_path}")

    config_dir.mkdir(parents=True, exist_ok=True)
    default_policy = Path(__file__).resolve().parents[2] / "configs" / "policy.default.json"
    if force or not policy_path.exists():
        shutil.copyfile(default_policy, policy_path)
    if not ledger_path.exists():
        ledger_path.write_text("", encoding="utf-8")

    config = {
        "schema_version": "governed_agent_project_config_v0.1",
        "project_name": root.name,
        "ledger_path": f"{DEFAULT_CONFIG_DIR}/{DEFAULT_LEDGER_FILE}",
        "policy_path": f"{DEFAULT_CONFIG_DIR}/{DEFAULT_POLICY_FILE}",
        "ledger_auth_mode": auth_mode,
        "ledger_key_id": key_id if auth_mode == "HMAC_SHA256_V1" else None,
    }
    config_path.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return config


def load_project_config(root: Path | None = None) -> dict:
    project_root = find_project_root(root)
    config_path = project_root / DEFAULT_CONFIG_DIR / DEFAULT_CONFIG_FILE
    if not config_path.exists():
        raise FileNotFoundError(f"Governed agent project is not initialized: {config_path}")
    return json.loads(config_path.read_text(encoding="utf-8"))


def resolve_paths(config: dict, root: Path) -> dict:
    root = root.resolve()
    return {
        "config_path": root / DEFAULT_CONFIG_DIR / DEFAULT_CONFIG_FILE,
        "policy_path": (root / config["policy_path"]).resolve(),
        "ledger_path": (root / config["ledger_path"]).resolve(),
    }


def project_status(root: Path | None = None) -> dict:
    project_root = find_project_root(root)
    config_path = project_root / DEFAULT_CONFIG_DIR / DEFAULT_CONFIG_FILE
    if not config_path.exists():
        return {"initialized": False, "config_path": config_path}

    config = json.loads(config_path.read_text(encoding="utf-8"))
    paths = resolve_paths(config, project_root)
    return {
        "initialized": True,
        "config_path": paths["config_path"],
        "ledger_path": paths["ledger_path"],
        "policy_path": paths["policy_path"],
        "ledger_exists": paths["ledger_path"].exists(),
        "policy_exists": paths["policy_path"].exists(),
        "ledger_auth_mode": config.get("ledger_auth_mode"),
        "ledger_key_id": config.get("ledger_key_id"),
    }
