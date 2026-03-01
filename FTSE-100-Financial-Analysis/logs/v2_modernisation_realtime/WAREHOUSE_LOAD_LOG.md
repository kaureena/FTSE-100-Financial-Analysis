# WAREHOUSE LOAD LOG — DuckDB (V2)

## Objective
Provide a local warehouse (`warehouse.duckdb`) containing:
- bronze.* tables
- silver.* tables
- gold.* tables
- mart.* tables

## Load approach
1) Create schemas: bronze, silver, gold, mart
2) Create or replace tables from parquet/csv sources
3) Validate:
   - table exists
   - rowcount > 0 (where expected)
   - key uniqueness where applicable

## Validation queries (examples)
- `SHOW TABLES;`
- `SELECT COUNT(*) FROM mart.market_overview;`
- `SELECT MIN(date), MAX(date) FROM gold.ftse100_daily;`

## Evidence
- `v2_modernisation_realtime/db/warehouse.duckdb`
- `v2_modernisation_realtime/db/README.md`
