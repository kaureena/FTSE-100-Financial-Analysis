---
page_id: V2-P17
page_name: KPI Dictionary
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
primary_grain: dictionary
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# KPI Dictionary

## 1) Purpose
**One sentence purpose:**  
> A dashboard-native KPI glossary: definition, formula, unit, and interpretation for every KPI used in V2.

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. What does each KPI mean?
2. How is it calculated and what is the unit?
3. What thresholds exist and why?

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
| mart.kpi_dictionary | run | Curated mart | manual update (versioned) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.kpi_dictionary | run | Curated mart | manual update (versioned) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.kpi_usage_map | run | Curated mart | manual update (versioned) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| Total KPIs | Count of KPIs documented | count(rows) | Info | Completeness signal |
| KPIs with Thresholds | Count with explicit thresholds | count(threshold not null) | Info | Operational maturity |
| Last Updated | Last update date of catalogue | max(updated) | Info | Governance signal |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_kpi_id`  
  - **Definition:** Stable KPI identifier  
  - **Implementation:** Docs  
  - **Formula:**  
    ```text
    kpi_id = V2KPI###
    ```

- **Measure 02:** `m_kpi_unit`  
  - **Definition:** Unit and display formatting  
  - **Implementation:** Docs  
  - **Formula:**  
    ```text
    unit in {points, %, GBP, ratio}
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
| V1 | Table | KPI Catalogue | mart.kpi_dictionary | Definitions | Search + filter |
| V2 | Table | Thresholds & Alerts | mart.kpi_dictionary | Ops readiness | Filter |
| V3 | Table | KPI Usage Map (by page) | mart.kpi_usage_map | Traceability | Filter |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | All | Applies to all visuals unless noted |
| Interval | dropdown | N/A | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Replay | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P18 Measure Catalogue
  - V2-P20 Lineage Explained
- **Cross-page filter behaviour:** Cross-page filters: enabled (KPI selection)

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
**Refresh cadence:** manual update (versioned)  
**Expected runtime:** < 10s  
**Freshness SLA:** N/A  
**Latency notes:** This is documentation-as-data; used to keep dashboards consistent

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
- `docs/dashboards/V2/exports/v2_page_17_kpi_dictionary.png`

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
**KPI Dictionary page:** makes the repo auditable — reviewers can trace every KPI to a definition and formula.
This is key for professional credibility and consistency.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P17. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| kpi_id | string | V2KPI001 | Stable KPI id |
| kpi_name | string | Last | Display name |
| unit | string | points | points/%/GBP/etc |
| definition | string | ... | Plain English |
| formula | string | ... | Pseudo/DAX/Python |
| owner | string | Reena | Owner |
| pages | string | V2-P01,V2-P16 | Used on pages |
| version_introduced | string | v2.0.0 | Version |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- KPI tooltip: show unit, formula, owner, and where used.

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
- Duplicate KPI ids → hard fail.
- Changing KPI meaning without version bump → blocked.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- KPI ids unique.
- Every KPI referenced in dashboards exists in catalogue.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Back this page directly from `KPI_CATALOGUE.md` or a generated table to avoid drift.
- Add a search filter (contains) to quickly find KPIs.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
