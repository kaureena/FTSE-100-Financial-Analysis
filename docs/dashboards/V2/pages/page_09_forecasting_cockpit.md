---
page_id: V2-P09
page_name: Forecasting Cockpit
version_track: V2
owner: Reena
last_updated: '2026-02-16'
status: Draft
audience:
- Hiring Manager
- BI Analyst
- Data Engineer
dashboard_tool: Mixed (Power BI + Python)
refresh_mode: Near real-time (in session) / Replay fallback
primary_grain: intraday_5m
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# Forecasting Cockpit

## 1) Purpose
**One sentence purpose:**  
> Central hub for forecasts: compare ARIMA/LSTM/V2 models, show yhat vs actual, confidence bands, and horizon metrics.

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. What do the models predict for the next horizon?
2. How confident is the forecast (bands / uncertainty proxy)?
3. Which model is currently most reliable under current regime?

---

## 3) Intended audience & usage pattern
**Audience:** Hiring manager / analyst  
**Typical usage:** Daily monitoring + intraday review  
**Decision context:** UK market analytics product

---

## 4) Data sources & contracts

### 4.1 Inputs (tables/files)
| Input | Grain | Source | Refresh | Contract |
|------|------|--------|---------|----------|
| mart.forecasting_cockpit | intraday/daily | Curated mart | every 30–60 minutes (session) + daily | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.forecasting_metrics | run | Curated mart | every 30–60 minutes (session) + daily | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.model_runs | run | Curated mart | every 30–60 minutes (session) + daily | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| Selected Model | Active model in cockpit | dropdown selection | Info | Defaults to best backtested model |
| Horizon MAE | MAE on selected horizon | MAE_h | Lower is better | Compare across models |
| Freshness | Minutes since last forecast run | now - last_run | Warn if > SLA | SLA defined in thresholds.yaml |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_forecast_band`  
  - **Definition:** Uncertainty band proxy  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    band = yhat ± 1.96*std(residuals_backtest)
    ```

- **Measure 02:** `m_best_model`  
  - **Definition:** Best model selection rule  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    best = argmin(rolling_RMSE) by regime
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
| V1 | Line | Forecast vs Actual | mart.forecasting_cockpit | Core comparison | Toggle model + bands |
| V2 | Bar | MAE/RMSE by model (horizon) | mart.forecasting_metrics | Model comparison | Hover |
| V3 | Table | Forecast Run Register | mart.model_runs | Operational trace | Sort |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Last 30 sessions | Applies to all visuals unless noted |
| Interval | dropdown | 5m | Intraday vs daily controls |
| Horizon | dropdown | 1–10 steps | Forecast pages only |
| View mode | toggle | Near real-time | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P10 Backtesting Report
  - V2-P11 Model Monitoring
- **Cross-page filter behaviour:** Cross-page filters: enabled (model + horizon)

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
**Refresh cadence:** every 30–60 minutes (session) + daily  
**Expected runtime:** < 120s  
**Freshness SLA:** 60 minutes  
**Latency notes:** Forecasts are short-horizon and for educational decision support only

---

## 12) Interpretation guide (how to read the page)
- Use KPI tiles for headline context; then confirm with the primary chart before deep-diving.
- When a metric breaches a threshold, check DQ and freshness first to avoid false alarms.
- Use drillthrough pages to validate the driver (intraday, risk, correlation, or model error).

> Keep interpretation factual; avoid “buy/sell” advice.

---

## 13) Compliance & disclaimers
- **Not financial advice.**  
- Data sources and limitations: `DATA_README.md`  
- Privacy: no personal data processed.

---

## 14) Screenshot/export references

**High-res export file(s):**
- `docs/dashboards/V2/exports/v2_page_09_forecasting_cockpit.png`

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
**Forecasting cockpit:** presents multiple model forecasts, horizons, and confidence at a glance.
This is the flagship ML/analytics page for the UK Masters project story.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P09. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| origin_timestamp_london | datetime | 2026-02-16 10:05 | Forecast issue time |
| target_timestamp_london | datetime | 2026-02-16 10:10 | Forecast target |
| horizon_step | int | 5 | 1..H |
| model_name | string | LSTM | ARIMA/LSTM/Prophet/etc |
| model_version | string | lstm_v2.3.0 | Semantic version |
| y_true | float | 8630.2 | Actual close (when available) |
| yhat | float | 8629.8 | Predicted close |
| mae_roll | float | 0.9 | Rolling MAE |
| rmse_roll | float | 1.2 | Rolling RMSE |
| run_id | string | 2026-02-16T10:05Z_02 | Run identifier |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Forecast tooltip: origin time, target time, horizon, model+version, yhat, y_true (if known), error, run_id.

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
- When y_true not yet available (future target) → tooltip must show “pending actual”.
- Model version mismatch vs page label → block export (must be consistent).

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- Model/horizon completeness: each model has rows for 1..H.
- Timestamps align to intraday bars (no off-by-one).

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Add a “model card” drawer link from this page to explain training window, features, and limitations.
- Keep ARIMA as baseline; add modern model as headline but never hide baseline.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
