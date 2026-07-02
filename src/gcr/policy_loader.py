from __future__ import annotations

import hashlib
import json
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_policy(path: str | Path | None = None) -> dict:
    policy_path = Path(path) if path is not None else _repo_root() / "configs" / "policy.default.json"
    with policy_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def get_policy_rule(policy: dict, consequence_class: str) -> dict:
    default_rule = {
        "decision": policy.get("default_decision", "REQUEST_REVIEW"),
        "review_required": True,
        "review_can_override": False,
    }
    return dict(policy.get("rules", {}).get(consequence_class, default_rule))


def policy_hash(policy: dict) -> str:
    canonical = json.dumps(policy, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
