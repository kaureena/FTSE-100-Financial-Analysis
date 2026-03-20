---
page_id: V2-P10
page_name: Backtesting Report
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
primary_grain: daily
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# Backtesting Report

## 1) Purpose
**One sentence purpose:**  
> Walk-forward backtesting summary: rolling MAE/RMSE by horizon and regime, model ranking stability.

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. How stable is model performance over time?
2. Which model performs best by regime?
3. Do errors drift upward as market conditions change?

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
| mart.backtesting_report | run | Curated mart | daily close (or weekly) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.backtesting_report | run | Curated mart | daily close (or weekly) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.backtesting_report | run | Curated mart | daily close (or weekly) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| Rolling RMSE | Rolling RMSE over evaluation windows | RMSE_roll | Lower is better | Used for stability |
| Best Model Share | % windows where each model is best | count(best)/N | Info | Shows dominance |
| Error Trend | Slope of rolling error | slope(RMSE_roll) | Warn if positive | Potential drift |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_walk_forward_split`  
  - **Definition:** Walk-forward split strategy  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    train=[t0..t], test=[t+1..t+h], rolling
    ```

- **Measure 02:** `m_rank_stability`  
  - **Definition:** Rank stability metric  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    stability = 1 - (rank_changes / windows)
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
| V1 | Line | Rolling Error Over Time | mart.backtesting_report | Drift visibility | Hover |
| V2 | Heatmap | Performance by Regime & Horizon | mart.backtesting_report | Where models win | Hover |
| V3 | Bar | Model Win Share | mart.backtesting_report | Ranking summary | Hover |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Last 1 year | Applies to all visuals unless noted |
| Interval | dropdown | 1d | Intraday vs daily controls |
| Horizon | dropdown | 1–10 steps | Forecast pages only |
| View mode | toggle | Replay | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P09 Forecasting Cockpit
  - V2-P11 Model Monitoring
- **Cross-page filter behaviour:** Cross-page filters: enabled (model + regime)

---

## 10) Data Quality (DQ) & trust signals

**DQ checks relevant to this page:**
- No duplicate dates per instrument
- No missing closes for trading days in calendar range (or flagged as market holiday)
- OHLC sanity + non-negative volume

**DQ outputs referenced (V2):**
- `v2_modernisation_realtime/dq_data_quality/reports/dq_report.html`
- `docs/logs/07_dq_issue_register.csv`

**If DQ fails:**
- Follow `v2_modernisation_realtime/monitoring/incident_playbook.md`

---

## 11) Refresh & performance expectations
**Refresh cadence:** daily close (or weekly)  
**Expected runtime:** < 180s  
**Freshness SLA:** 7 days  
**Latency notes:** Backtests are computational; store snapshots for reproducibility

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
- `docs/dashboards/V2/exports/v2_page_10_backtesting_report.png`

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
**Backtesting page:** converts forecasts/signals into performance evidence (what would have happened).
This makes the project feel production-grade rather than purely academic.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P10. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| strategy_id | string | mean_reversion_v1 | Strategy label |
| as_of_date | date | 2026-02-16 | Backtest end date |
| window_start | date | 2023-01-01 | Backtest start |
| window_end | date | 2026-02-16 | Backtest end |
| total_return_pct | float | 12.4 | % |
| annualised_return_pct | float | 4.1 | % |
| volatility_pct | float | 9.2 | % |
| sharpe | float | 0.45 | risk-adjusted |
| max_drawdown_pct | float | -8.3 | % |
| trade_count | int | 132 | Number of trades |
| run_id | string | 2026-02-16T10:05Z_02 | Run identifier |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Performance tooltip: strategy, time window, return, vol, sharpe, max DD, trade count.

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
- Transaction costs not included → must be stated; optionally include a sensitivity toggle.
- Look-ahead bias risk → explicitly document feature timing and signal generation.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- PnL curve reconciles to daily returns aggregation.
- Trade count matches trade log table if present.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Include a “methodology box” on page: signal rules + assumptions in plain English.
- Use the same risk metrics definitions as V2-P04.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
