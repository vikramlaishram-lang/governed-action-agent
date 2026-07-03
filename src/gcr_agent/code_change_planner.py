from __future__ import annotations

from pathlib import Path

from gcr.code_change_proposal import CodeChangeProposal, new_code_change_proposal

from .sandbox import SandboxWorkspace


class CodeChangePlanningError(ValueError):
    def __init__(self, consequence_class: str, message: str) -> None:
        super().__init__(message)
        self.consequence_class = consequence_class


class CodeChangePlanner:
    def plan_change(
        self,
        *,
        root: Path,
        user_request: str,
        proposal_id: str,
        agent_id: str,
    ) -> CodeChangeProposal:
        lowered = user_request.lower()
        if any(term in lowered for term in (".env", "secret", "credentials", "id_rsa", "id_ed25519")):
            raise CodeChangePlanningError("SECRET_ACCESS", "Sensitive file patch requests are denied")
        if any(term in lowered for term in ("delete", "remove", "rm -rf")):
            raise CodeChangePlanningError("IRREVERSIBLE_DELETE", "Destructive patch requests are denied")

        sandbox = SandboxWorkspace(root)
        sandbox.create_workspace()
        if "workflow" in lowered or "ci yaml" in lowered:
            return self._workflow_change(sandbox, user_request, proposal_id, agent_id)
        if "readme" in lowered:
            return self._readme_change(sandbox, user_request, proposal_id, agent_id)
        raise CodeChangePlanningError("UNKNOWN", "Unsupported code change request")

    def _readme_change(
        self,
        sandbox: SandboxWorkspace,
        user_request: str,
        proposal_id: str,
        agent_id: str,
    ) -> CodeChangeProposal:
        target = "README.md"
        source = sandbox.root / target
        original = source.read_text(encoding="utf-8") if source.exists() else ""
        addition = (
            "\n## Governed Action Agent Note\n\n"
            "This repository includes a governed agent loop that records proposal, decision, execution status, and receipt ledger evidence.\n"
        )
        proposed = original.rstrip() + addition
        sandbox.copy_allowed_file(target)
        sandbox.write_sandbox_file(target, proposed)
        diff_text = sandbox.generate_unified_diff(target, original, proposed)
        return new_code_change_proposal(
            proposal_id=proposal_id,
            agent_id=agent_id,
            user_request=user_request,
            target_files=[target],
            change_intent="Append governed agent summary to README.md",
            sandbox_path=str(sandbox.sandbox_root),
            diff_text=diff_text,
            risk_flags=[],
            requires_review=True,
        )

    def _workflow_change(
        self,
        sandbox: SandboxWorkspace,
        user_request: str,
        proposal_id: str,
        agent_id: str,
    ) -> CodeChangeProposal:
        target = ".github/workflows/example.yml"
        original = ""
        proposed = "name: Governed Agent Example\non: [pull_request]\njobs:\n  noop:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo governed-agent\n"
        sandbox.write_sandbox_file(target, proposed)
        diff_text = sandbox.generate_unified_diff(target, original, proposed)
        return new_code_change_proposal(
            proposal_id=proposal_id,
            agent_id=agent_id,
            user_request=user_request,
            target_files=[target],
            change_intent="Propose GitHub workflow example in sandbox",
            sandbox_path=str(sandbox.sandbox_root),
            diff_text=diff_text,
            risk_flags=["WORKFLOW_CHANGE"],
            requires_review=True,
        )
