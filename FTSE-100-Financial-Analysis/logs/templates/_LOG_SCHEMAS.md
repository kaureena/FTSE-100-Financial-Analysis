# Log Schemas (Reference)

This file defines the expected columns and meaning for the CSV logs in this pack.

## ISSUE_REGISTER.csv
Columns:
- `issue_id` — stable ID (e.g., ISSUE-012)
- `date_opened` — YYYY-MM-DD (Europe/London)
- `workstream` — V1 / V2 / Repo
- `component` — data / model / dashboard / monitoring / docs / CI
- `summary` — short description
- `severity` — Low / Medium / High / Critical
- `status` — Open / Mitigated / Closed
- `owner` — name/role
- `evidence_path` — repo path(s) where fix is evidenced
- `root_cause` — brief root cause category
- `resolution` — brief resolution summary
- `date_closed` — YYYY-MM-DD or blank if open

## PIPELINE_RUN_REGISTER.csv (V2)
- `run_id` — stable identifier
- `run_timestamp_london` — ISO timestamp displayed in London time
- `data_source` — snapshot / yahoo / stooq / alphavantage / polygon
- `window_start` / `window_end` — YYYY-MM-DD
- `status` — Success / Failed / Partial
- `duration_seconds` — total runtime
- `rows_bronze` / `rows_silver` / `rows_gold` / `rows_mart` — row counts
- `dq_score` — 0–100
- `exports_count` — number of PNG exports produced
- `notes` — short free-text notes

## EXPORT_AUDIT.csv (V1/V2)
- `page_id` — e.g., V1-P01, V2-P12
- `export_path` — relative path
- `expected_resolution` — e.g., 3840x2160
- `actual_resolution` — e.g., 3840x2160
- `status` — PASS / WARN / FAIL
- `notes` — comments and remediation

## DAILY_TIMELOG.csv
- `date` — YYYY-MM-DD
- `workstream` — Repo / V1 / V2
- `category` — data / model / dashboards / monitoring / docs / QA / ops
- `task` — short task name
- `hours` — float
- `evidence_path` — repo path(s)
