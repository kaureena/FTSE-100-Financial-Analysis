---
page_id: V2-P12
page_name: Data Quality & Coverage
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
primary_grain: run (dataset-level)
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# Data Quality & Coverage

## 1) Purpose
**One sentence purpose:**  
> DQ scorecard for raw/staged/curated datasets with explicit rules, coverage metrics, and issue register links.

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. Is data complete and consistent for the selected window?
2. Are there timestamp gaps/duplicates or OHLC anomalies?
3. Which issues are currently open and what is their impact?

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
| mart.data_quality_health | run | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.data_quality_health | run | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.dq_issue_register | run | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| DQ Score | Overall DQ score (0–100) | weighted_rule_pass_rate | >= 95 | Threshold adjustable |
| Missing Bars | Missing intraday bars count | expected - actual | 0 preferred | Flag gaps > 0 |
| Open Issues | Count of open DQ issues | count(open) | 0 preferred | Link to register |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_dq_score`  
  - **Definition:** Weighted pass rate of DQ rules  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    score = sum(weight_i * pass_i) / sum(weights)
    ```

- **Measure 02:** `m_gap_summary`  
  - **Definition:** Gap count and duration summary  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    gaps = groupby(diff(timestamp)>interval)
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
| V1 | Table | DQ Rule Scorecard | mart.data_quality_health | Trust view | Sort |
| V2 | Bar | Gaps & Missingness | mart.data_quality_health | Coverage diagnostics | Hover |
| V3 | Table | DQ Issue Register (open) | mart.dq_issue_register | Operational follow-up | Filter by status |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Today + last 7 days | Applies to all visuals unless noted |
| Interval | dropdown | 5m | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Near real-time | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P13 Pipeline Health & Refresh
  - V2-P21 Incident Timeline
- **Cross-page filter behaviour:** Cross-page filters: enabled (dataset + date)

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
**Expected runtime:** < 60s  
**Freshness SLA:** 10 minutes  
**Latency notes:** DQ is a gate; if failing, downstream dashboards show warning banner

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
- `docs/dashboards/V2/exports/v2_page_12_data_quality_coverage.png`

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
**DQ coverage page:** shows completeness and sanity across all datasets that feed dashboards and models.
It is the platform-level trust layer (V2 equivalent of V1-P07).

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P12. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| run_id | string | 2026-02-16T10:05Z_02 | Run identifier |
| dataset_name | string | mart.market_overview | Dataset |
| dq_score | float | 98.0 | 0–100 |
| missingness_pct | float | 0.2 | % missing |
| duplicate_count | int | 0 | Hard fail if >0 |
| ohlc_fail_count | int | 0 | Hard fail if >0 |
| freshness_minutes | int | 3 | minutes |
| status | string | OK | OK/WARN/FAIL |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- DQ tooltip: dataset, dq_score breakdown, missingness, duplicates, last updated, run_id.

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
- Some marts are daily-only → do not penalise intraday missingness incorrectly; tag expected grain per dataset.
- DQ scoring weights changes → must be logged in release notes.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- DQ score matches weighted rule outputs; store rule-level detail in dq report JSON.
- Dataset list matches data inventory page (V2-P19).

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Expose DQ status as a shared banner component consumed by all pages.
- Keep a DQ issue register for auditability.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
