---
page_id: V2-P04
page_name: Drawdown & Risk
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

# Drawdown & Risk

## 1) Purpose
**One sentence purpose:**  
> Quantify drawdowns, recovery time, and basic risk metrics (VaR/CVaR optional) with clear UK-market framing.

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. What is the current drawdown vs recent peak?
2. How deep are historical drawdowns and how long do recoveries take?
3. Are risk metrics deteriorating alongside volatility regimes?

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
| mart.drawdown_risk | daily | Curated mart | daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.drawdown_risk | daily | Curated mart | daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.drawdown_risk | daily | Curated mart | daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| Current Drawdown (%) | Distance from recent peak | (close/peak - 1)*100 | Warn if < -X% | Threshold depends on window |
| Max Drawdown (%) | Worst drawdown in window | min(drawdown) | Info | Used for narrative |
| VaR (95%) | Value-at-Risk (optional) | quantile(returns, 5%) | Warn if breaches | Use daily returns for risk |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_drawdown`  
  - **Definition:** Peak-to-trough drawdown  
  - **Implementation:** SQL/Python  
  - **Formula:**  
    ```text
    dd_t = close_t / max(close_{<=t}) - 1
    ```

- **Measure 02:** `m_cvar_95`  
  - **Definition:** Conditional VaR 95%  
  - **Implementation:** SQL/Python  
  - **Formula:**  
    ```text
    cvar = mean(returns[returns<=VaR_95])
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
| V1 | Line | Drawdown Curve | mart.drawdown_risk | Risk visibility | Hover + zoom |
| V2 | Bar | Top Drawdowns (Table/Bar) | mart.drawdown_risk | Historical context | Sort |
| V3 | Gauge | Risk Summary (VaR/CVaR) | mart.drawdown_risk | Headline risk | N/A |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Last 1 year | Applies to all visuals unless noted |
| Interval | dropdown | 1d | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Replay | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P03 Volatility Regimes
  - V2-P16 Board Pack One‑Pager
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
**Refresh cadence:** daily close  
**Expected runtime:** < 60s  
**Freshness SLA:** 24 hours  
**Latency notes:** Risk metrics are descriptive; no trading advice implied

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
- `docs/dashboards/V2/exports/v2_page_04_drawdown_risk.png`

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
**Risk lens:** drawdown contextualises “how bad can it get” from recent peaks; VaR/ES provide probabilistic risk proxies.
Use plain-language callouts: “Current drawdown = X% from last 3‑month high.”

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P04. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| date | date | 2026-02-16 | daily |
| close | float | 8625.4 | points |
| rolling_peak | float | 8800.0 | points |
| drawdown_pct | float | -1.98 | % |
| var_95 | float | -1.25 | % daily |
| es_95 | float | -1.80 | % daily |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Drawdown tooltip: date, close, peak, drawdown%, VaR95/ES95.

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
- Insufficient history for rolling peak window → show null with annotation.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- drawdown_pct == close/rolling_peak - 1.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Prefer transparent risk formulas and document windows (e.g., 252 trading days).

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
