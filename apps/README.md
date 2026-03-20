# Apps

## UK Market Terminal (Streamlit)

This repo ships a **terminal-style Streamlit app** that reads from the V2 `mart.*` tables.

### Install

```bash
pip install -r requirements.txt -r requirements_ui.txt
```

### Run

```bash
streamlit run apps/uk_market_terminal.py
```

The app reads mart tables from:

- `v2_modernisation_realtime/data/mart/*.parquet` (preferred)
- falls back to `*.csv` if parquet is unavailable.
