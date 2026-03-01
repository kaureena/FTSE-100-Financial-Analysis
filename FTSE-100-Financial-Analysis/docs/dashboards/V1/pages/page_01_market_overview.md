---
page_id: V1-P01
page_name: Market Overview (Intraday)
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

# Market Overview (Intraday)

## 1) Purpose
**One sentence purpose:**  
> Provide an at-a-glance view of the FTSE 100 intraday session using line-based trend and headline KPIs.

**Why this page exists (business value):**
- Summarises session direction, range and volatility in a single view.
- Establishes the baseline context before drilling into candles/volume.
- Supports rapid validation that the dataset and timeline are sensible before modelling.

---

## 2) Primary questions this page answers
1. What is the overall direction of the index during the session?
2. How volatile was the session (range, realised volatility proxy)?
3. Were there visible regime shifts (trend breaks or volatility spikes)?

---

## 3) Intended audience & usage pattern
**Audience:** Portfolio reviewer / analyst  
**Typical usage:** Intraday monitoring (replay snapshot)  
**Decision context:** Market analytics (educational / dissertation replication)

---

## 4) Data sources & contracts

### 4.1 Inputs (tables/files)
| Input | Grain | Source | Refresh | Contract |
|------|------|--------|---------|----------|
| v1_dissertation_baseline/data/processed/ftse100_intraday_1m_clean.parquet | intraday_1m | Yahoo Finance snapshot | snapshot (frozen) | [DATA_CONTRACTS.md#v1-intraday-1m](../../../../DATA_CONTRACTS.md#v1-intraday-1m) |
| v1_dissertation_baseline/outputs/metrics/session_kpis.csv | session | Derived KPIs | on export | `KPI_CATALOGUE.md#v1-session-kpis` |
| v1_dissertation_baseline/outputs/figures/line_trend.png | figure | Plot export | on export | N/A |

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
| Last Close (points) | Closing index level at final bar of session | close[last_bar] | Informational | Displayed in index points |
| Intraday Δ (%) | Percent change vs first bar (open proxy) | (close_last/close_first - 1)*100 | Informational | Use close_first as intraday baseline |
| Session Range (points) | High - Low for the day/session | max(high)-min(low) | Warn if unusually wide | Range is sensitive to outliers; validate DQ |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_return_simple`  
  - **Definition:** Simple return between consecutive closes  
  - **Implementation:** Python/SQL  
  - **Formula:**  
    ```text
    r_t = (close_t / close_{t-1}) - 1
    ```

- **Measure 02:** `m_realised_vol_20`  
  - **Definition:** Rolling realised volatility proxy (20 bars)  
  - **Implementation:** Python/SQL  
  - **Formula:**  
    ```text
    vol_20 = std(r_{t-19..t}) * sqrt(20)
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
| V1 | Line | FTSE 100 Intraday Trend | ftse100_intraday_1m_clean.parquet | Trend + volatility visibility | Hover tooltip; zoom/pan |
| V2 | Area | Session Range Band (High/Low) | ftse100_intraday_1m_clean.parquet | Show high-low envelope | Toggle band on/off |
| V3 | Table | Session KPI Summary | session_kpis.csv | Quick numeric summary | Sort by KPI |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | This session day | Applies to all visuals unless noted |
| Interval | dropdown | 1m | Intraday vs daily controls |
| Horizon | dropdown | 10-min (forecast pages) | Forecast pages only |
| View mode | toggle | Replay | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V1-P02 Candlestick + Volume
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
**Expected runtime:** < 30s for export build  
**Freshness SLA:** N/A (snapshot)  
**Latency notes:** No live refresh; this is a reproducible replay pack

---

## 12) Interpretation guide (how to read the page)
- Use the line chart to identify the dominant intraday direction and any sharp discontinuities.
- If the session range is unusually wide, verify OHLC sanity and outlier flags in the DQ page before interpreting moves.
- Use this page as the ‘starting context’ before looking at candlestick patterns and model forecasts.

> Keep interpretation factual; avoid “buy/sell” advice.

---

## 13) Compliance & disclaimers
- **Not financial advice.**  
- Data sources and limitations: `DATA_README.md`  
- Privacy: no personal data processed.

---

## 14) Screenshot/export references

**High-res export file(s):**
- `docs/dashboards/V1/exports/v1_page_01_market_overview.png`

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
**London session storyline:** Start by validating the **session open**, then watch how price evolves into mid-session and into the close.
**What to notice (quick scan):**
- Gap vs prev close (if available) and whether the first 30–60 minutes are trend-following or mean-reverting.
- Whether the session range expands steadily (trending) or oscillates (choppy/sideways).
- Any volatility burst (spikes in 1m returns) that might impact short-horizon forecasting stability.
**Next step:** If the trend looks clean, move to **V1-P02** (candles/volume). If the trend looks noisy, check **V1-P07** (DQ) before modelling.

### Dissertation traceability (V1)
- Maps to dissertation visuals: **line chart** for overall trend and volatility framing.
- Supports the dissertation goal of **real-time display** for rapid decision context before deeper analysis.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V1-P01. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| timestamp | datetime | 2024-09-05 08:01:00+00:00 | Unique per minute; display in Europe/London |
| open | float | 8602.5 | Index points; >= 0 |
| high | float | 8604.2 | >= max(open, close) |
| low | float | 8601.9 | <= min(open, close) |
| close | float | 8603.7 | Index points; >= 0 |
| volume | float/int | 12345 | Non-negative; proxy for activity |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- **Primary line chart tooltip:** London time, close (points), Δ points vs session open, Δ% vs session open, session high/low so far, rolling vol proxy (if enabled).
- **KPI tiles tooltip:** define exactly which timestamps are used (first bar vs official open; last available bar).

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
- Provider returns timestamps in UTC without timezone → must be localised and then converted for display.
- Missing bars near open/close due to ingestion lag → show AMBER freshness banner, do not interpret intraday range until filled.
- Market closed (weekend/holiday) → show “No session data” state and disable KPIs that assume intraday bars.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- Check `count_duplicates(timestamp)==0` and log if not.
- Check OHLC sanity for every bar: `high>=max(open,close)` and `low<=min(open,close)`.
- Reconcile: session range KPI equals `max(high)-min(low)` from the same filtered window.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- **Power BI:** Use measures for `SessionOpen = FIRSTNONBLANK(close,1)` (respect filters) and `IntradayΔ%` from close_last vs close_first.
- **Plotly:** Use a single time index; avoid auto-resampling which can hide missing minutes—explicitly show gaps.
- **Export:** Include footer with run_id + London timestamp + freshness.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
