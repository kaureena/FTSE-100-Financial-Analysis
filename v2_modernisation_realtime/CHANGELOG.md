# V2 Changelog (Modern Platform)

## V2.2 — 2026-02-19
- Added Power BI export evidence pack under `bi_powerbi/exports/` with donut/gauge visuals.
- Added governance logs under `docs/logs/` and repo root.
- Confirmed exports read from `data/mart/*.parquet` only (semantic layer discipline).

## V2.1 — 2026-02-17
- Added constituents universe loader + events enrichment stub.
- Materialised `mart.*` layer and populated `warehouse.duckdb`.

## V2.0 — 2026-02-16
- Introduced medallion tables + monitoring reports + premium export pack.

