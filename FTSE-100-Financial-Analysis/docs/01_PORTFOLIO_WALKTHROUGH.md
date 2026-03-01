# Portfolio Walkthrough (UK Market Terminal Narrative)

This repo is designed to be reviewed like a **mini-market terminal**.

---

## 10-minute walkthrough (recommended for interviews)

### Step 1 — Start with the story
- Read `README.md` (2 minutes)
- Skim `CHANGELOG.md` (1 minute)

### Step 2 — Show the evidence pack (screenshare-friendly)
Open these in order:

1. **V2 Page 01 — Footsie Pulse Overview**  
   `docs/dashboards/V2/exports/v2_page_01_footsie_pulse_overview.png`

2. **V2 Page 03 — Volatility Regimes**  
   `docs/dashboards/V2/exports/v2_page_03_volatility_regimes.png`

3. **V2 Page 10 — Forecasting Cockpit**  
   `docs/dashboards/V2/exports/v2_page_10_forecasting_cockpit.png`

4. **V2 Page 18 — Pipeline Health**  
   `docs/dashboards/V2/exports/v2_page_18_pipeline_health.png`

Optional executive-style pages:
- `v2_modernisation_realtime/bi_powerbi/exports/pbi_page_06_exec_board_pack.png`

### Step 3 — Prove it’s not just visuals
- Open `v2_modernisation_realtime/data/mart/market_overview.csv`
- Open `v2_modernisation_realtime/data/mart/pipeline_health.csv`
- Open `v2_modernisation_realtime/monitoring/reports/dq_latest_session.csv`

This demonstrates:
- **Semantic layer discipline** (dashboard pages map to marts)
- **Operational monitoring** (latency, drift, incidents)
- **Auditability** (run register + logs)

---

## 30-minute walkthrough (deep dive)

### V1 (Dissertation baseline)
- `v1_dissertation_baseline/docs/diagrams/v1_data_pipeline.png`
- `v1_dissertation_baseline/docs/Dashboards/` (neon-framed V1 evidence pack)
- `v1_dissertation_baseline/outputs/metrics/model_comparison.csv`

### V2 (Platform)
- `docs/mermaid/01_end_to_end_architecture.mmd`
- `docs/mermaid/02_data_lineage_medallion.mmd`
- `v2_modernisation_realtime/data/mart/` (tables)
- `v2_modernisation_realtime/db/warehouse.duckdb`

### Governance realism (optional, but “premium”)
- `LOGBOOK.md`
- `PROGRESS_LOG_DAILY.md`
- `RISK_LOG.md`
- `docs/logs/DECISIONS_LOG.md`
- `docs/logs/dashboard_review_log.md`

---

## Suggested “talk track” (how Reena can present this)
- “V1 mirrors my dissertation workflow: intraday visuals + ARIMA/LSTM forecasting with a short horizon.”
- “V2 modernises the same idea into a production-style platform with marts, monitoring, and audit logs.”
- “Every dashboard is reproducible: it reads from a curated semantic layer (`mart.*`) and exports consistently at 4K.”

