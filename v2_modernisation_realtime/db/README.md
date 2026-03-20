# Local Warehouse (DuckDB)

This DuckDB file is populated during the V2 build and mirrors the platform layers:

- bronze.* (raw ingest)
- silver.* (clean/enriched)
- gold.* (curated core tables)
- mart.* (dashboard-ready tables)

Open with DuckDB CLI / DBeaver / Python duckdb to query locally.
