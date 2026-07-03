# Evaluator Quickstart

## Step 1

```bash
git clone https://github.com/vikramlaishram-lang/governed-action-agent
cd governed-action-agent
```

## Step 2

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

## Step 3

```bash
python -m pip install -e .
```

## Step 4

```bash
PYTHONPATH=src python -m pytest -q
```

## Step 5

```bash
PYTHONPATH=src python scripts/run_public_demo.py
```

## Step 6

```bash
PYTHONPATH=src python scripts/validate_release_package.py
```

## CLI Path

```bash
PYTHONPATH=src python -m gcr_agent.cli init
PYTHONPATH=src python -m gcr_agent.cli ask "Read README.md"
PYTHONPATH=src python -m gcr_agent.cli ask "Read .env"
PYTHONPATH=src python -m gcr_agent.cli propose-change "Update README.md with governed agent summary"
PYTHONPATH=src python -m gcr_agent.cli report
PYTHONPATH=src python -m gcr_agent.cli viewer
```
