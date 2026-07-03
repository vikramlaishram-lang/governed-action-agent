from __future__ import annotations

import pytest

from gcr_agent.sandbox import SandboxBoundaryError, SandboxWorkspace


def test_m11_sandbox_creates_isolated_workspace(tmp_path) -> None:
    workspace = SandboxWorkspace(tmp_path).create_workspace()

    assert workspace.exists()
    assert ".governed-agent" in str(workspace)


def test_m11_sandbox_rejects_path_traversal(tmp_path) -> None:
    sandbox = SandboxWorkspace(tmp_path)

    with pytest.raises(SandboxBoundaryError):
        sandbox.write_sandbox_file("../escape.txt", "nope")


def test_m11_sandbox_rejects_secret_files(tmp_path) -> None:
    sandbox = SandboxWorkspace(tmp_path)

    with pytest.raises(SandboxBoundaryError):
        sandbox.write_sandbox_file(".env", "SECRET=nope")
