from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from gcr.policy_loader import get_policy_rule, load_policy, policy_hash


def test_m4_policy_file_loads_and_validates() -> None:
    policy = load_policy()
    schema = json.loads(Path("schemas/policy_v0.1.schema.json").read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(policy)

    assert policy["schema_version"] == "policy_v0.1"
    assert policy["policy_version"] == "m4-default-policy"
    assert get_policy_rule(policy, "PRODUCTION_STATE_CHANGE")["decision"] == "REQUEST_REVIEW"
    assert len(policy_hash(policy)) == 64
