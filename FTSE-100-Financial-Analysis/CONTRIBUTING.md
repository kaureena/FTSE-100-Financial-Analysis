# Contributing

This repository is designed as a **portfolio-grade project** (documentation-first, reproducible builds, high-resolution exports).

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional UI (terminal app):

```bash
pip install -r requirements_ui.txt
```

## Build pipelines

### V1 (dissertation baseline)

```bash
python scripts/v1_build_all.py --data-source snapshot
```

### V2 (modern platform)

```bash
python scripts/v2_build_all.py --data-source synthetic
```

## Tests

```bash
pytest
```

## Style

- Keep markdown pages consistent with `docs/dashboards/**/pages/*`
- If you add a new dashboard page, ensure:
  - it references a `mart.*` input table
  - that table exists as `v2_modernisation_realtime/data/mart/<table>.parquet`
