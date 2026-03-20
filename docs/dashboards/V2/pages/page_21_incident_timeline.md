---
page_id: V2-P21
page_name: Incident Timeline
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
primary_grain: incident-level
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# Incident Timeline

## 1) Purpose
**One sentence purpose:**  
> Operational incident timeline: DQ failures, refresh failures, model drift alerts, and resolution notes (MTTR).

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. What went wrong and when?
2. How quickly were incidents resolved?
3. What are recurring failure patterns and root causes?

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
| mart.incident_timeline | run | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.incident_register | run | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.incident_register | run | Curated mart | every 5 minutes (session) + daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| Open Incidents | Currently open incidents | count(open) | 0 preferred | Ops KPI |
| MTTR | Mean time to resolve | mean(resolution_time) | Lower is better | Ops maturity |
| Recurring Causes | Top recurring root causes | topk(cause) | Info | Focus improvements |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_incident_status`  
  - **Definition:** Incident status definition  
  - **Implementation:** Docs  
  - **Formula:**  
    ```text
    status in {open, mitigated, closed}
    ```

- **Measure 02:** `m_mttr`  
  - **Definition:** MTTR calculation  
  - **Implementation:** SQL/Python  
  - **Formula:**  
    ```text
    mttr = mean(closed_at - opened_at)
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
| V1 | Timeline | Incident Timeline | mart.incident_timeline | Ops history | Hover |
| V2 | Table | Incident Register | mart.incident_register | Details | Filter |
| V3 | Bar | Root Cause Frequency | mart.incident_register | Patterns | Hover |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Last 90 days | Applies to all visuals unless noted |
| Interval | dropdown | N/A | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Near real-time | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P13 Pipeline Health & Refresh
  - V2-P12 Data Quality & Coverage
- **Cross-page filter behaviour:** Cross-page filters: enabled (run_id + incident)

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
**Latency notes:** Incidents link to playbooks and run registers

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
- `docs/dashboards/V2/exports/v2_page_21_incident_timeline.png`

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
**Incident timeline:** proves operational maturity — issues happen, but you track them and learn.
Keep incidents realistic: DQ fails, provider outages, pipeline breaks.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P21. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| incident_id | string | INC-2026-02-16-001 | Unique id |
| opened_at_london | datetime | 2026-02-16 10:07 | London time |
| resolved_at_london | datetime | 2026-02-16 10:22 | London time (nullable) |
| severity | string | SEV2 | SEV1/SEV2/SEV3 |
| category | string | DQ_FAIL | DQ_FAIL/SLA_BREACH/PIPELINE_FAIL |
| summary | string | Duplicate timestamps detected | Short summary |
| root_cause | string | Provider resend caused duplicates | Plain English |
| action_taken | string | Dedup + replay | Fix |
| run_id | string | 2026-02-16T10:05Z_02 | Related run |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Incident tooltip: times, severity, category, summary, run_id.

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
- Incidents without resolution → highlight as open and list owner/next action.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- Incident times consistent (resolved >= opened).

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Link incidents to pipeline runs (V2-P13) and SLA breaches (V2-P14).

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
