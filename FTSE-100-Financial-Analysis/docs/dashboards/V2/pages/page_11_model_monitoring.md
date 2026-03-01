---
page_id: V2-P11
page_name: Model Monitoring
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
primary_grain: run + intraday
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# Model Monitoring

## 1) Purpose
**One sentence purpose:**  
> Monitor forecasting performance, drift proxies, and alerting thresholds over time with an operational posture.

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. Is the selected model degrading in accuracy?
2. Do drift proxies suggest changing market dynamics?
3. When should we trigger retraining or switch models?

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
| mart.model_monitoring | run | Curated mart | daily close + hourly (session) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.model_monitoring | run | Curated mart | daily close + hourly (session) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.alerts_register | run | Curated mart | daily close + hourly (session) | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| Error Drift | Change in error vs baseline | RMSE_now - RMSE_base | Warn if > threshold | Triggers investigation |
| Data Drift Proxy | Shift in returns distribution | KS_stat(returns) | Warn if high | Proxy only |
| Last Retrain | Time since last training | now - retrain_time | Warn if > schedule | Config driven |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_error_drift`  
  - **Definition:** Error drift calculation  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    drift = rolling_RMSE - baseline_RMSE
    ```

- **Measure 02:** `m_distribution_shift`  
  - **Definition:** Returns distribution shift proxy  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    KS_test(recent_returns, baseline_returns)
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
| V1 | Line | Error Drift Timeline | mart.model_monitoring | Degradation visibility | Hover |
| V2 | Histogram | Returns Distribution (recent vs baseline) | mart.model_monitoring | Drift proxy | Toggle windows |
| V3 | Table | Alerts & Breaches | mart.alerts_register | Operational trace | Sort |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Last 180 sessions | Applies to all visuals unless noted |
| Interval | dropdown | 1d | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Near real-time | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P21 Incident Timeline
  - V2-P10 Backtesting Report
- **Cross-page filter behaviour:** Cross-page filters: enabled (model selection)

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
**Expected runtime:** < 90s  
**Freshness SLA:** 1 hour  
**Latency notes:** If drift breaches, document incident and link to playbook

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
- `docs/dashboards/V2/exports/v2_page_11_model_monitoring.png`

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
**Monitoring page:** answers “is the model still behaving?” with drift + error + data health signals.
This is critical for the ‘real-time platform’ credibility.

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P11. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| as_of_london | datetime | 2026-02-16 10:05 | London time |
| model_name | string | LSTM | Model |
| model_version | string | lstm_v2.3.0 | Version |
| rmse_roll | float | 1.2 | Rolling RMSE |
| mae_roll | float | 0.9 | Rolling MAE |
| drift_metric | float | 0.15 | Error drift or KS/PSI |
| drift_status | string | WARN | OK/WARN/FAIL |
| dq_score | float | 98.0 | 0-100 |
| freshness_minutes | int | 3 | minutes |
| run_id | string | 2026-02-16T10:05Z_02 | Run identifier |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Monitoring tooltip: model+version, rolling errors, drift metric, status, DQ score, freshness.

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
- False positives during regime changes → show regime context (link to V2-P03).
- Drift metrics require baseline window → document baseline selection.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- drift_status must match threshold bands from KPI catalogue/config.
- Rolling window lengths match documentation.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- Implement alert rules and reference them in Mermaid monitoring sequence diagram.
- Include a “last retrain date” field for transparency.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
