# DATA_CONTRACTS — Source of Truth for Schemas & Grain

This file defines **what data must look like** so dashboards and models are reproducible.

---

## V1 contracts (Dissertation baseline)

### V1 intraday 1m (clean)
<a id="v1-intraday-1m"></a>

**Dataset name:** `ftse100_intraday_1m_clean`  
**Typical file:** `v1_dissertation_baseline/data/processed/ftse100_intraday_1m_clean.parquet`  
**Grain:** 1 row per `timestamp` (1 minute)  

| Field | Type | Required | Rules |
|------|------|----------|------|
| timestamp | datetime | Yes | Must be timezone-aware (UTC preferred) |
| open | float | Yes | points; >= 0 |
| high | float | Yes | high >= max(open, close) |
| low | float | Yes | low <= min(open, close) |
| close | float | Yes | points; >= 0 |
| volume | float/int | Optional | non-negative; treat as proxy for index activity |

**Primary key:** `timestamp`  
**DQ gates:** duplicates=0, gaps flagged, OHLC sanity must pass.

---

### V1 volume flags
<a id="v1-volume-flags"></a>

**Dataset name:** `volume_spike_flags`  
**Typical file:** `v1_dissertation_baseline/outputs/metrics/volume_spike_flags.csv`  
**Grain:** 1 row per `timestamp`  

| Field | Type | Required | Rules |
|------|------|----------|------|
| timestamp | datetime | Yes | aligns to intraday bars |
| volume | float/int | Yes | from intraday dataset |
| spike_flag | bool | Yes | True if volume >= p95(volume) (configurable) |
| spike_rank | int | Optional | rank of volume (descending) |

---

### V1 moving average features
<a id="v1-features"></a>

**Dataset name:** `moving_average_features`  
**Typical file:** `v1_dissertation_baseline/outputs/tables/moving_average_features.parquet`  
**Grain:** 1 row per `timestamp`  

| Field | Type | Required | Rules |
|------|------|----------|------|
| timestamp | datetime | Yes | aligns to intraday bars |
| close | float | Yes | points |
| ma20 | float | Yes | 20-bar moving average of close |
| ma_gap | float | Yes | close - ma20 |
| crossover_flag | bool | Optional | True when sign(close-ma20) changes |

---

### V1 forecasts
<a id="v1-forecasts"></a>

**Dataset name:** `forecast_output`  
**Typical files:**  
- `v1_dissertation_baseline/outputs/forecasts/arima_forecast.csv`  
- `v1_dissertation_baseline/outputs/forecasts/lstm_forecast.csv`  

**Grain:** 1 row per (`origin_timestamp`, `horizon_step`)  

| Field | Type | Required | Rules |
|------|------|----------|------|
| origin_timestamp | datetime | Yes | time forecast was issued |
| target_timestamp | datetime | Yes | time being forecasted |
| horizon_step | int | Yes | 1..H |
| y_true | float | Yes | actual close at target_timestamp |
| yhat | float | Yes | predicted close |
| model_name | string | Yes | "ARIMA" or "LSTM" |
| residual | float | Optional | y_true - yhat |

**Alignment rule:** `target_timestamp` must match the actual series timestamps exactly.

---

### V1 model comparison
<a id="v1-model-comparison"></a>

**Dataset name:** `model_comparison`  
**Typical file:** `v1_dissertation_baseline/outputs/tables/model_comparison.csv`  
**Grain:** 1 row per (`model_name`, `horizon_step`)  

| Field | Type | Required |
|------|------|----------|
| model_name | string | Yes |
| horizon_step | int | Yes |
| mae | float | Yes |
| rmse | float | Yes |
| sample_n | int | Optional |

---

### V1 DQ outputs
<a id="v1-dq"></a>

**Dataset name:** `dq_snapshot`  
**Typical files:**  
- `v1_dissertation_baseline/outputs/metrics/dq_snapshot.json`  
- `v1_dissertation_baseline/outputs/tables/gap_report.csv`

**Grain:** run-level + gap-level

Minimum fields include:
- missing_bar_count
- duplicate_timestamp_count
- ohlc_sanity_fail_count
- max_gap_minutes

---

## V2 contracts (Modernised platform)

### V2 marts (dashboard-ready)
<a id="v2-marts"></a>

All V2 dashboards should read from `mart.*` tables.
Each mart has:
- a declared **grain**
- a declared **freshness SLA**
- a declared **owner**
- a declared **contract status** (draft/approved/deprecated)

#### Example: `mart.market_overview`
**Grain:** (`timestamp`, `interval`)  
Minimum fields:
- timestamp_london (datetime)
- interval (string: 1m/5m/1d)
- close (float, points)
- prev_close (float, points)
- delta_pct (float)
- session_high (float)
- session_low (float)
- realised_vol_20 (float)
- run_id (string)
- freshness_minutes (int)

#### Example: `mart.pipeline_health`
**Grain:** (`run_id`)  
Minimum fields:
- run_id
- started_at
- finished_at
- status (success/fail)
- stage_durations_json
- sla_breach_flag
- version_tag

> Additional marts are defined in their page specs. This contract section is the minimum standard.

---

## Contract governance

### Breaking-change rules
- Changing a field name is a breaking change.
- Changing a field meaning (units / grain) is a breaking change.
- Breaking changes require:
  - Release note entry (V2-P22)
  - Version bump
  - Backfill plan (if applicable)

### Contract review checklist
- [ ] Grain declared and enforced
- [ ] Primary key defined
- [ ] Nullability defined
- [ ] Timezone rules explicit
- [ ] DQ gates defined
---

## V2 (Gold) — Reference & Enrichment tables

### `gold.ftse100_constituent_universe`

| Column | Type | Description |
|---|---|---|
| ticker | string | Yahoo-style ticker (e.g., `AZN.L`) |
| epic | string | LSE EPIC ticker (public sources) |
| company_name | string | Display name |
| icb_sector | string | Source sector label |
| sector | string | Broad sector mapping (dashboard palette) |
| index_weight | float | Portfolio/demo weight (sums to 1.0) |
| as_of_date | date | Snapshot date |
| source | string | Snapshot source |

### `gold.events_calendar`

| Column | Type | Description |
|---|---|---|
| event_id | string | Stable identifier for event row |
| event_type | string | `macro` / `earnings` / `news` |
| timestamp_local | timestamp | Local timestamp (Europe/London) |
| date | date | Convenience date key |
| category | string | e.g., Inflation, Central Bank, Earnings |
| impact | string | `low` / `medium` / `high` |
| event_name | string | Macro/earnings label |
| ticker | string | For earnings rows only |
| headline | string | For news rows only |
| sentiment | string | Optional label |
| is_stub | boolean | Whether row is a stub (portfolio) |
| source | string | Provider/source label |

### V2 marts (dashboard-ready)

All V2 dashboard pages reference `mart.*` tables. These are materialised under:

- `v2_modernisation_realtime/data/mart/*.parquet`
- `v2_modernisation_realtime/data/mart/*.csv`

Core marts referenced by the spec pack:

- `mart.alerts_register`
- `mart.backtesting_report`
- `mart.board_pack`
- `mart.correlation_matrix`
- `mart.correlation_pairs`
- `mart.data_inventory`
- `mart.data_quality_health`
- `mart.data_usage_map`
- `mart.dq_issue_register`
- `mart.drawdown_risk`
- `mart.failure_impact`
- `mart.forecasting_cockpit`
- `mart.forecasting_metrics`
- `mart.incident_register`
- `mart.incident_timeline`
- `mart.intraday_terminal`
- `mart.kpi_dictionary`
- `mart.kpi_usage_map`
- `mart.latency_sla`
- `mart.lineage_details`
- `mart.lineage_map`
- `mart.market_overview`
- `mart.measure_catalogue`
- `mart.measure_dependencies`
- `mart.measure_usage_map`
- `mart.model_monitoring`
- `mart.model_runs`
- `mart.pipeline_health`
- `mart.release_impacts`
- `mart.release_kpi_trends`
- `mart.release_versions`
- `mart.sector_rotation`
- `mart.technical_indicators`
- `mart.top_movers`
- `mart.volatility_regimes`
