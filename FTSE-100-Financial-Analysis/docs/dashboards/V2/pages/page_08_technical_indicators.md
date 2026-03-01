---
page_id: V2-P08
page_name: Technical Indicators
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

# Technical Indicators

## 1) Purpose
**One sentence purpose:**  
> Provide a clean technical-indicators panel (RSI, MACD, Bollinger Bands, MA cross) with disciplined explanations.

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. Are common indicator thresholds being approached or crossed?
2. Do indicators confirm or contradict price trend?
3. Is the market stretched (overbought/oversold proxies)?

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
| mart.technical_indicators | daily | Curated mart | daily close + hourly (session) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.technical_indicators | daily | Curated mart | daily close + hourly (session) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.technical_indicators | daily | Curated mart | daily close + hourly (session) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| RSI (14) | Relative Strength Index (14) | RSI(close, 14) | Warn if >70 or <30 | Thresholds are conventional |
| MACD | MACD line vs signal | EMA12-EMA26 | Info | Use crossovers as descriptive signals |
| BB Width | Bollinger band width | (upper-lower)/MA20 | Warn if widening fast | Proxy for volatility expansion |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_rsi14`  
  - **Definition:** RSI (14)  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    RSI = 100 - (100/(1+RS)), RS=avg_gain/avg_loss
    ```

- **Measure 02:** `m_macd`  
  - **Definition:** MACD(12,26,9)  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    macd=ema12-ema26; signal=ema9(macd)
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
| V1 | Line | Price + Bollinger Bands | mart.technical_indicators | Stretch + volatility | Hover + toggle bands |
| V2 | Line | RSI Panel | mart.technical_indicators | Momentum proxy | Hover |
| V3 | Line | MACD Panel | mart.technical_indicators | Momentum + crossovers | Hover |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Last 180 sessions | Applies to all visuals unless noted |
| Interval | dropdown | 1d | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Replay | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P02 Intraday Terminal
  - V2-P03 Volatility Regimes
- **Cross-page filter behaviour:** Cross-page filters: enabled (date range)

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
**Refresh cadence:** daily close + hourly (session)  
**Expected runtime:** < 60s  
**Freshness SLA:** 1 hour  
**Latency notes:** Indicators depend on consistent history; gaps degrade reliability

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
- `docs/dashboards/V2/exports/v2_page_08_technical_indicators.png`

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
**Technical indicators page:** makes the repo look like a serious market analytics toolkit while staying explainable.
Indicators must be documented in plain English (avoid “mystery math”).

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P08. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| timestamp_london | datetime | 2026-02-16 10:05 | London time |
| close | float | 8625.4 | points |
| rsi_14 | float | 57.2 | 0–100 |
| macd | float | 1.15 | MACD line |
| macd_signal | float | 0.98 | Signal line |
| bb_upper | float | 8650.0 | Bollinger upper |
| bb_lower | float | 8600.0 | Bollinger lower |
| run_id | string | 2026-02-16T10:05Z_02 | Run identifier |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Indicator tooltip: time, close, RSI, MACD, signal, BB upper/lower; include window sizes (14, 12-26-9, 20).

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
- Warm-up periods create null indicator values → annotate rather than backfilling silently.
- Indicator windows must match documentation; changing them is a breaking change.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- RSI must be within [0,100].
- BB upper >= BB lower always.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Centralise indicator computation in `curated.indicators` so all pages use the same logic.
- Use subtle bands; avoid neon overload.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
