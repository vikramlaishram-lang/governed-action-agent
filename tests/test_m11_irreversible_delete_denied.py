from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m11_irreversible_delete_denied(tmp_path) -> None:
    result = GovernedAgent(root_path=tmp_path).propose_code_change("Delete README.md")

    assert result["proposal"]["consequence_class"] == "IRREVERSIBLE_DELETE"
    assert result["envelope"]["decision"] == "DENY"
    assert "code_change_proposal" not in result
