# MART BUILD LOG — V2

This log documents how marts are produced from gold datasets.

## Mart principles
- Marts must be:
  - stable in schema
  - optimised for dashboard consumption
  - documented in DATA_CONTRACTS.md (in main repo)

## Mart mapping (high level)
- `mart.market_overview`
  - Source: `gold.ftse100_daily` + derived returns/vol
  - Purpose: top-level overview KPIs and trend series

- `mart.intraday_terminal`
  - Source: `silver.ftse100_intraday`
  - Purpose: candles/volume/VWAP proxy

- `mart.data_quality_health`
  - Source: DQ outputs
  - Purpose: trust banner and DQ scorecards

- `mart.pipeline_health`
  - Source: run register + stage durations
  - Purpose: ops dashboard (SLA, durations, failures)

## Validation checks
- Rowcount sanity (no unexpected drops)
- Key uniqueness
- Date/timestamp alignment and timezone normalisation
- No “nan” strings in categorical fields

## Evidence paths
- `v2_modernisation_realtime/data/mart/*.parquet`
- `logs/v2_modernisation_realtime/PIPELINE_RUN_REGISTER.csv`
