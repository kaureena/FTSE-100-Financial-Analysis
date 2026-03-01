---
page_id: "{{PAGE_ID}}"                     # e.g. V2-P01
page_name: "{{PAGE_NAME}}"                 # human readable title
version_track: "{{V1_OR_V2}}"              # V1 or V2
owner: "Reena"
reviewers: ["TBD"]
last_updated: "{{YYYY-MM-DD}}"
status: "Draft"                            # Draft | In Review | Approved
audience: ["Hiring Manager", "BI Analyst", "Data Engineer"]
dashboard_tool: "{{DASHBOARD_TOOL}}"       # Power BI | Tableau | Streamlit | Plotly | Mixed
refresh_mode: "{{REFRESH_MODE}}"           # Near real-time | Replay | Daily close
timezone: "Europe/London"
currency: "GBP"
primary_grain: "{{PRIMARY_GRAIN}}"         # intraday_1m | intraday_5m | daily
export_target: "PNG"
export_resolution: "{{EXPORT_RESOLUTION}}" # 2560×1440 min, 3840×2160 preferred
run_id_policy: "Required on every export"
---

# {{PAGE_NAME}}

## 0) Executive summary (for reviewers)
- **What this page is:** {{EXEC_SUMMARY_1}}
- **Why it matters:** {{EXEC_SUMMARY_2}}
- **How to trust it:** {{EXEC_SUMMARY_3}}

---

## 1) Purpose
**One sentence purpose:**  
> {{PURPOSE_ONE_LINER}}

**Business value (why this exists):**
- {{VALUE_POINT_1}}
- {{VALUE_POINT_2}}
- {{VALUE_POINT_3}}

**Success looks like:**
- {{SUCCESS_CRITERIA_1}}
- {{SUCCESS_CRITERIA_2}}
- {{SUCCESS_CRITERIA_3}}

---

## 2) Primary questions this page answers
1. {{QUESTION_1}}
2. {{QUESTION_2}}
3. {{QUESTION_3}}

---

## 3) User stories (portfolio-grade)
- As a **reviewer**, I can {{USER_STORY_1}}.
- As an **analyst**, I can {{USER_STORY_2}}.
- As an **engineer**, I can {{USER_STORY_3}}.

---

## 4) Scope
**In-scope:**
- {{IN_SCOPE_1}}
- {{IN_SCOPE_2}}
- {{IN_SCOPE_3}}

**Explicitly out-of-scope (prevents scope creep):**
- {{OUT_SCOPE_1}}
- {{OUT_SCOPE_2}}
- {{OUT_SCOPE_3}}

---

## 5) Intended audience & usage pattern
**Audience:** {{AUDIENCE}}  
**Typical usage:** {{USAGE_PATTERN}}  
**Decision context:** {{DECISION_CONTEXT}}

---

## 6) Data sources & contracts

### 6.1 Inputs (tables/files)
| Input | Grain | Source | Refresh | Owner | Contract | Critical? |
|------|------|--------|---------|-------|----------|-----------|
| {{INPUT_1}} | {{GRAIN_1}} | {{SOURCE_1}} | {{REFRESH_1}} | {{OWNER_1}} | {{CONTRACT_1}} | {{CRITICAL_1}} |
| {{INPUT_2}} | {{GRAIN_2}} | {{SOURCE_2}} | {{REFRESH_2}} | {{OWNER_2}} | {{CONTRACT_2}} | {{CRITICAL_2}} |
| {{INPUT_3}} | {{GRAIN_3}} | {{SOURCE_3}} | {{REFRESH_3}} | {{OWNER_3}} | {{CONTRACT_3}} | {{CRITICAL_3}} |

### 6.2 Minimum viable schema (what columns must exist)
| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| {{SCHEMA_FIELD_1}} | {{SCHEMA_TYPE_1}} | {{SCHEMA_EX_1}} | {{SCHEMA_RULE_1}} |
| {{SCHEMA_FIELD_2}} | {{SCHEMA_TYPE_2}} | {{SCHEMA_EX_2}} | {{SCHEMA_RULE_2}} |
| {{SCHEMA_FIELD_3}} | {{SCHEMA_TYPE_3}} | {{SCHEMA_EX_3}} | {{SCHEMA_RULE_3}} |

> Extend the schema list for pages that need more fields (e.g., forecasts, correlation matrices, model monitoring).

### 6.3 Timezone & session rules (UK authenticity)
- **All timestamps displayed in Europe/London** (GMT/BST as applicable).
- **London session framing:** {{SESSION_RULES}}
- **Weekends & UK bank holidays:** {{CALENDAR_RULES}}
- **DST handling:** explicitly document how duplicated/missing local hours are handled.

---

## 7) KPI tiles (definitions + thresholds)
| KPI | Definition | Calculation | Unit | Target/Threshold | Alert behaviour |
|-----|------------|-------------|------|------------------|----------------|
| {{KPI_1}} | {{KPI_1_DEF}} | {{KPI_1_CALC}} | {{KPI_1_UNIT}} | {{KPI_1_THRESH}} | {{KPI_1_ALERT}} |
| {{KPI_2}} | {{KPI_2_DEF}} | {{KPI_2_CALC}} | {{KPI_2_UNIT}} | {{KPI_2_THRESH}} | {{KPI_2_ALERT}} |
| {{KPI_3}} | {{KPI_3_DEF}} | {{KPI_3_CALC}} | {{KPI_3_UNIT}} | {{KPI_3_THRESH}} | {{KPI_3_ALERT}} |

**Threshold source of truth:** `KPI_CATALOGUE.md` + `config/thresholds.yaml` (V2)

---

## 8) Measures catalogue (semantic layer)
List calculated measures used on this page (stable names; avoid breaking changes).

- **Measure 01:** `{{MEASURE_1}}`  
  - Definition: {{MEASURE_1_DEF}}  
  - Implementation: {{MEASURE_1_IMPL}}  
  - Formula:
    ```text
    {{MEASURE_1_FORMULA}}
    ```
  - Dependencies: {{MEASURE_1_DEPS}}

- **Measure 02:** `{{MEASURE_2}}`  
  - Definition: {{MEASURE_2_DEF}}  
  - Implementation: {{MEASURE_2_IMPL}}  
  - Formula:
    ```text
    {{MEASURE_2_FORMULA}}
    ```
  - Dependencies: {{MEASURE_2_DEPS}}

---

## 9) Visual components (layout + intent)

### 9.1 Layout map (12-column grid standard)
```
┌───────────────────────────────────────────────────────────────────────────┐
│ Header: Page title | London timestamp | freshness | run_id                │
├───────────────────────────────────────────────────────────────────────────┤
│ KPI Tile 1 | KPI Tile 2 | KPI Tile 3 | KPI Tile 4 (optional)              │
├───────────────────────────────────────────────────────────────────────────┤
│ Primary chart (trend/candles/heatmap)                                     │
├───────────────────────────────────────────────────────────────────────────┤
│ Secondary chart(s)                      | Supporting table/diagnostics    │
└───────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Visual inventory
| Visual ID | Type | Title | Input(s) | Purpose | Interaction | Tooltip must include |
|-----------|------|-------|----------|---------|------------|----------------------|
| V1 | {{VIS_1_TYPE}} | {{VIS_1_TITLE}} | {{VIS_1_INPUT}} | {{VIS_1_PURPOSE}} | {{VIS_1_INTERACT}} | {{VIS_1_TOOLTIP}} |
| V2 | {{VIS_2_TYPE}} | {{VIS_2_TITLE}} | {{VIS_2_INPUT}} | {{VIS_2_PURPOSE}} | {{VIS_2_INTERACT}} | {{VIS_2_TOOLTIP}} |
| V3 | {{VIS_3_TYPE}} | {{VIS_3_TITLE}} | {{VIS_3_INPUT}} | {{VIS_3_PURPOSE}} | {{VIS_3_INTERACT}} | {{VIS_3_TOOLTIP}} |

### 9.3 Formatting rules (consistent premium look)
- Number formatting: {{NUMBER_FORMAT_RULES}}
- Axes: {{AXIS_RULES}}
- Legends: {{LEGEND_RULES}}
- Colour semantics: Up/Down/Warning/Info must follow theme guide.

---

## 10) Filters & controls
| Control | Type | Default | Applies to | Notes |
|---------|------|---------|------------|------|
| Date range | picker | {{FILTER_DATE_DEFAULT}} | All visuals | London time boundaries |
| Interval | dropdown | {{FILTER_INTERVAL_DEFAULT}} | Intraday visuals | 1m/5m/1d |
| Horizon | dropdown | {{FILTER_HORIZON_DEFAULT}} | Forecast pages | 1–10 steps |
| View mode | toggle | {{FILTER_VIEWMODE_DEFAULT}} | Whole page | Near real-time vs replay |

---

## 11) Drilldowns & navigation
- Primary drillthrough:
  - {{DRILL_1}}
  - {{DRILL_2}}
- Cross-page filters: {{CROSS_FILTER_BEHAVIOUR}}
- “What next?” links (forces a narrative):
  - {{WHAT_NEXT_1}}
  - {{WHAT_NEXT_2}}

---

## 12) Data Quality (DQ) & trust signals
**DQ checks required for this page:**
- {{DQ_RULE_1}}
- {{DQ_RULE_2}}
- {{DQ_RULE_3}}

**Trust banner rules (recommended):**
- Show **GREEN** when freshness and DQ pass.
- Show **AMBER** when freshness is borderline or minor DQ warnings exist.
- Show **RED** when DQ fails (block interpretability of forecasts).

**DQ artefacts:**
- `docs/logs/07_dq_issue_register.csv`
- `docs/logs/refresh_run_register.csv`

---

## 13) Refresh & performance expectations
**Refresh cadence:** {{REFRESH_CADENCE}}  
**Expected runtime:** {{EXPECTED_RUNTIME}}  
**Freshness SLA:** {{FRESHNESS_SLA}}  
**Latency notes:** {{LATENCY_NOTES}}

**Performance budget (recommended):**
- Page load/render: < 2s (cached) / < 5s (uncached)
- Max rows scanned per view: {{PERF_MAX_ROWS}}
- Cache strategy: {{CACHE_STRATEGY}}

---

## 14) Interpretation guide (how to read the page)
- {{INTERPRET_1}}
- {{INTERPRET_2}}
- {{INTERPRET_3}}

**Do-not-misread warnings:**
- {{MISREAD_1}}
- {{MISREAD_2}}

---

## 15) Edge cases & failure modes
- {{EDGE_1}}
- {{EDGE_2}}
- {{EDGE_3}}

**Fallback behaviour (must be explicit):**
- {{FALLBACK_1}}
- {{FALLBACK_2}}

---

## 16) Validation & reconciliation tests (must pass before export)
- {{VALIDATION_1}}
- {{VALIDATION_2}}
- {{VALIDATION_3}}

---

## 17) Compliance & disclaimers
- **Not financial advice.**
- Dataset limitations and assumptions: `DATA_README.md`
- Data contracts: `DATA_CONTRACTS.md`
- Methods & metrics: `METRICS_LIBRARY.md`
- Privacy: no personal data processed.

---

## 18) Screenshot/export references (evidence pack)
**High-res export file(s):**
- `{{EXPORT_PATH}}`

**Export checklist (hard requirements):**
- [ ] Resolution meets target (min 2560×1440; preferred 3840×2160)
- [ ] Dark theme enabled (UK Neon Terminal)
- [ ] Footer shows: `run_id`, London timestamp, freshness, “Not financial advice”
- [ ] Page index links work
- [ ] Export stored in evidence pack (V1 or V2)

---

## 19) Acceptance criteria (definition of done)
- [ ] Page renders without errors
- [ ] KPIs reconcile to input tables/files within tolerance
- [ ] Filters behave as specified
- [ ] DQ checks pass (or issues logged + banner visible)
- [ ] Export exists and is linked from `page_index.md`
- [ ] Interpretation guide + limitations included
- [ ] Evidence artefacts saved (run register, DQ report snapshot)

---

## 20) QA checklist (pre-release)
- [ ] Labels and units correct (points, %, GBP where applicable)
- [ ] No broken links
- [ ] Colour contrast acceptable
- [ ] Tooltips show London timestamp + units
- [ ] Re-run reproducibility checked (snapshot or tolerance)
- [ ] Export filename matches convention exactly

---

## 21) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| {{YYYY-MM-DD}} | Initial spec draft | Baseline page spec created | Reena |
