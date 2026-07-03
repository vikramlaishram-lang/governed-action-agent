from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m11_secret_file_patch_denied(tmp_path) -> None:
    result = GovernedAgent(root_path=tmp_path).propose_code_change("Update .env with new secret")

    assert result["proposal"]["consequence_class"] == "SECRET_ACCESS"
    assert result["envelope"]["decision"] == "DENY"
    assert "code_change_proposal" not in result
    assert result["tool_result"]["tool_executed"] is False
