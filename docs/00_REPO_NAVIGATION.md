# Repo Navigation Map

This repository is intentionally **dashboard-first** and **UK-market themed**.

Use this file as a map when reviewing the repo quickly .

---

## 1) The two-track delivery (V1 vs V2)

### V1 — Dissertation Baseline (Replay / Snapshot)
**Path:** `v1_dissertation_baseline/`

Purpose:
- Preserve the academic dissertation-style approach (real-time visuals + ARIMA + LSTM).
- Produce a **7-page** export pack as evidence.

Key folders:
- `v1_dissertation_baseline/data/`  
  - `raw/` snapshot input  
  - `processed/` cleaned / tz-normalised data
- `v1_dissertation_baseline/notebooks/`  
  - V1 narrative notebooks (dissertation-style)
- `v1_dissertation_baseline/outputs/metrics/`  
  - ARIMA/LSTM metrics, DQ snapshot, model comparison
- `v1_dissertation_baseline/docs/`  
  - `diagrams/` (architecture/lineage PNGs)  
  - `Dashboards/` (V1 dashboard gallery)

Evidence pack:
- `docs/dashboards/V1/exports/` (4K PNG exports)

---

### V2 — Modernised UK Market Terminal (Platform / Monitoring)
**Path:** `v2_modernisation_realtime/`

Purpose:
- Demonstrate production-grade thinking: **medallion tables**, **monitoring**, **semantic marts**.
- Produce a **22-page** export pack and monitoring reports.

Key folders:
- `v2_modernisation_realtime/data/`  
  - `bronze/` raw-ish ingestion  
  - `silver/` cleaned + conformed  
  - `gold/` curated signals  
  - `mart/` *dashboard-ready semantic layer* (CSV + parquet)
- `v2_modernisation_realtime/db/`  
  - `warehouse.duckdb` (local BI-friendly warehouse)
- `v2_modernisation_realtime/monitoring/reports/`  
  - drift, latency, DQ coverage, incidents
- `v2_modernisation_realtime/bi_powerbi/`  
  - theme + export evidence pack (donut/gauge visuals)

Evidence packs:
- `docs/dashboards/V2/exports/` (4K PNG exports)
- `v2_modernisation_realtime/bi_powerbi/exports/` (Power BI-style 4K exports)

---

## 2) Repo-level content (governance + reference)

- `README.md` — main narrative and how to run exports.
- `CHANGELOG.md` — release history.
- `LOGBOOK.md` — work log (portfolio-grade).
- `PROGRESS_LOG_DAILY.md` — daily timeline.
- `RISK_LOG.md` — risk register.
- `docs/logs/` — operational registers (issues, decisions, experiments, review log).
- `data/reference/` — frozen reference datasets (constituents universe, events stubs).

---

## 3) Where to look if you have 5 minutes

1. `README.md`
2. `docs/dashboards/V2/exports/v2_page_01_footsie_pulse_overview.png`
3. `v2_modernisation_realtime/data/mart/market_overview.*`
4. `v2_modernisation_realtime/monitoring/reports/pipeline_runs_last14d.csv`
5. `v2_modernisation_realtime/bi_powerbi/exports/` (executive visuals)

