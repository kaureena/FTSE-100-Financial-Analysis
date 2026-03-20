---
page_id: V2-P02
page_name: Intraday Terminal
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
primary_grain: intraday_1m
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# Intraday Terminal

## 1) Purpose
**One sentence purpose:**  
> Provide a trading-terminal style intraday view (candles, volume, VWAP proxy, microstructure notes).

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. How does intraday price action look at fine granularity?
2. Do volume spikes align with price jumps?
3. Are there intraday patterns that explain risk/forecast behaviour?

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
| mart.intraday_terminal | intraday_1m_or_5m | Curated mart | every 1–5 minutes (session) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.intraday_terminal | intraday_1m_or_5m | Curated mart | every 1–5 minutes (session) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.intraday_terminal | intraday_1m_or_5m | Curated mart | every 1–5 minutes (session) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| VWAP (proxy) | Volume-weighted average price proxy | sum(tp*vol)/sum(vol) | Info | Proxy for index-level data |
| Volume Spike Count | Number of bars flagged as spikes | count(vol > p95) | Warn if spikes cluster | May indicate news or data artefacts |
| Gap Minutes | Total missing minutes in session | sum(gap_minutes>1) | 0 preferred | DQ continuity gate |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_vwap_proxy`  
  - **Definition:** VWAP proxy using typical price  
  - **Implementation:** SQL/Python  
  - **Formula:**  
    ```text
    vwap = sum(((h+l+c)/3)*vol)/sum(vol)
    ```

- **Measure 02:** `m_volume_spike_flag`  
  - **Definition:** Flag volume spike bars  
  - **Implementation:** SQL/Python  
  - **Formula:**  
    ```text
    flag = volume >= percentile(volume, 95)
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
| V1 | Candlestick | FTSE 100 — Intraday Candles | mart.intraday_terminal | Microstructure view | Zoom + pan + hover |
| V2 | Bar | Volume (Intraday) | mart.intraday_terminal | Contextualise moves | Cross-filter (optional) |
| V3 | Line | VWAP (Proxy) Overlay | mart.intraday_terminal | Reference level | Toggle overlay |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Today (session) | Applies to all visuals unless noted |
| Interval | dropdown | 1m | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Near real-time | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P03 Volatility Regimes
  - V2-P12 Data Quality & Coverage
- **Cross-page filter behaviour:** Cross-page filters: enabled (interval + selected window)

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
**Refresh cadence:** every 1–5 minutes (session)  
**Expected runtime:** < 90s  
**Freshness SLA:** 5 minutes  
**Latency notes:** If intraday provider limits apply, fall back to replay mode for older days

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
- `docs/dashboards/V2/exports/v2_page_02_intraday_terminal.png`

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
**Terminal feel:** this page is the “trader screen” — candles, volume proxy, and micro-metrics.
**What to notice:**
- Breakouts supported by volume spikes.
- Momentum vs mean reversion behaviour intraday.
- Gap minutes (missing bars) indicator for trust.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P02. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| timestamp_london | datetime | 2026-02-16 10:05 | London time |
| open | float | 8624.8 | points |
| high | float | 8626.0 | points |
| low | float | 8624.1 | points |
| close | float | 8625.4 | points |
| volume | float/int | 14500 | >=0 |
| gap_flag | bool | False | True if missing minutes around this bar |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Candles tooltip: O/H/L/C, body, wick sizes, 1m return, volume percentile.
- Gap tooltip: show missing interval length and location.

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
- Provider resamples data → may hide gaps; enforce explicit continuity checks.
- Volume missing → downgrade trust and hide volume-based interpretations.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- OHLC sanity hard gate.
- Continuity check within session.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Plotly candlestick is recommended for reliability; Power BI requires stable candlestick visual selection.
- Keep terminal-like dense layout but avoid unreadable labels.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
