from __future__ import annotations

import copy
import hashlib
import json


def canonical_json(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def evidence_hash(payload: dict) -> str:
    hashable = copy.deepcopy(payload)
    hashable.pop("evidence_hash", None)
    return f"sha256:{hashlib.sha256(canonical_json(hashable)).hexdigest()}"
