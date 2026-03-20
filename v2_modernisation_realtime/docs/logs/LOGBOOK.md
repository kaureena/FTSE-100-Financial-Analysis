# Logbook

A dense, reviewer-friendly work log for the FTSE 100 Financial Analysis repo.

This repo is presented as a **UK Master’s project** (V1 dissertation baseline) plus a **modernised industry platform** (V2).

> Portfolio note: entries are curated from build runs + artefact generation and are intended to show an end-to-end delivery narrative.


---

## How to use this logbook

- Use it to understand *what changed*, *why it changed*, and *where the evidence lives*.

- Pair with `CHANGELOG.md` for release-style view and with `docs/logs/refresh_run_register.csv` for run-level audit.


---

## Entries

### 2026-01-21 — Planning

**Summary:** Defined UK market terminal theme and repo positioning as a Master’s dissertation + modern platform extension.


**Key artefacts / evidence:**

- `assets/branding/REPO_THEME_GUIDE.md`
- `README.md`


**Notes / decisions:**

- Decided to separate V1 (dissertation baseline replay) and V2 (modern platform) to satisfy both academic narrative and industry-grade engineering.
- Adopted 'terminal realism' visual language: dark background, neon accents, compact density, UK market conventions (London time, LSE session).


### 2024-07-27 — V1

**Summary:** Built V1 snapshot dataset and cleaning pipeline; generated baseline KPI and DQ artefacts.


**Key artefacts / evidence:**

- `v1_dissertation_baseline/data/processed/ftse100_intraday_1m_clean.parquet`
- `v1_dissertation_baseline/outputs/metrics/session_kpis.csv`
- `v1_dissertation_baseline/outputs/metrics/dq_snapshot.json`


**Notes / decisions:**

- Normalised timestamps to Europe/London; ensured 08:00–16:30 trading window coverage.
- Implemented gap detection + OHLC sanity checks; persisted both JSON snapshot and CSV detail for audit.


### 2024-08-14 — V1

**Summary:** Generated the 7 dissertation-style dashboard pages at 4K and saved them under docs/dashboards/V1/exports.


**Key artefacts / evidence:**

- `docs/dashboards/V1/exports/v1_page_01_market_overview.png`
- `docs/dashboards/V1/exports/v1_page_04_arima_forecast.png`
- `docs/dashboards/V1/exports/v1_page_05_lstm_forecast.png`


**Notes / decisions:**

- Kept the layout closer to dissertation narrative: price/volume, technicals, ARIMA vs LSTM, model comparison, DQ snapshot.


### 2026-02-16 — V2

**Summary:** Materialised bronze/silver/gold layers + mart tables; populated local DuckDB warehouse; ensured dashboard exports read from mart parquet only.


**Key artefacts / evidence:**

- `v2_modernisation_realtime/data/mart/*.parquet`
- `v2_modernisation_realtime/db/warehouse.duckdb`
- `docs/dashboards/V2/exports/`


**Notes / decisions:**

- Defined semantic marts per dashboard page (market_overview, drawdown_risk, sector_rotation, pipeline_health, etc.).
- Added monitoring tables for drift/latency/DQ and included 14-day pipeline run histories.


### 2026-02-17 — V2

**Summary:** Final UK market terminal realism pass: constituents universe loader + events enrichment stub; added Power BI export pack and governance logs.


**Key artefacts / evidence:**

- `data/reference/ftse100_constituents_universe_snapshot.csv`
- `v2_modernisation_realtime/bi_powerbi/exports/pbi_page_01_market_overview.png`
- `LOGBOOK.md / PROGRESS_LOG_DAILY.md / RISK_LOG.md`


**Notes / decisions:**

- Universe loader provides tickers + sectors + weights for sector rotation / movers context.
- Events stub introduces macro calendar + earnings dates (extensible to live feeds).
- Added portfolio-grade operational logs (changelog, risk register, hours CSVs) for realism and auditability.



> Tip: filter entries for **stream = V2**.
