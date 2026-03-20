# LOGBOOK — Repo-wide (V1 + V2)

Timezone: **Europe/London**  
Scope: Repo-wide narrative log (V1 dissertation baseline + V2 modernisation platform)  
Audience: Reviewer / Hiring manager / Maintainer (Reena)

---

## Guiding principle
This repo is designed to feel like a **UK-market analytics product**, not a classroom scaffold:
- V1 demonstrates dissertation baseline reproducibility (visualisation + ARIMA/LSTM)
- V2 demonstrates platform-grade modernisation (marts, monitoring, governance, terminal feel)

---

## 2026-02-17 — Governance hardening (logs expansion)
**Objective**
- Consolidate governance artefacts into a single `logs/` folder and make them audit-ready.

**Actions completed**
- Standardised log schemas (Issue register, Run register, Export audit).
- Expanded logbooks and progress logs with evidence path references.
- Added/extended time tracking: daily timelog, weekly rollups, hours breakdown.

**Evidence paths**
- `logs/repo_root/*`
- `logs/v1_dissertation_baseline/*`
- `logs/v2_modernisation_realtime/*`

**Notes**
- This step is deliberately “enterprise dense” because the repo is positioned as a UK Master’s project.

---

## 2026-02-16 — Terminal realism: constituents + events enrichment
**Objective**
- Make the platform feel like a UK market terminal by adding:
  - a constituents universe (tickers, sectors, weights)
  - a market events calendar stub (macro + earnings + optional news headlines)

**Actions completed**
- Introduced offline-first constituents snapshot and loader.
- Built unified events calendar with a consistent schema.

**Evidence paths**
- `data/reference/ftse100_constituents_universe_snapshot.csv`
- `data/reference/uk_macro_calendar_stub.csv`
- `data/reference/ftse100_earnings_calendar_stub_top25.csv`
- `v2_modernisation_realtime/data/gold/events_calendar.*`

**Risks tracked**
- Weights are “portfolio demo weights” (not official FTSE Russell). Tracked in `logs/*/RISK_LOG.md`.

---

## 2026-02-15 — Mart-only exports (spec fidelity)
**Objective**
- Ensure dashboard exports are produced strictly from marts (single source of truth).

**Actions completed**
- Export generation updated to read only from:
  - `v2_modernisation_realtime/data/mart/*.parquet`
- Export audit added (PASS/FAIL rules) and linked into daily QA.

**Evidence paths**
- `v2_modernisation_realtime/data/mart/`
- `docs/dashboards/V2/exports/`
- `logs/v2_modernisation_realtime/EXPORT_AUDIT.csv`

---

## 2026-02-14 — Platform completion: marts + DuckDB warehouse
**Objective**
- Convert medallion zones into a queryable warehouse, with marts.

**Actions completed**
- Materialised marts.
- Loaded bronze/silver/gold/mart into DuckDB.
- Added run register to support an operational narrative.

**Evidence paths**
- `v2_modernisation_realtime/db/warehouse.duckdb`
- `v2_modernisation_realtime/data/mart/`
- `logs/v2_modernisation_realtime/PIPELINE_RUN_REGISTER.csv`

---

## 2026-02-05 — V1 baseline completion
**Objective**
- Deliver dissertation-aligned baseline:
  - intraday visuals
  - ARIMA and LSTM forecasts
  - metrics and comparison
  - 7-page dashboard export pack

**Actions completed**
- Built V1 pipeline:
  - raw → processed → features → models → exports
- Produced DQ artefacts and evaluation metrics.

**Evidence paths**
- `v1_dissertation_baseline/data/*`
- `v1_dissertation_baseline/outputs/*`
- `docs/dashboards/V1/exports/*`

---

## Open questions (tracked in Issue Register)
- Add a “real provider” run schedule for a fully live demo (optional).
- Expand constituents beyond snapshot (add refresh mechanism with clear licensing).
- Expand events calendar from stub → integration (macro calendar API + earnings feed) if data access is available.

See: `logs/repo_root/ISSUE_REGISTER.csv`
