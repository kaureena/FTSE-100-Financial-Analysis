---
page_id: V2-P07
page_name: Top Movers Watchlist
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
primary_grain: intraday_5m (constituents)
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# Top Movers Watchlist

## 1) Purpose
**One sentence purpose:**  
> Provide a watchlist of top gainers/losers and volume movers (constituent-level if available).

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. Which constituents moved the most today / over the selected window?
2. Are moves supported by unusual volume?
3. Which names merit deeper drilldown (risk/forecast)?

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
| mart.top_movers | daily | Curated mart | daily close + intraday refresh (optional) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.top_movers | daily | Curated mart | daily close + intraday refresh (optional) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.top_movers | daily | Curated mart | daily close + intraday refresh (optional) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| Top Gainer | Largest % return | max(return) | Info | Based on selected window |
| Top Loser | Smallest % return | min(return) | Info | Based on selected window |
| Volume Spike Names | Count of tickers with volume spike | count(flag) | Warn if many | May coincide with events/news |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_return_window`  
  - **Definition:** Return over selected window  
  - **Implementation:** SQL/Python  
  - **Formula:**  
    ```text
    (last/first - 1)
    ```

- **Measure 02:** `m_volume_spike`  
  - **Definition:** Volume spike flag per ticker  
  - **Implementation:** SQL/Python  
  - **Formula:**  
    ```text
    volume >= p95(volume)
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
| V1 | Table | Top Movers (Ranked) | mart.top_movers | Watchlist | Sort + search |
| V2 | Bar | Top Movers Bar | mart.top_movers | Rank visual | Hover |
| V3 | Scatter | Return vs Volume (Outlier map) | mart.top_movers | Spot unusual combos | Hover |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Today (or last session) | Applies to all visuals unless noted |
| Interval | dropdown | 1d | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Near real-time | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P02 Intraday Terminal
  - V2-P15 Events Overlay
- **Cross-page filter behaviour:** Cross-page filters: enabled (selected ticker)

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
**Refresh cadence:** daily close + intraday refresh (optional)  
**Expected runtime:** < 60s  
**Freshness SLA:** 24 hours (or 10 min in session)  
**Latency notes:** Watchlist is descriptive; no recommendations

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
- `docs/dashboards/V2/exports/v2_page_07_top_movers_watchlist.png`

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
**Watchlist purpose:** show top gainers/losers with enough context to be credible (sector, size, volume, news flag).
This is the most “real-time product” feeling table in the repo.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P07. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| as_of_london | datetime | 2026-02-16 10:05 | London time snapshot |
| ticker | string | AZN.L | Constituent ticker |
| company_name | string | AstraZeneca | Display name |
| sector | string | Healthcare | Sector |
| return_pct | float | 1.12 | % over selected window |
| volume | float/int | 1200345 | Shares traded (if available) |
| market_cap_gbp | float | 175000000000 | GBP (optional) |
| news_flag | bool | True | True if news/event linked |
| rank | int | 1 | Rank by abs return |
| run_id | string | 2026-02-16T10:05Z_02 | Run identifier |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Row tooltip: ticker, name, sector, return%, volume, market cap, last update time, data source.

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
- Constituent list changes (quarterly index review) → version constituents and log in release notes.
- Some providers do not give intraday volume for all names → show missingness explicitly.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- Ranks must match sort order (e.g., abs(return) desc).
- Ticker must exist in constituents dimension for that date.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Add a search box (ticker/company) for a premium feel.
- Provide export-friendly formatting: fixed decimals, right-aligned numbers, sticky header.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
