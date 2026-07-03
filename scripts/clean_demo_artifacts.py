from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ALLOWED_RELATIVE_DIRS = [
    Path(".governed-agent/public-demo"),
    Path(".governed-agent/demo-output"),
    Path("tmp_public_demo"),
    Path("examples/tmp"),
]
PROTECTED_DIRS = {"src", "tests", "docs", "schemas", "configs", ".git"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    clean_demo_artifacts(Path(args.root))
    print("CLEAN_DEMO_ARTIFACTS_DONE: true")
    return 0


def clean_demo_artifacts(root: Path) -> None:
    root = root.resolve()
    for protected in PROTECTED_DIRS:
        if (root / protected).exists() and (root / protected).resolve() == root:
            raise ValueError(f"Refusing to clean protected root: {root}")
    for relative in ALLOWED_RELATIVE_DIRS:
        target = (root / relative).resolve()
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"Refusing to remove path outside root: {target}") from exc
        if target.name in PROTECTED_DIRS:
            raise ValueError(f"Refusing to remove protected directory: {target}")
        if target.exists():
            shutil.rmtree(target)


if __name__ == "__main__":
    sys.exit(main())
