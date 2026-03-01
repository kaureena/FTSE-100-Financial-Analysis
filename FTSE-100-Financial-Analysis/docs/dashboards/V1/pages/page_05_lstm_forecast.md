---
page_id: V1-P05
page_name: LSTM Forecast (Short Horizon)
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

# LSTM Forecast (Short Horizon)

## 1) Purpose
**One sentence purpose:**  
> Show LSTM short-horizon forecasting performance, including error bands and interpretability notes.

**Why this page exists (business value):**
- Demonstrates the non-linear sequence model described in the dissertation (60-step lookback).
- Compares to ARIMA on equal horizons with common metrics.
- Introduces interpretability narrative (SHAP workaround) for portfolio credibility.

---

## 2) Primary questions this page answers
1. How well does LSTM forecast the next short horizon compared to ARIMA?
2. Does performance remain stable across calm vs volatile segments?
3. Which recent lags/features appear most influential (interpretability pack)?

---

## 3) Intended audience & usage pattern
**Audience:** Hiring manager / ML reviewer  
**Typical usage:** Forecast review + explainability (replay snapshot)  
**Decision context:** Model evaluation (sequence model)

---

## 4) Data sources & contracts

### 4.1 Inputs (tables/files)
| Input | Grain | Source | Refresh | Contract |
|------|------|--------|---------|----------|
| v1_dissertation_baseline/data/processed/ftse100_intraday_1m_clean.parquet | intraday_1m | Yahoo Finance snapshot | snapshot (frozen) | [DATA_CONTRACTS.md#v1-intraday-1m](../../../../DATA_CONTRACTS.md#v1-intraday-1m) |
| v1_dissertation_baseline/outputs/forecasts/lstm_forecast.csv | intraday_1m | Model output | on model run | [DATA_CONTRACTS.md#v1-forecasts](../../../../DATA_CONTRACTS.md#v1-forecasts) |
| v1_dissertation_baseline/outputs/metrics/lstm_metrics.json | run | Metrics output | on model run | [METRICS_LIBRARY.md#forecast-metrics](../../../../METRICS_LIBRARY.md#forecast-metrics) |

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
| MAE (LSTM) | Mean Absolute Error over forecast horizon | mean(|y - yhat|) | Lower is better | Compare directly to ARIMA |
| RMSE (LSTM) | Root Mean Square Error over horizon | sqrt(mean((y - yhat)^2)) | Lower is better | Sensitive to spikes |
| Stability (rolling MAE) | Rolling MAE over time | rolling_window(MAE) | Lower & stable | Used to identify regime sensitivity |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_lookback_window`  
  - **Definition:** Lookback length used for sequences  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    lookback = 60 (bars)
    ```

- **Measure 02:** `m_error_band`  
  - **Definition:** Error band proxy (e.g., ±1 std of residuals)  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    band = yhat ± std(residuals)
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
| V1 | Line | LSTM Forecast vs Actual (next N bars) | lstm_forecast.csv | Performance visibility | Toggle band |
| V2 | Line | Rolling Error (MAE/RMSE) | lstm_forecast.csv | Stability check | Hover |
| V3 | Bar | SHAP-like Feature Importance (proxy) | shap_proxy.csv (optional) | Explainability narrative | Hover |

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
  - V1-P04 ARIMA Forecast
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
**Refresh cadence:** snapshot (reproducible training)  
**Expected runtime:** < 5–10 min (CPU) or faster on GPU  
**Freshness SLA:** N/A (snapshot)  
**Latency notes:** Ensure scaling and sequence alignment are consistent across runs

---

## 12) Interpretation guide (how to read the page)
- Compare the LSTM forecast path to the actual series; focus on direction and turning-point timing.
- If rolling error spikes coincide with candle volatility clusters, note regime sensitivity.
- Explainability is approximate; use as trust-building narrative rather than strict causal inference.

> Keep interpretation factual; avoid “buy/sell” advice.

---

## 13) Compliance & disclaimers
- **Not financial advice.**  
- Data sources and limitations: `DATA_README.md`  
- Privacy: no personal data processed.

---

## 14) Screenshot/export references

**High-res export file(s):**
- `docs/dashboards/V1/exports/v1_page_05_lstm_forecast.png`

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
**LSTM role in V1:** capture non-linear temporal dependencies in intraday data for improved short-horizon forecasts.
**Interpretation:**
- Compare LSTM and ARIMA on the same horizon for fairness.
- Watch for overfitting signs (excellent in-sample, unstable out-of-sample).
- Use SHAP-proxy narrative carefully: interpretability is approximate when using a dense surrogate.

### Dissertation traceability (V1)
- Maps to dissertation modelling: LSTM trained on scaled close using a 60-step lookback; evaluated with MAE/RMSE; interpretability discussion via SHAP workaround.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V1-P05. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| origin_timestamp | datetime | 2024-09-05 11:00:00+00:00 | Forecast issue time |
| target_timestamp | datetime | 2024-09-05 11:05:00+00:00 | Forecast target time |
| horizon_step | int | 5 | 1..H |
| y_true | float | 8635.2 | Actual close |
| yhat | float | 8635.0 | LSTM forecast |
| abs_error | float | 0.2 | |y_true - yhat| |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- **Forecast tooltip:** target time, y_true, yhat, abs error, rolling MAE (optional).
- **Feature contribution tooltip (if surrogate SHAP shown):** top contributing lag buckets (e.g., last 5 mins, last 15 mins).

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
- Scaling mismatch (train scaler vs inference scaler) → produces unrealistic forecasts; must be locked and versioned.
- Random seed differences → forecast drift; fix seeds and document environment.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- Input sequence length (lookback) is fixed and documented (e.g., 60).
- Forecast rows align exactly to timestamps (no off-by-one).

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- **Python/Keras:** save model + scaler + hyperparams; log train/test window and run_id.
- **Dashboard:** avoid exposing too many ML terms; provide plain-language explanation + limitations.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
