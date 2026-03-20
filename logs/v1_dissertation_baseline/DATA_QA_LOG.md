# DATA QA LOG — V1

This log documents the **data trust gate** for the V1 intraday dataset.

## Checks performed (per run)
1) Timestamp continuity (expected 1-minute cadence within session window)
2) Duplicate timestamps
3) OHLC sanity:
   - high >= max(open, close)
   - low  <= min(open, close)
   - volume >= 0
4) Outlier scan (return spikes)
5) Null scan (required columns present)

## Findings summary
- Dataset is mostly clean and consistent.
- Any gaps are explicitly:
  - recorded in `time_gap_report.csv`
  - surfaced in the DQ dashboard page (V1-P07)

## Remediation rules
- If gaps exist:
  - do **not** interpolate silently for modelling
  - flag gaps; optionally drop windows that cross large gaps for sequence modelling
- If OHLC sanity fails:
  - treat dataset as invalid until corrected

## Evidence
- `v1_dissertation_baseline/outputs/metrics/time_gap_report.csv`
- `v1_dissertation_baseline/outputs/metrics/dq_snapshot.json`
- `docs/dashboards/V1/exports/v1_page_07_data_quality_snapshot.png`
