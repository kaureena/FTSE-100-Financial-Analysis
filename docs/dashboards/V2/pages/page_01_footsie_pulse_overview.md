---
page_id: V2-P01
page_name: Footsie Pulse — Overview
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
primary_grain: mixed (intraday + daily)
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# Footsie Pulse — Overview

## 1) Purpose
**One sentence purpose:**  
> Show the current FTSE 100 state (level, change, range, realised volatility proxy) with London-session framing.

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. What’s the current market state vs previous close?
2. Is the session calm or stressed (range/vol proxy)?
3. What are the headline drivers worth investigating next (movers/sector/risk)?

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
| mart.market_overview | intraday_5m | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.market_overview | intraday_5m | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.data_quality_health | run | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| Last (points) | Latest index level | last(close) | Info | Index points |
| Δ vs Prev Close (%) | Percent change vs previous close | (close/prev_close-1)*100 | Info | Shows direction and magnitude |
| Realised Vol (20) | Rolling realised volatility proxy | std(r_20)*sqrt(20) | Warn if > threshold | Threshold set in thresholds.yaml |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_prev_close`  
  - **Definition:** Previous close value  
  - **Implementation:** SQL/Python  
  - **Formula:**  
    ```text
    prev_close = last(close) from previous trading day
    ```

- **Measure 02:** `m_range_pct`  
  - **Definition:** Session range as % of prev close  
  - **Implementation:** SQL/Python  
  - **Formula:**  
    ```text
    range_pct = (high-low)/prev_close * 100
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
| V1 | Line | FTSE 100 — Session Trend | mart.market_overview | Headline trend | Hover + zoom |
| V2 | KPI Panel | Headline KPIs | mart.market_overview | Top KPIs | N/A |
| V3 | Table | Quick Diagnostics (freshness + DQ) | mart.data_quality_health | Trust signals | N/A |

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
  - V2-P02 Intraday Terminal
  - V2-P16 Board Pack One‑Pager
- **Cross-page filter behaviour:** Cross-page filters: enabled (date + interval + selection)

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
**Refresh cadence:** every 5 minutes (session) + daily close  
**Expected runtime:** < 60s end-to-end  
**Freshness SLA:** 5–10 minutes  
**Latency notes:** Supports near real-time feel; outside session uses last available snapshot

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
- `docs/dashboards/V2/exports/v2_page_01_footsie_pulse_overview.png`

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
**Executive storyline:** a one-screen snapshot of the Footsie with trust signals (freshness + DQ + run_id).
**What to notice:**
- Market direction (Δ% vs prev close) + breadth (if constituents available).
- Volatility regime label (calm/normal/stressed).
- Any anomaly banner (freshness, DQ, pipeline).
**Next step:** use P02 for intraday detail or P03/P04 for regime and risk context.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P01. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| timestamp_london | datetime | 2026-02-16 10:05 | Display timezone Europe/London |
| interval | string | 1m | 1m/5m/1d |
| close | float | 8625.4 | points |
| prev_close | float | 8602.1 | points |
| delta_pct | float | 0.27 | % change |
| realised_vol_20 | float | 0.85 | % vol proxy |
| run_id | string | 2026-02-16T10:05Z_02 | Run identifier |
| freshness_minutes | int | 3 | minutes since refresh |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Primary trend tooltip: London time, close, Δ points, Δ%, regime, vol proxy, freshness.
- KPI tooltip: ensure baseline definition is explicit (prev close vs open).

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
- Near real-time mode with provider lag → show AMBER banner when freshness > threshold.
- Daily interval selected during session → warn that daily close is incomplete.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- Δ% must reconcile: (close/prev_close-1)*100.
- Freshness must match run register timestamps.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Implement the header trust banner as a reusable component across all V2 pages.
- Use consistent KPI tile layout and number formats (points, %, + sign for positive).

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
