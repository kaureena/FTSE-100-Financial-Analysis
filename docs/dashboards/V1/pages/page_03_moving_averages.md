---
page_id: V1-P03
page_name: Moving Averages & Trend
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

# Moving Averages & Trend

## 1) Purpose
**One sentence purpose:**  
> Explain trend structure using a 20-period moving average overlay and crossover markers.

**Why this page exists (business value):**
- Smooths noise to highlight underlying direction.
- Provides consistent narrative between visuals and models (trend vs noise).
- Supplies features used downstream (MA, slopes) for model comparison.

---

## 2) Primary questions this page answers
1. Is the market trending or ranging during the session?
2. Do MA crossovers coincide with visible turning points?
3. How much lag does MA introduce relative to rapid moves?

---

## 3) Intended audience & usage pattern
**Audience:** Portfolio reviewer / analyst  
**Typical usage:** Intraday analysis (replay snapshot)  
**Decision context:** Feature + signal explanation

---

## 4) Data sources & contracts

### 4.1 Inputs (tables/files)
| Input | Grain | Source | Refresh | Contract |
|------|------|--------|---------|----------|
| v1_dissertation_baseline/data/processed/ftse100_intraday_1m_clean.parquet | intraday_1m | Yahoo Finance snapshot | snapshot (frozen) | [DATA_CONTRACTS.md#v1-intraday-1m](../../../../DATA_CONTRACTS.md#v1-intraday-1m) |
| v1_dissertation_baseline/outputs/tables/moving_average_features.parquet | intraday_1m | Derived features | on export | [DATA_CONTRACTS.md#v1-features](../../../../DATA_CONTRACTS.md#v1-features) |
| v1_dissertation_baseline/outputs/figures/ma_overlay.png | figure | Plot export | on export | N/A |

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
| MA(20) slope | Direction of MA(20) over recent bars | slope(MA20) | Informational | Use linear fit over last N bars |
| Crossover count | Number of close vs MA crossovers | count(crossovers) | Informational | Higher values may indicate choppiness |
| Trendiness score | Signal-to-noise proxy | abs(mean(r))/std(r) | Informational | Used for narrative only |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_ma20`  
  - **Definition:** 20-bar moving average of close  
  - **Implementation:** Python/SQL  
  - **Formula:**  
    ```text
    MA20_t = mean(close_{t-19..t})
    ```

- **Measure 02:** `m_ma_gap`  
  - **Definition:** Distance between close and MA20  
  - **Implementation:** Python/SQL  
  - **Formula:**  
    ```text
    gap_t = close_t - MA20_t
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
| V1 | Line | Close vs MA(20) | moving_average_features.parquet | Trend smoothing and lag | Hover + toggle MA |
| V2 | Marker | Crossover markers | moving_average_features.parquet | Highlight crosses | Tooltip with timestamp |
| V3 | Histogram | MA Gap distribution | moving_average_features.parquet | Context on deviations | Brush to filter |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | This session day | Applies to all visuals unless noted |
| Interval | dropdown | 1m | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Replay | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V1-P04 ARIMA Forecast
  - V1-P05 LSTM Forecast
- **Cross-page filter behaviour:** Cross-page filters: enabled (date/session only)

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
**Refresh cadence:** snapshot (frozen dataset)  
**Expected runtime:** < 30s  
**Freshness SLA:** N/A (snapshot)  
**Latency notes:** MA features depend on continuity; gaps reduce interpretability

---

## 12) Interpretation guide (how to read the page)
- Use MA(20) to describe the underlying direction without overreacting to minute noise.
- Crossover clusters often indicate sideways conditions; note this when interpreting ARIMA stationarity assumptions.
- Large MA gaps can correspond to volatility spikes; expect higher forecast error around these segments.

> Keep interpretation factual; avoid “buy/sell” advice.

---

## 13) Compliance & disclaimers
- **Not financial advice.**  
- Data sources and limitations: `DATA_README.md`  
- Privacy: no personal data processed.

---

## 14) Screenshot/export references

**High-res export file(s):**
- `docs/dashboards/V1/exports/v1_page_03_moving_averages.png`

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
**Why MA matters:** Moving averages reduce 1m noise and provide a consistent trend lens for non-technical reviewers.
**What to look for:**
- Distance of price from MA(20) (overextension risk).
- Crossovers and whether they happen on meaningful moves (avoid over-trading).
- MA slope direction consistency (trend stability).

### Dissertation traceability (V1)
- Maps to dissertation visuals: **20-period moving average** used to smooth short-term fluctuations and highlight trends.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V1-P03. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| timestamp | datetime | 2024-09-05 10:15:00+00:00 | Unique per minute |
| close | float | 8620.4 | points |
| ma20 | float | 8618.9 | Computed from close rolling(20) |
| ma_gap | float | 1.5 | close - ma20 |
| crossover_flag | bool | False | True when sign(ma_gap) changes |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- **MA chart tooltip:** London time, close, MA20, gap, slope (optional), crossover flag.
- **Crossover markers tooltip:** “Bullish cross above MA20” / “Bearish cross below MA20”.

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
- First 19 bars have no MA20 → show as null and annotate “warm-up period”.
- Frequent crossovers in sideways market → interpretation guide must warn about whipsaw risk.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- MA20 must equal rolling mean of close (spot-check a random timestamp).
- If slope computed, confirm window length and units (points/minute).

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- **Power BI:** Use a calculated column or measure for MA20; if using measure, ensure it respects filter context correctly.
- **Python:** `pandas.Series.rolling(20).mean()` with explicit `min_periods=20`.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
