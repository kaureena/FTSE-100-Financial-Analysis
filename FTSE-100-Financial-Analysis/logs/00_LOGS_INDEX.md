# Logs Index

Use this index to navigate the logging artefacts quickly.

## 1) Repo-wide logs (`logs/repo_root/`)
- `CHANGELOG.md` — consolidated release notes for all iterations (V1 and V2)
- `LOGBOOK.md` — narrative execution diary (day-by-day)
- `PROGRESS_LOG_DAILY.md` — daily timeline in a structured table
- `PROGRESS_LOG_WEEKLY.md` — weekly roll-up (outcomes, lessons, next week plan)
- `RISK_LOG.md` — risk register (likelihood × impact + mitigation)
- `ISSUE_REGISTER.csv` — issue tracker (severity, owner, status, evidence path)
- `DECISIONS_LOG.md` — ADR-lite decisions log (alternatives + rationale)
- `ASSUMPTIONS_LOG.md` — explicit assumptions and “what would invalidate this”
- `STAKEHOLDER_COMMS_LOG.md` — stakeholder comms timeline (requests, responses)
- `MEETING_NOTES.md` — meeting minutes (agenda → decisions → actions)
- `REPO_AUDIT_LOG.md` — audit trail of structure/content checks and outcomes
- `KPI_THRESHOLDS_CHANGELOG.md` — how KPI/threshold rules evolved
- `RELEASE_CHECKLIST.md` — pre-release checklist with sign-off blocks
- `HANDOVER_NOTES.md` — handover to Reena / reviewer

Time tracking:
- `DAILY_TIMELOG.csv` — daily time log (by workstream)
- `WEEKLY_HOURS.csv` — weekly hours summary
- `HOURS_BREAKDOWN.csv` — detailed breakdown by task

## 2) V1 logs (`logs/v1_dissertation_baseline/`)
- V1-specific versions of changelog/logbook/progress/risk/issues/hours
- `DATA_REFRESH_LOG.csv` — data pulls/snapshots used for V1
- `DATA_QA_LOG.md` — V1 DQ gate narrative + findings
- `FEATURE_ENGINEERING_LOG.md` — features derived and why
- `MODEL_EXPERIMENT_LOG.csv` — ARIMA/LSTM experiments & metrics
- `MODEL_EVAL_LOG.csv` — evaluation runs (MAE/RMSE etc.) per horizon
- `INTERPRETABILITY_LOG.md` — SHAP surrogate and limitations log
- `EXPORT_AUDIT.csv` — V1 exports audit (resolution, checksum, status)

## 3) V2 logs (`logs/v2_modernisation_realtime/`)
- V2-specific versions of changelog/logbook/progress/risk/issues/hours
- `PIPELINE_RUN_REGISTER.csv` — end-to-end run register (run_id, status, duration)
- `PIPELINE_STAGE_DURATIONS.csv` — stage-level timings (ingest/etl/dq/model/export)
- `DQ_RUN_LOG.csv` — DQ run outcomes, rule pass rates
- `DQ_ISSUE_REGISTER.csv` — DQ issues and their remediation notes
- `INCIDENT_REGISTER.csv` — incidents (DQ breach, stale data, export failure)
- `SLA_LATENCY_REPORT.md` — SLA and latency narrative with action plan
- `LATENCY_SAMPLES.csv` — raw samples used for SLA reporting
- `MART_BUILD_LOG.md` — mart build trace (inputs → outputs → rowcounts)
- `WAREHOUSE_LOAD_LOG.md` — DuckDB load trace and validation checks
- `UNIVERSE_REFRESH_LOG.csv` — constituents universe source and validation
- `EVENTS_CALENDAR_LOG.csv` — macro/earnings/news event feed updates
- `NEWS_STUB_LOG.csv` — news stub updates and curation rules
- `MODEL_REGISTRY_LOG.csv` — model registry/versioning decisions
- `MODEL_MONITORING_LOG.csv` — drift/error monitoring snapshots
- `BACKTESTING_RUN_LOG.csv` — walk-forward backtests and results summaries
- `EXPORT_AUDIT.csv` — V2 exports audit (resolution, status, page-by-page)
- `POWERBI_EXPORT_QA_LOG.md` — Power BI export pack QA notes
- `DASHBOARD_REVIEW_LOG.md` — page-by-page review notes and fixes

## 4) Templates (`logs/templates/`)
- `_LOG_SCHEMAS.md` — CSV schema definitions for all logs (column meaning)
- `_LOGGING_RULES.md` — how to write logs consistently and keep them credible
