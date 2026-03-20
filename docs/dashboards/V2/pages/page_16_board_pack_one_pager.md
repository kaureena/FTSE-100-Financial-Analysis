---
page_id: V2-P16
page_name: Board Pack One‑Pager
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
primary_grain: mixed (executive summary)
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# Board Pack One‑Pager

## 1) Purpose
**One sentence purpose:**  
> Executive one-pager summarising market state, risk, and forecast headline with clear caveats and trust signals.

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. What happened since last close (headline)?
2. What are the top risks and notable changes?
3. What is the short-horizon outlook (as a descriptive forecast)?

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
| mart.board_pack | run | Curated mart | daily close (primary) + intraday optional | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.board_pack | run | Curated mart | daily close (primary) + intraday optional | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.board_pack | run | Curated mart | daily close (primary) + intraday optional | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| Headline Δ | Change vs previous close | Δ% | Info | One-line headline |
| Risk Flag | Risk status (OK/WARN/ALERT) | threshold rules | Warn/Alert | Derived from vol+drawdown+DQ |
| Forecast Direction | Near-horizon direction (up/down/flat) | sign(yhat - last) | Info | No trading advice |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_risk_flag`  
  - **Definition:** Composite risk flag  
  - **Implementation:** SQL/Python  
  - **Formula:**  
    ```text
    flag based on vol + drawdown + DQ pass
    ```

- **Measure 02:** `m_exec_headline`  
  - **Definition:** Auto headline text (optional)  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    template fill with KPIs and date
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
| V1 | KPI Panel | Executive KPIs | mart.board_pack | One glance summary | N/A |
| V2 | Line | Trend + Regime mini-chart | mart.board_pack | Context | Hover |
| V3 | Table | Notes & Assumptions | mart.board_pack | Caveats | N/A |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Latest snapshot | Applies to all visuals unless noted |
| Interval | dropdown | N/A | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Replay | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P01 Footsie Pulse — Overview
  - V2-P04 Drawdown & Risk
- **Cross-page filter behaviour:** Cross-page filters: minimal (executive view)

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
**Refresh cadence:** daily close (primary) + intraday optional  
**Expected runtime:** < 60s  
**Freshness SLA:** 24 hours  
**Latency notes:** Designed to export to PDF/PNG for portfolio viewing

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
- `docs/dashboards/V2/exports/v2_page_16_board_pack_one_pager.png`

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
**Board pack one-pager:** a CEO-friendly summary — direction, risk, regime, forecast, and operational trust signals.
This page is meant to be exported as a single 4K image and pasted into a deck.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P16. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| as_of_london | datetime | 2026-02-16 10:05 | London time |
| headline_move_pct | float | 0.27 | % |
| regime_label | string | Normal | Regime |
| current_drawdown_pct | float | -1.98 | % |
| forecast_10m_delta_points | float | 3.2 | points |
| dq_score | float | 98.0 | 0–100 |
| freshness_minutes | int | 3 | minutes |
| run_id | string | 2026-02-16T10:05Z_02 | Run identifier |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Executive KPI tooltip: show definition + baseline + unit (keep it simple).

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
- If DQ FAIL → board pack must show RED banner and hide forecast deltas.
- If daily close not available yet → label as “intraday snapshot”.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- All values reconcile to their source pages/measures.
- Board pack values match those shown on detail pages under same filters.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Use large typography, minimal charts, and crisp callouts.
- This page should be the most polished export in the repo.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
