---
page_id: V2-P05
page_name: Correlation Heatmap
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
primary_grain: daily (constituent returns)
timezone: Europe/London
currency: GBP
export_resolution: 3840×2160 preferred (min 2560×1440)
run_id_policy: Required on every export
---

# Correlation Heatmap

## 1) Purpose
**One sentence purpose:**  
> Visualise rolling correlation structure (index/constituents/sectors) to show diversification and stress clustering.

**Why this page exists (business value):**
- Provides a decision-quality view of the relevant market slice in a UK trading-desk style.
- Uses curated marts to keep metrics consistent and auditable.
- Includes trust signals (freshness, DQ, run_id) to support operational credibility.

---

## 2) Primary questions this page answers
1. Which instruments/sectors are moving together?
2. Has correlation increased during stressed regimes?
3. Are there clusters that explain index behaviour?

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
| mart.correlation_matrix | daily | Curated mart | daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.correlation_matrix | daily | Curated mart | daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |
| mart.correlation_pairs | daily | Curated mart | daily close | [DATA_CONTRACTS.md#v2-marts](../../../../DATA_CONTRACTS.md#v2-marts) |

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
| Avg Corr | Average off-diagonal correlation | mean(corr_ij) | Warn if > threshold | High correlation reduces diversification |
| Max Pair Corr | Largest pairwise correlation | max(corr_ij) | Info | Check for redundancy |
| Corr Shift | Change vs previous window | avg_corr_now - avg_corr_prev | Info | Tracks stress clustering |

**Threshold logic source:** `KPI_CATALOGUE.md` and/or `config/thresholds.yaml`

---

## 6) Measures catalogue (semantic layer)

List calculated measures used on this page (keep stable names across V2).

- **Measure 01:** `m_corr_rolling`  
  - **Definition:** Rolling correlation matrix  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    corr(window_returns)
    ```

- **Measure 02:** `m_cluster_id`  
  - **Definition:** Optional clustering label  
  - **Implementation:** Python  
  - **Formula:**  
    ```text
    cluster = hierarchical_clustering(corr)
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
| V1 | Heatmap | Rolling Correlation Matrix | mart.correlation_matrix | Relationship map | Hover |
| V2 | Heatmap | Correlation Shift (Δ) | mart.correlation_matrix | Stress view | Toggle Δ |
| V3 | Table | Top Correlated Pairs | mart.correlation_pairs | Actionable insight | Sort |

---

## 8) Filters & controls
| Control | Type | Default | Notes |
|---------|------|---------|------|
| Date range | picker | Last 90 sessions | Applies to all visuals unless noted |
| Interval | dropdown | 1d | Intraday vs daily controls |
| Horizon | dropdown | N/A | Forecast pages only |
| View mode | toggle | Replay | Replay vs near real-time (V2) |

---

## 9) Drilldowns & navigation
- **Recommended drillthrough targets:**
  - V2-P06 Sector Rotation
  - V2-P03 Volatility Regimes
- **Cross-page filter behaviour:** Cross-page filters: enabled (window selection)

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
**Expected runtime:** < 90s  
**Freshness SLA:** 24 hours  
**Latency notes:** Requires constituents list; if unavailable, show proxy set

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
- `docs/dashboards/V2/exports/v2_page_05_correlation_heatmap.png`

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
**Why correlation matters:** correlation spikes during stress and reduces diversification; this page makes that visible.
**How to read:**
- Heatmap shows pairwise correlations over a defined window (e.g., 20d or 60d).
- Watch for “all-high-corr” blocks (systemic risk) vs sector clusters (normal).
- Use the “Avg Corr” KPI as the quick health signal.
**Next step:** If correlation spikes, check **V2-P04** (risk) and **V2-P03** (regimes).

---

## 18) Data dictionary excerpt (minimum viable schema)
> This excerpt is the **minimum** required to render V2-P05. Full contracts live in `DATA_CONTRACTS.md`.

| Field | Type | Example | Rules / Notes |
|------|------|---------|---------------|
| as_of_date | date | 2026-02-16 | Correlation window end date |
| window_days | int | 60 | Rolling window length |
| ticker_i | string | HSBA.L | Constituent ticker |
| ticker_j | string | BP.L | Constituent ticker |
| corr | float | 0.42 | Pearson correlation of returns |
| method | string | pearson | pearson/spearman |
| run_id | string | 2026-02-16T10:05Z_02 | Run identifier |


---

## 19) Tooltip, formatting & interaction spec (make it feel “real-time”)
- Cell tooltip: as_of_date, tickers i/j, corr value, window length, method.
- KPI tooltip: Avg Corr definition = mean of off-diagonal corr values.

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
- Small constituent set → correlation may be unstable; show sample_n (#tickers used).
- Missing returns for a ticker in window → document imputation or exclusion policy.

---

## 21) Validation & reconciliation tests (must pass before 4K export)
- Corr values must be within [-1, 1].
- Avg Corr must reconcile to mean(off-diagonal) of the same matrix shown.

---

## 22) Implementation notes (Power BI / Python / Streamlit)
- If using Power BI, precompute correlations in Python and load as long-form table (ticker_i, ticker_j, corr) for stable rendering.
- Provide a method toggle (pearson/spearman) only if both are implemented and documented.

- For all pages: follow `assets/branding/REPO_THEME_GUIDE.md` and export via `DASHBOARD_EXPORT_RUNBOOK.md`.

## 23) Change log (page-level)
| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-02-16 | Initial spec draft | Baseline page spec created | Reena |
