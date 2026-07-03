from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m11_readme_patch_proposal(tmp_path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")

    result = GovernedAgent(root_path=tmp_path).propose_code_change("Update README.md with governed agent summary")

    artifact = result["code_change_proposal"]
    assert "Governed Action Agent Note" in result["tool_result"]["code_change_proposal"]["diff_text"]
    assert artifact["target_files"] == ["README.md"]
    assert artifact["diff_hash"].startswith("sha256:")
