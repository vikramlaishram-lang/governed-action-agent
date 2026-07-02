from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def _run_cli(cwd: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    command_env = os.environ.copy()
    command_env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    if env:
        command_env.update(env)
    return subprocess.run(
        [sys.executable, "-m", "gcr_agent.cli", *args],
        cwd=cwd,
        env=command_env,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )


def _write_readme(root: Path) -> None:
    (root / "README.md").write_text("# Demo Repo\n", encoding="utf-8")


def main() -> None:
    with TemporaryDirectory() as tmpdir:
        root = Path(tmpdir) / "demo-repo"
        root.mkdir()
        _write_readme(root)
        init = _run_cli(root, "init")
        status = _run_cli(root, "status")
        safe = _run_cli(root, "ask", "Read README.md")
        secret = _run_cli(root, "ask", "Read .env")
        verify = _run_cli(root, "verify-ledger")

        hmac_root = Path(tmpdir) / "hmac-repo"
        hmac_root.mkdir()
        _write_readme(hmac_root)
        env = {"GAA_LEDGER_HMAC_KEY": "m7-demo-dev-key"}
        hmac_init = _run_cli(hmac_root, "init", "--hmac", "--key-id", "m7-demo-key", env=env)
        _run_cli(hmac_root, "ask", "Read README.md", env=env)
        hmac_verify = _run_cli(hmac_root, "verify-ledger", env=env)

        print(f"CLI_INIT: {'OK' if 'GAA_INIT: OK' in init.stdout else 'FAILED'}")
        print(f"CLI_STATUS: {'INITIALIZED' if 'GAA_STATUS: INITIALIZED' in status.stdout else 'NOT_INITIALIZED'}")
        print(f"CLI_SAFE_READ: {_value(safe.stdout, 'DECISION')}")
        print(f"CLI_SECRET_ACCESS: {_value(secret.stdout, 'DECISION')}")
        print(f"CLI_VERIFY_LEDGER: {_value(verify.stdout, 'LEDGER_VALID')}")
        print(f"CLI_HMAC_INIT: {'OK' if 'GAA_INIT: OK' in hmac_init.stdout else 'FAILED'}")
        print(f"CLI_HMAC_VERIFY: {_value(hmac_verify.stdout, 'LEDGER_VALID')}")


def _value(output: str, key: str) -> str:
    prefix = f"{key}: "
    for line in output.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix)
    return ""


if __name__ == "__main__":
    main()
