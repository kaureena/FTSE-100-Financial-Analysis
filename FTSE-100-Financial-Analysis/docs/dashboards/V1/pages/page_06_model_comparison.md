---
page_id: V1-P06
page_name: Model Comparison & Metrics
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

# Model Comparison & Metrics

## 1) Purpose
**One sentence purpose:**  
> Compare ARIMA and LSTM using consistent metrics (MAE/RMSE) and a single reconciliation table.

**Why this page exists (business value):**
- Provides a single ‘winner/loser’ summary with evidence-based metrics.
- Shows trade-offs: interpretability vs non-linear accuracy.
- Creates the bridge to V2 modernisation (backtesting + monitoring).

---

## 2) Primary questions this page answers
1. Which model performs better on this session and horizon?
2. Is the improvement consistent across horizons (1–10 steps)?
3. Are differences concentrated around specific volatility regimes?

---

## 3) Intended audience & usage pattern
**Audience:** Hiring manager / ML reviewer  
**Typical usage:** Model comparison (snapshot)  
**Decision context:** Evaluation summary

---

## 4) Data sources & contracts

### 4.1 Inputs (tables/files)
| Input | Grain | Source | Refresh | Contract |
|------|------|--------|---------|----------|
| v1_dissertation_baseline/outputs/metrics/arima_metrics.json | run | ARIMA metrics | on model run | [METRICS_LIBRARY.md#forecast-metrics](../../../../METRICS_LIBRARY.md#forecast-metrics) |
| v1_dissertation_baseline/outputs/metrics/lstm_metrics.json | run | LSTM metrics | on model run | [METRICS_LIBRARY.md#forecast-metrics](../../../../METRICS_LIBRARY.md#forecast-metrics) |
| v1_dissertation_baseline/outputs/tables/model_comparison.csv | run | Compiled comparison | on export | [DATA_CONTRACTS.md#v1-model-comparison](../../../../DATA_CONTRACTS.md#v1-model-comparison) |

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
| Best Model (by RMSE) | Model with lower RMSE on default horizon | argmin(RMSE) | Informational | Tie-breaker: MAE |
| RMSE Δ (%) | Percent RMSE improvement of LSTM over ARIMA | (RMSE_arima - RMSE_lstm)/RMSE_arima * 100 | Higher is better | Report negative if ARIMA wins |
| MAE Δ (%) | Percent MAE improvement of LSTM over ARIMA | (MAE_arima - MAE_lstm)/MAE_arima * 100 | Higher is better | Provide horizon-level table |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_rmse`  
  - **Definition:** Root Mean Square Error  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    RMSE = sqrt(mean((y - yhat)^2))
    ```

- **Measure 02:** `m_mae`  
  - **Definition:** Mean Absolute Error  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    MAE = mean(|y - yhat|)
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
| V1 | Table | Model Comparison Table (by horizon) | model_comparison.csv | Single truth table | Sort + highlight best |
| V2 | Bar | MAE by model | model_comparison.csv | Quick comparison | Hover |
| V3 | Bar | RMSE by model | model_comparison.csv | Quick comparison | Hover |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | This session day | Applies to all visuals unless noted |
| Interval | dropdown | 1m | Intraday vs daily controls |
| Horizon | dropdown | 1–10 steps | Forecast pages only |
| View mode | toggle | Replay | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V1-P04 ARIMA Forecast
  - V1-P05 LSTM Forecast
- **Cross-page filter behaviour:** Cross-page filters: enabled (horizon selection)

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
**Refresh cadence:** snapshot (compiled after model run)  
**Expected runtime:** < 15s  
**Freshness SLA:** N/A (snapshot)  
**Latency notes:** Make sure both models evaluate on the same timestamps

---

## 12) Interpretation guide (how to read the page)
- Use MAE as ‘typical error’ and RMSE as ‘penalise big misses’; interpret both together.
- If LSTM improves RMSE but not MAE, it may reduce large errors but keep typical errors similar.
- Use this page to justify V2 improvements (walk-forward backtesting, monitoring, richer features).

> Keep interpretation factual; avoid “buy/sell” advice.

---

## 13) Compliance & disclaimers
- **Not financial advice.**  
- Data sources and limitations: `DATA_README.md`  
- Privacy: no personal data processed.

---

## 14) Screenshot/export references

**High-res export file(s):**
- `docs/dashboards/V1/exports/v1_page_06_model_comparison.png`

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
**What this page does:** collapses model evaluation into a single decision: which model is better for which horizon.
**How to read:**
- Compare MAE/RMSE by horizon step (1..H).
- If lines cross, you may choose a hybrid: ARIMA for very short horizon, LSTM for longer horizon.
- Always interpret with DQ context (V1-P07).

### Dissertation traceability (V1)
- Maps to dissertation comparison: LSTM achieved lower MAE/RMSE than ARIMA on the sample shown.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V1-P06. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| model_name | string | LSTM | ARIMA | LSTM |
| horizon_step | int | 1 | 1..H |
| mae | float | 0.8 | points |
| rmse | float | 1.1 | points |
| sample_n | int | 10 | number of forecast points |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- **Metric tooltip:** model, horizon, MAE, RMSE, sample_n, evaluation window.

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
- Small sample sizes can make differences look large → show sample_n and interpret cautiously.
- Metric scale changes by interval (1m vs 5m) → lock interval for V1 comparison.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- Recompute MAE/RMSE from forecast_output and match within tolerance.
- Ensure horizon list is consistent across models.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- **Dashboard:** include an “Executive callout” card: “Winner: LSTM (lower MAE/RMSE)” with caveats.
- **Exports:** include the exact horizon and interval in the subtitle.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
