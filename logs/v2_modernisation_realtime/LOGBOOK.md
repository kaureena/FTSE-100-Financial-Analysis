# LOGBOOK — V2 Modernisation Platform

Timezone: Europe/London  
Objective: Provide a platform-grade modernisation of the dissertation baseline:
- medallion architecture (bronze/silver/gold)
- marts and semantic layer
- monitoring and governance (DQ, latency, incident timeline)
- premium “UK market terminal” dashboards (22 pages)
- Power BI export pack for recruiter-friendly visuals

---

## Build philosophy
V2 aims for “real-time feel” while remaining reproducible:
- marts are the source of truth for exports
- run registers and audits provide operational credibility

---

## 2026-02-15 — Mart-only exports
Updated export pipeline to enforce:
- **Exports are produced solely from mart parquet**
- Missing marts cause a clear failure (no silent fallbacks)

Evidence:
- `v2_modernisation_realtime/data/mart/`
- `docs/dashboards/V2/exports/`
- `logs/v2_modernisation_realtime/EXPORT_AUDIT.csv`

---

## 2026-02-16 — Terminal realism
Added:
- Constituents universe snapshot (tickers/sectors/demo weights)
- Events calendar stub (macro + earnings + optional news)

Evidence:
- `data/reference/*`
- `v2_modernisation_realtime/data/gold/events_calendar.*`
- `logs/v2_modernisation_realtime/UNIVERSE_REFRESH_LOG.csv`

---

## 2026-02-14 — Warehouse completion
- Marts materialised and DuckDB warehouse populated
Evidence:
- `v2_modernisation_realtime/db/warehouse.duckdb`
- `logs/v2_modernisation_realtime/WAREHOUSE_LOAD_LOG.md`
