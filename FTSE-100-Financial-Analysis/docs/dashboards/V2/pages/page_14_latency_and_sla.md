---
page_id: V2-P14
page_name: Latency & SLA
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
primary_grain: daily (ops metrics)
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# Latency & SLA

## 1) Purpose
**One sentence purpose:**  
> Break down end-to-end latency into ingestion/transform/model/export components and show SLA compliance trends.

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. Where does latency come from (ingestion vs modelling vs exports)?
2. Is latency stable across sessions?
3. Which changes improved or degraded SLA compliance?

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
| mart.latency_sla | run | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.latency_sla | run | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.latency_sla | run | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| Median Latency | Median end-to-end latency | median(latency) | Warn if > SLA | SLA configurable |
| p95 Latency | 95th percentile latency | p95(latency) | Warn if high | Tail risk for ops |
| SLA Pass Rate | % runs meeting SLA | count(pass)/N | >= 95% | Target can be adjusted |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_latency_total`  
  - **Definition:** Total latency minutes  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    latency = export_time - market_time
    ```

- **Measure 02:** `m_latency_component`  
  - **Definition:** Component latency  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    lat_comp = stage_end - stage_start
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
| V1 | Line | Latency Trend | mart.latency_sla | Trend view | Hover |
| V2 | Bar | Latency Breakdown (components) | mart.latency_sla | Where time goes | Hover |
| V3 | Table | SLA Breaches Detail | mart.latency_sla | Investigation list | Filter |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Last 30 runs | Applies to all visuals unless noted |
| Interval | dropdown | N/A | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Near real-time | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P13 Pipeline Health & Refresh
  - V2-P22 Release Notes & Versions
- **Cross-page filter behaviour:** Cross-page filters: enabled (run_id + version)

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
**Expected runtime:** < 30s  
**Freshness SLA:** 10 minutes  
**Latency notes:** Latency is measured end-to-end; refresh windows are London-session aware

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
- `docs/dashboards/V2/exports/v2_page_14_latency_and_sla.png`

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
**Latency & SLA:** answers “are we truly real-time?” with measurable latency components.
A premium dashboard shows p50/p95 latency and breach history.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P14. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| date | date | 2026-02-16 | Date |
| latency_p50_min | float | 1.2 | minutes |
| latency_p95_min | float | 3.8 | minutes |
| freshness_sla_min | int | 5 | SLA target |
| breach_count | int | 0 | breaches that day |
| run_id | string | 2026-02-16T10:05Z_02 | Run id (optional per row) |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Latency tooltip: date, p50/p95, SLA target, breaches.

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
- Outliers (network issues) dominate p95 → show both p95 and max plus counts.
- Session vs off-session latency differ → segment by session state.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- latency_p95 >= latency_p50 always.
- breach_count reconciles to run register.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Use a rolling 30-day SLA chart for credibility.
- Use consistent units (minutes) and avoid mixing seconds/minutes in visuals.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
