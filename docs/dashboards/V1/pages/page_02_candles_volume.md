---
page_id: V1-P02
page_name: Candlestick + Volume
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

# Candlestick + Volume

## 1) Purpose
**One sentence purpose:**  
> Provide minute-level candlestick and volume context for intraday price action.

**Why this page exists (business value):**
- Shows open/high/low/close structure per minute for detailed intraday analysis.
- Pairs volume with price action to contextualise moves.
- Supports identification of short-term patterns and volatility clustering (educational).

---

## 2) Primary questions this page answers
1. What does price action look like at the 1-minute granularity?
2. Are large moves supported by elevated volume?
3. Do we see obvious patterns (consolidation, spikes) that explain forecast errors later?

---

## 3) Intended audience & usage pattern
**Audience:** Portfolio reviewer / analyst  
**Typical usage:** Intraday monitoring (replay snapshot)  
**Decision context:** Technical visualisation (dissertation replication)

---

## 4) Data sources & contracts

### 4.1 Inputs (tables/files)
| Input | Grain | Source | Refresh | Contract |
|------|------|--------|---------|----------|
| v1_dissertation_baseline/data/processed/ftse100_intraday_1m_clean.parquet | intraday_1m | Yahoo Finance snapshot | snapshot (frozen) | [DATA_CONTRACTS.md#v1-intraday-1m](../../../../DATA_CONTRACTS.md#v1-intraday-1m) |
| v1_dissertation_baseline/outputs/metrics/volume_spike_flags.csv | intraday_1m | Derived flags | on export | [DATA_CONTRACTS.md#v1-volume-flags](../../../../DATA_CONTRACTS.md#v1-volume-flags) |
| v1_dissertation_baseline/outputs/figures/candles_volume.png | figure | Plot export | on export | N/A |

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
| Avg Volume (bars) | Average volume per bar | mean(volume) | Informational | Volume interpretation is proxy-like for index data |
| Max Volume Spike | Largest bar volume | max(volume) | Warn if outlier | Verify spikes are not missing-data artefacts |
| Vol/Price Co-move | Correlation of abs return vs volume | corr(|r|, volume) | Informational | Used for narrative only |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_vwap_proxy`  
  - **Definition:** VWAP proxy using typical price * volume  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    vwap = sum(tp*vol)/sum(vol), tp=(high+low+close)/3
    ```

- **Measure 02:** `m_abs_return`  
  - **Definition:** Absolute return magnitude  
  - **Implementation:** Python/SQL  
  - **Formula:**  
    ```text
    |r_t| = abs((close_t/close_{t-1})-1)
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
| V1 | Candlestick | FTSE 100 — 1m Candles | ftse100_intraday_1m_clean.parquet | Minute-by-minute structure | Zoom + pan + hover |
| V2 | Bar | Volume (1m) | ftse100_intraday_1m_clean.parquet | Contextualise price moves | Cross-filter (optional) |
| V3 | Scatter | |Return| vs Volume | ftse100_intraday_1m_clean.parquet | Check co-movement | Hover points |

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
  - V1-P03 Moving Averages & Trend
  - V1-P07 Data Quality Snapshot
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
**Expected runtime:** < 45s for candle+volume export  
**Freshness SLA:** N/A (snapshot)  
**Latency notes:** Volume spikes are flagged; confirm DQ for missing bars

---

## 12) Interpretation guide (how to read the page)
- Use candle bodies/wicks to describe intraday sentiment shifts (educational context).
- Treat volume spikes as ‘attention’ markers, but confirm they are not caused by timestamp gaps.
- If candles show abrupt jumps, cross-check DQ and note potential impact on ARIMA residuals and LSTM fit.

> Keep interpretation factual; avoid “buy/sell” advice.

---

## 13) Compliance & disclaimers
- **Not financial advice.**  
- Data sources and limitations: `DATA_README.md`  
- Privacy: no personal data processed.

---

## 14) Screenshot/export references

**High-res export file(s):**
- `docs/dashboards/V1/exports/v1_page_02_candles_volume.png`

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
**Trading desk use:** Candles explain *how* the line chart moved—body vs wick shows conviction vs rejection.
**What to look for:**
- Sequences of higher highs / higher lows (trend strength).
- Wick-heavy bars around key levels (potential mean reversion / resistance).
- Volume confirming breakouts (volume spike aligned with candle expansion).
**Next step:** Use **V1-P03** to smooth noise and confirm trend direction with MA(20).

### Dissertation traceability (V1)
- Maps to dissertation visuals: **candlestick chart** + **volume chart** for granular market activity interpretation.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V1-P02. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| timestamp | datetime | 2024-09-05 09:30:00+00:00 | Unique per minute |
| open | float | 8610.1 | points |
| high | float | 8612.7 | points |
| low | float | 8609.6 | points |
| close | float | 8612.3 | points |
| volume | float/int | 18400 | >=0 |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- **Candlestick tooltip:** London time, O/H/L/C (points), candle body size, wick sizes, 1m return %, optional pattern label (doji/engulfing).
- **Volume tooltip:** London time, volume, volume z-score or percentile rank, spike_flag.

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
- Extreme wicks due to bad ticks → flag as outlier, do not drop silently.
- Volume missing/null → treat as unknown; hide volume-dependent KPIs with an AMBER note.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- OHLC sanity (hard fail).
- If pattern labelling enabled, ensure it uses clean OHLC and document rules (avoid ‘black box’).

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- **Plotly:** `go.Candlestick` + volume bars below; align x-axes and keep gaps visible.
- **Power BI:** Candlestick may require custom visual—if used, document and ensure export reliability.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
