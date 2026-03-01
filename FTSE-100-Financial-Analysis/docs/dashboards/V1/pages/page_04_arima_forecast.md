---
page_id: V1-P04
page_name: ARIMA Forecast (Short Horizon)
version_track: V1
owner: Reena
last_updated: '2026-02-16'
status: Draft
audience:
- Hiring Manager
- BI Analyst
- Data Engineer
dashboard_tool: Mixed (Python + BI)
refresh_mode: snapshot (frozen)
primary_grain: intraday_1m
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# ARIMA Forecast (Short Horizon)

## 1) Purpose
**One sentence purpose:**  
> Show ARIMA short-horizon forecasting performance with side-by-side actual vs forecast and residual diagnostics.

**Why this page exists (business value):**
- Demonstrates the statistical baseline approach described in the dissertation.
- Provides an interpretable benchmark for comparing to LSTM.
- Highlights limitations: stationarity requirements and sensitivity to abrupt jumps.

---

## 2) Primary questions this page answers
1. How well does ARIMA forecast the next short horizon on intraday data?
2. Where do residuals cluster (bias during volatility spikes)?
3. Does the model under/over react during fast moves?

---

## 3) Intended audience & usage pattern
**Audience:** Hiring manager / analyst  
**Typical usage:** Forecast review (replay snapshot)  
**Decision context:** Model evaluation (baseline)

---

## 4) Data sources & contracts

### 4.1 Inputs (tables/files)
| Input | Grain | Source | Refresh | Contract |
|------|------|--------|---------|----------|
| v1_dissertation_baseline/data/processed/ftse100_intraday_1m_clean.parquet | intraday_1m | Yahoo Finance snapshot | snapshot (frozen) | [DATA_CONTRACTS.md#v1-intraday-1m](../../../../DATA_CONTRACTS.md#v1-intraday-1m) |
| v1_dissertation_baseline/outputs/forecasts/arima_forecast.csv | intraday_1m | Model output | on model run | [DATA_CONTRACTS.md#v1-forecasts](../../../../DATA_CONTRACTS.md#v1-forecasts) |
| v1_dissertation_baseline/outputs/metrics/arima_metrics.json | run | Metrics output | on model run | [METRICS_LIBRARY.md#forecast-metrics](../../../../METRICS_LIBRARY.md#forecast-metrics) |

> If an input is optional for this page (e.g., events overlay, constituents), mark it explicitly as **Optional**.

### 4.2 Timezone & session rules
- **All timestamps displayed in Europe/London** (GMT/BST as applicable).
- **Session framing:** London trading session (typically 08:00–16:30 local time).
- **Non-trading days:** weekends + UK bank holidays (handled via trading calendar where available).
- **Intraday bars:** expected to be continuous during session; gaps are flagged in DQ.

---

## 5) KPI tiles (definitions + thresholds)

| KPI | Definition | Calculation | Target/Threshold | Notes |
|-----|------------|-------------|------------------|------|
| MAE (ARIMA) | Mean Absolute Error over forecast horizon | mean(|y - yhat|) | Lower is better | Compare to LSTM on V1-P06 |
| RMSE (ARIMA) | Root Mean Square Error over horizon | sqrt(mean((y - yhat)^2)) | Lower is better | More sensitive to large errors |
| Residual bias | Mean residual (y - yhat) | mean(residual) | Close to 0 | Persistent bias indicates systematic under/over forecast |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_residual`  
  - **Definition:** Forecast residual at time t  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    residual_t = y_t - yhat_t
    ```

- **Measure 02:** `m_horizon_mae`  
  - **Definition:** MAE grouped by forecast horizon  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    MAE_h = mean(|y_{t+h}-yhat_{t+h}|)
    ```

---

## 7) Visual components (layout + intent)

### 7.1 Layout map
**Grid:** 12-column grid (recommended)  
**Header:** Title + London timestamp + freshness + run_id  
**Top row:** KPI tiles + headline chart  
**Mid row:** supporting charts  
**Bottom row:** breakdown table / diagnostics panel

### 7.2 Visual inventory
| Visual ID | Type | Title | Input(s) | Purpose | Interaction |
|-----------|------|-------|----------|---------|------------|
| V1 | Line | ARIMA Forecast vs Actual (next N bars) | arima_forecast.csv | Performance visibility | Toggle forecast bands |
| V2 | Bar | Residuals by time | arima_forecast.csv | Detect clustering | Hover |
| V3 | Histogram | Residual distribution | arima_forecast.csv | Check symmetry/heavy tails | Brush |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | This session day | Applies to all visuals unless noted |
| Interval | dropdown | 1m | Intraday vs daily controls |
| Horizon | dropdown | 10 steps (default) | Forecast pages only |
| View mode | toggle | Replay | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V1-P06 Model Comparison
  - V1-P07 Data Quality Snapshot
- **Cross-page filter behaviour:** Cross-page filters: enabled (date/session + horizon)

---

## 10) Data Quality (DQ) & trust signals

**DQ checks relevant to this page:**
- No duplicate timestamps per instrument per interval
- Timestamp monotonic increasing within session window
- OHLC sanity: high >= max(open, close) and low <= min(open, close); volume >= 0

**DQ outputs referenced (V2):**
- `v2_modernisation_realtime/dq_data_quality/reports/dq_report.html`
- `docs/logs/07_dq_issue_register.csv`

**If DQ fails:**
- Follow `v2_modernisation_realtime/monitoring/incident_playbook.md`

---

## 11) Refresh & performance expectations
**Refresh cadence:** snapshot (run-once, reproducible)  
**Expected runtime:** < 2 min training + export  
**Freshness SLA:** N/A (snapshot)  
**Latency notes:** Forecast horizon is short; align timestamps carefully

---

## 12) Interpretation guide (how to read the page)
- Focus on alignment of yhat with actual trend direction; inspect where divergence starts.
- Large RMSE spikes usually correspond to sharp discontinuities; cross-check candle page and DQ gaps.
- Residual bias away from 0 suggests ARIMA is systematically lagging or overshooting during regime shifts.

> Keep interpretation factual; avoid “buy/sell” advice.

---

## 13) Compliance & disclaimers
- **Not financial advice.**  
- Data sources and limitations: `DATA_README.md`  
- Privacy: no personal data processed.

---

## 14) Screenshot/export references

**High-res export file(s):**
- `docs/dashboards/V1/exports/v1_page_04_arima_forecast.png`

**Export requirements:**
- Resolution: **2560×1440 minimum** (preferred 3840×2160)
- Dark theme enabled (UK Neon Terminal style)
- Footer must include: `run_id` + London timestamp + freshness + disclaimer

---

## 15) Acceptance criteria (definition of done)
- [ ] Page renders without errors
- [ ] All KPIs reconcile with source tables/files within tolerance
- [ ] Filters behave as specified
- [ ] DQ checks referenced and pass (or issues logged)
- [ ] Export exists in `/exports/` and is linked from `page_index.md`
- [ ] Page has an interpretation guide + limitations notes

---

## 16) QA checklist (pre-release)
- [ ] Labels and units correct (points, %, GBP where applicable)
- [ ] No broken links
- [ ] Colour contrast acceptable
- [ ] Tooltip shows London time + units
- [ ] Re-run produces consistent results (snapshot or within tolerance)

---

## 17) Page narrative & storyboarding (premium UK trading-desk tone)
**ARIMA role in V1:** a transparent statistical baseline for short-horizon forecasts.
**Interpretation:**
- Compare predicted vs actual for the next 1–10 minutes.
- Residual plot indicates systematic bias (under/over prediction).
- Treat ARIMA as a benchmark, not the final best model.

### Dissertation traceability (V1)
- Maps to dissertation modelling: ARIMA trained on historical close, forecasting the next ~10 minutes; evaluated using MAE/RMSE.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V1-P04. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| origin_timestamp | datetime | 2024-09-05 11:00:00+00:00 | Forecast issue time |
| target_timestamp | datetime | 2024-09-05 11:05:00+00:00 | Forecast target time |
| horizon_step | int | 5 | 1..H |
| y_true | float | 8635.2 | Actual close |
| yhat | float | 8634.6 | ARIMA forecast |
| residual | float | 0.6 | y_true - yhat |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- **Forecast vs actual tooltip:** target time, y_true, yhat, absolute error, signed error.
- **Residual chart tooltip:** target time, residual, rolling residual mean (optional).

**Formatting defaults (unless page overrides):**
- Points: 1 decimal (e.g., `8,625.4`)
- Percent: 2 decimals with sign (e.g., `+0.27%`)
- Time: `DD Mon YYYY HH:MM` (Europe/London)
- Always show interval (1m/5m/1d) in subtitle when relevant.

**Interaction rules:**
- Cross-filter is allowed only when it clarifies (avoid “filter chaos”).
- Drilldowns must keep the user in the story (link to “What next?” in each page spec).
- If DQ is FAIL → show RED banner and block forecast interpretation.

---

## 20) Edge cases & failure modes (operational realism)
- Non-stationary behaviour can destabilise ARIMA → document differencing order and stationarity checks.
- Forecast outputs outside plausible intraday range → cap/band only if justified and documented.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- MAE/RMSE computed from the same forecast rows shown in the visual (no hidden filtering).
- Horizon steps are continuous and within 1..H.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- **Python:** Statsmodels ARIMA; persist model params + run_id; save forecasts to `outputs/forecasts/`.
- **Dashboard:** Display horizon controls and explicitly label them (e.g., “+5 minutes”).

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
