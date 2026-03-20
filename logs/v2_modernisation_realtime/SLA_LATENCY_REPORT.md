# SLA & Latency Report — V2

## SLA definition (portfolio target)
- In-session freshness SLA: **<= 10 minutes**
- Daily close refresh SLA: **<= 24 hours**

## Latency components (measured)
- Ingestion latency
- Transform latency (bronze→silver→gold→mart)
- Export latency
- Warehouse load latency

## What we monitor
- `PIPELINE_RUN_REGISTER.csv` for total runtime and export counts
- `PIPELINE_STAGE_DURATIONS.csv` for bottlenecks
- `LATENCY_SAMPLES.csv` for raw observations

## Current status
- No SLA breaches recorded in sample runs.
- p95 latency is controlled by export rendering time; acceptable for portfolio demo.

## Action plan
1) If latency rises:
   - reduce export frequency
   - cache derived plots
   - precompute heavy aggregates into marts
2) If DQ fails:
   - block exports or mark as “DQ FAIL” on export footer/banner

## Evidence
- `logs/v2_modernisation_realtime/PIPELINE_RUN_REGISTER.csv`
- `logs/v2_modernisation_realtime/LATENCY_SAMPLES.csv`
