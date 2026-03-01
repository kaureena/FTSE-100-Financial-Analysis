# DECISIONS LOG (ADR-lite)

This is a lightweight architecture decision record (ADR) list.

| Decision ID | Date | Decision | Alternatives considered | Rationale | Status | Evidence/Link |
| --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-01-28 | Split into V1 (dissertation baseline) + V2 (modernisation platform) | Single combined pipeline only | Clear narrative: academic baseline + enterprise upgrade | Accepted | CHANGELOG.md |
| DEC-002 | 2024-08-08 | Use 7-page V1 dashboard pack aligned to visuals + ARIMA/LSTM | Only notebooks, no dashboard exports | Portfolio readability: hiring managers prefer exports | Accepted | docs/dashboards/V1/exports |
| DEC-003 | 2026-02-14 | Materialise marts + DuckDB warehouse | Keep everything as CSV/plots only | Enterprise realism: marts/warehouse standard | Accepted | v2_modernisation_realtime/db/warehouse.duckdb |
| DEC-004 | 2026-02-15 | V2 exports read exclusively from mart parquet | Exports from gold/silver or in-memory frames | Spec fidelity and single source of truth | Accepted | v2_modernisation_realtime/data/mart |
| DEC-005 | 2026-02-16 | Constituents & events as offline-first stubs with clear labelling | Live feeds requiring keys/subscriptions | Keep repo runnable and reproducible; avoid external dependencies | Accepted | data/reference/* |

## Decision quality rules
- Every decision must list at least one alternative.
- Every accepted decision must reference where it is evidenced in the repo.
