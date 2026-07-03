from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


SOURCE_PATHS = [
    Path("docs/external_review"),
    Path("examples/external_review"),
    Path("docs/PUBLIC_CLAIMS_AND_LIMITATIONS.md"),
    Path("docs/EVALUATOR_QUICKSTART.md"),
    Path("examples/public_demo_expected_output.txt"),
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="dist/external-review-packet")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    output_dir = output_dir.resolve()

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    copied: list[Path] = []
    for source in SOURCE_PATHS:
        source_path = root / source
        if not source_path.exists():
            continue
        if source_path.is_dir():
            for file_path in sorted(path for path in source_path.rglob("*") if path.is_file()):
                relative = file_path.relative_to(root)
                _copy_file(file_path, output_dir / relative)
                copied.append(relative)
        else:
            _copy_file(source_path, output_dir / source)
            copied.append(source)

    packet_index = output_dir / "PACKET_INDEX.md"
    lines = ["# External Review Packet Index", "", "Included files:", ""]
    lines.extend(f"- {path.as_posix()}" for path in sorted(copied, key=lambda p: p.as_posix()))
    packet_index.write_text("\n".join(lines) + "\n", encoding="utf-8")
    copied.append(Path("PACKET_INDEX.md"))

    print("EXTERNAL_REVIEW_PACKET_GENERATED: true")
    print(f"PACKET_INDEX_READY: {str(packet_index.exists()).lower()}")
    print(f"PACKET_FILES_COUNT: {len(copied)}")
    print(f"PACKET_OUTPUT_DIR: {_display_output_dir(args.output_dir)}")
    return 0


def _copy_file(source: Path, target: Path) -> None:
    if any(part in {".git", ".venv", "__pycache__"} for part in source.parts):
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def _display_output_dir(raw_output_dir: str) -> str:
    return raw_output_dir.replace("\\", "/")


if __name__ == "__main__":
    sys.exit(main())
