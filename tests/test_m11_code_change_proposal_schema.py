from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from gcr_agent import GovernedAgent


def test_m11_code_change_proposal_schema(tmp_path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    result = GovernedAgent(root_path=tmp_path).propose_code_change("Update README.md with governed agent summary")
    schema = json.loads(Path("schemas/code_change_proposal_v0.1.schema.json").read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(result["code_change_proposal"])
    assert result["code_change_proposal"]["applied_to_real_repo"] is False
