# Release Package

## Contents

The release package includes the governed agent source, tests, schemas, configs, demos, scripts, docs, sample report artifacts, and a sample local receipt viewer.

## Main Commands

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_public_demo.py
PYTHONPATH=src python scripts/validate_release_package.py
PYTHONPATH=src python scripts/clean_demo_artifacts.py
```

## Files And Directories

- `src/`: governed agent and governance modules
- `tests/`: regression and milestone tests
- `configs/`: default policy and reviewer registry
- `schemas/`: JSON schemas
- `docs/`: public evaluation and milestone docs
- `examples/`: sanitized sample report and viewer artifacts
- `scripts/`: public demo, release validation, and cleanup helpers

## Validate Package

```bash
PYTHONPATH=src python scripts/validate_release_package.py
```

## Clean Generated Artifacts

```bash
PYTHONPATH=src python scripts/clean_demo_artifacts.py
```

The cleanup script removes only approved local demo directories.

## Inspect Report And Viewer

Open `examples/sample_governed_agent_report.md`, `examples/sample_governed_agent_report.json`, and `examples/sample_viewer/index.html`.

## Safe To Share Publicly

Source code, docs, configs, schemas, tests, expected demo output, sanitized reports, and sanitized viewer artifacts are safe to share.

## Do Not Commit

Do not commit real secrets, HMAC keys, GitHub tokens, authorization headers, private keys, unsanitized local ledgers, generated temp folders, or machine-specific paths.
