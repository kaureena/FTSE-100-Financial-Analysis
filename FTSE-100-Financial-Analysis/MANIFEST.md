# Repository Manifest — FTSE 100 Financial Analysis

Generated: 2026-02-17 (Europe/London)

This manifest lists the key **portfolio evidence artefacts** shipped in the repo.

---

## 1) Evidence packs (dashboards)

### V1 (Dissertation baseline — 7 pages, 4K PNG)
- Folder: `docs/dashboards/V1/exports/`
- Also mirrored in: `v1_dissertation_baseline/docs/Dashboards/` (includes neon-framed variants)

Pages:
1. `v1_page_01_market_overview.png`
2. `v1_page_02_candles_volume.png`
3. `v1_page_03_moving_averages.png`
4. `v1_page_04_arima_forecast.png`
5. `v1_page_05_lstm_forecast.png`
6. `v1_page_06_model_comparison.png`
7. `v1_page_07_data_quality_snapshot.png`

### V2 (Modern terminal — 22 pages, 4K PNG)
- Folder: `docs/dashboards/V2/exports/`

### Power BI evidence pack (4K PNG)
- Folder: `v2_modernisation_realtime/bi_powerbi/exports/`

Pages:
1. `pbi_page_01_market_overview.png`
2. `pbi_page_02_sector_rotation.png`
3. `pbi_page_03_risk_drawdown.png`
4. `pbi_page_04_model_performance.png`
5. `pbi_page_05_pipeline_health.png`
6. `pbi_page_06_exec_board_pack.png`

---

## 2) Diagrams (V1 rendered)

Folder:
- `v1_dissertation_baseline/docs/diagrams/`

Included:
- `v1_data_pipeline.png`
- `v1_model_lifecycle.png`
- `v1_dashboard_lineage.png`

Repo-wide Mermaid source diagrams:
- `docs/mermaid/`

---

## 3) Data & semantic layer (V2)

### Medallion storage
- `v2_modernisation_realtime/data/bronze/`
- `v2_modernisation_realtime/data/silver/`
- `v2_modernisation_realtime/data/gold/`

### Dashboard-ready marts (CSV + parquet)
- `v2_modernisation_realtime/data/mart/`

### Local warehouse
- `v2_modernisation_realtime/db/warehouse.duckdb`

---

## 4) Monitoring (V2)

Folder:
- `v2_modernisation_realtime/monitoring/reports/`

Typical outputs:
- DQ session checks
- latency SLA tables
- drift proxy outputs
- pipeline run histories
- incident timeline

---

## 5) Governance / realism logs

Repo root:
- `CHANGELOG.md`
- `LOGBOOK.md`
- `PROGRESS_LOG_DAILY.md`
- `RISK_LOG.md`
- `WEEKLY_HOURS.csv`
- `HOURS_BREAKDOWN.csv`

Deep registers:
- `docs/logs/DECISIONS_LOG.md`
- `docs/logs/ASSUMPTIONS_LOG.md`
- `docs/logs/issue_register.csv`
- `docs/logs/model_experiment_log.csv`
- `docs/logs/dashboard_review_log.md`

V1 and V2 local copies:
- `v1_dissertation_baseline/` and `v2_modernisation_realtime/` contain the same log files for reviewer convenience.

---

## 6) Reference datasets (terminal realism)
- Constituents universe snapshot: `data/reference/ftse100_constituents_universe_snapshot.csv`
- Events stubs: `data/reference/events/`

---

## 7) Reviewer docs
- `docs/00_REPO_NAVIGATION.md`
- `docs/01_PORTFOLIO_WALKTHROUGH.md`
- `docs/02_UK_MARKET_CONTEXT.md`
- `docs/03_POWERBI_BUILD_GUIDE.md`
- `docs/04_DASHBOARD_DESIGN_SYSTEM.md`
- `docs/05_OPERATIONS_AND_MONITORING.md`
- `docs/06_DATA_GOVERNANCE_AND_LINEAGE.md`
- `docs/07_MODEL_CARDS.md`

