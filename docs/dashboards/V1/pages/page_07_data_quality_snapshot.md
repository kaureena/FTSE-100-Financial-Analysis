---
page_id: V1-P07
page_name: Data Quality Snapshot
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

# Data Quality Snapshot

## 1) Purpose
**One sentence purpose:**  
> Provide a trust layer for the V1 dataset and outputs (gaps, duplicates, OHLC sanity, outliers).

**Why this page exists (business value):**
- Ensures users do not over-interpret results from flawed intraday data.
- Documents dataset granularity and continuity assumptions.
- Creates professional credibility by including DQ in an academic repo.

---

## 2) Primary questions this page answers
1. Are there missing bars, duplicates, or timestamp anomalies?
2. Do OHLC values satisfy basic sanity constraints?
3. Are outliers likely to distort forecasts or volatility measures?

---

## 3) Intended audience & usage pattern
**Audience:** Data/BI reviewer  
**Typical usage:** Pre-flight validation  
**Decision context:** DQ and trust

---

## 4) Data sources & contracts

### 4.1 Inputs (tables/files)
| Input | Grain | Source | Refresh | Contract |
|------|------|--------|---------|----------|
| v1_dissertation_baseline/data/processed/ftse100_intraday_1m_clean.parquet | intraday_1m | Yahoo Finance snapshot | snapshot (frozen) | [DATA_CONTRACTS.md#v1-intraday-1m](../../../../DATA_CONTRACTS.md#v1-intraday-1m) |
| v1_dissertation_baseline/outputs/metrics/dq_snapshot.json | run | DQ output | on export | [DATA_CONTRACTS.md#v1-dq](../../../../DATA_CONTRACTS.md#v1-dq) |
| v1_dissertation_baseline/outputs/tables/gap_report.csv | run | Gap report | on export | [DATA_CONTRACTS.md#v1-dq](../../../../DATA_CONTRACTS.md#v1-dq) |

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
| Missing bars | Count of expected bars missing within session | expected_bars - actual_bars | 0 preferred | If >0, document gaps and impact |
| Duplicate timestamps | Count of duplicates | count(dupes) | 0 required | Duplicates can break models |
| OHLC sanity failures | Count of sanity rule violations | count(violations) | 0 required | High >= max(open,close), low <= min(open,close) |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_gap_minutes`  
  - **Definition:** Gap length between consecutive bars (minutes)  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    gap = diff(timestamp) in minutes
    ```

- **Measure 02:** `m_ohlc_sanity_flag`  
  - **Definition:** Boolean flag for OHLC constraints  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    flag = (high>=max(open,close)) & (low<=min(open,close)) & (volume>=0)
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
| V1 | Table | DQ Scorecard | dq_snapshot.json | Quick trust view | N/A |
| V2 | Bar | Gaps by length | gap_report.csv | Continuity diagnostics | Hover |
| V3 | Scatter | Outlier map (return vs time) | ftse100_intraday_1m_clean.parquet | Spot extreme moves | Hover |

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
  - V1-P01 Market Overview
  - V1-P04 ARIMA Forecast
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
**Refresh cadence:** snapshot (DQ computed on export)  
**Expected runtime:** < 20s  
**Freshness SLA:** N/A (snapshot)  
**Latency notes:** DQ should run before forecast generation

---

## 12) Interpretation guide (how to read the page)
- If missing bars > 0, note that moving averages and LSTM sequences may be disrupted.
- If OHLC sanity failures exist, treat downstream metrics and forecasts as invalid until corrected.
- Use this page as a ‘trust gate’ before presenting forecasts in V1 pages.

> Keep interpretation factual; avoid “buy/sell” advice.

---

## 13) Compliance & disclaimers
- **Not financial advice.**  
- Data sources and limitations: `DATA_README.md`  
- Privacy: no personal data processed.

---

## 14) Screenshot/export references

**High-res export file(s):**
- `docs/dashboards/V1/exports/v1_page_07_data_quality_snapshot.png`

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
**This is the trust gate:** if DQ fails, *do not interpret forecasts*.
**What to watch:**
- Missing minute bars (continuity) and where the gaps occur.
- Duplicate timestamps (hard fail).
- OHLC sanity violations (hard fail).
**Action:** log issues in `docs/logs/07_dq_issue_register.csv` and show banner behaviour on other pages.

### Dissertation traceability (V1)
- Supports the dissertation’s emphasis on reliable real-time interpretation by ensuring the input time series is sane.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V1-P07. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| run_id | string | 2026-02-16T09:30Z_01 | Unique run identifier |
| missing_bar_count | int | 0 | Expected-actual minutes |
| duplicate_timestamp_count | int | 0 | Hard fail if >0 |
| ohlc_sanity_fail_count | int | 0 | Hard fail if >0 |
| max_gap_minutes | int | 1 | Largest consecutive gap |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- **DQ KPI tooltip:** show counts and a plain-language impact note (e.g., “Forecasts may be unreliable”).
- **Gap table tooltip:** start/end of gap, length, session context.

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
- Early close / unusual session → expected bars differ; use a trading calendar reference.
- DST day → local time discontinuity; use UTC storage to avoid false gaps.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- Primary key uniqueness check passes.
- Gap report totals reconcile to missing_bar_count.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- **Automation:** run DQ checks as a required pipeline stage; persist snapshot JSON per run_id.
- **Dashboard:** other pages should read DQ state and show consistent banners.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
