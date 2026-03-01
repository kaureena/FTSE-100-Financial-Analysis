# DASHBOARD_EXPORT_RUNBOOK — Premium 4K Exports (V1 + V2)

This runbook ensures every dashboard export looks **consistent, high-end, and UK-authentic**.

---

## 1) Non-negotiable requirements
Every export must:
- Follow the UK Neon Terminal theme (`assets/branding/REPO_THEME_GUIDE.md`)
- Use the correct filename convention (from `page_index.md`)
- Include footer with:
  - `run_id`
  - London timestamp (Europe/London)
  - freshness note (minutes since refresh or “snapshot”)
  - “Not financial advice”

Preferred resolution:
- **3840×2160 (4K)**  
Minimum:
- **2560×1440**

---

## 2) Export workflow (recommended)

### Step A — Pre-export checks (trust gate)
- Confirm DQ status (V1-P07 or V2-P12)
- Confirm freshness (V2-P13 / V2-P14)
- Confirm correct filters:
  - date range
  - interval
  - horizon (if forecasting page)
  - view mode (near real-time vs replay)

### Step B — Export
Export to PNG.

### Step C — Store evidence
For each export, save:
- PNG to `docs/dashboards/V*/exports/`
- run register row to `docs/logs/refresh_run_register.csv`
- DQ snapshot summary (if any) to `docs/logs/07_dq_issue_register.csv` (only when issues exist)

---

## 3) Power BI export (high-resolution)
Best practice:
- Use a 16:9 canvas matching 3840×2160 ratio
- Ensure consistent font sizes (Inter/Segoe UI)

Export tips:
- Avoid “auto-fit” shrinking labels
- Keep margins; don’t place elements too close to canvas edges
- Use consistent tooltip formatting (London time, points, %)

---

## 4) Tableau export (high-resolution)
- Set dashboard size to a fixed 16:9
- Export as PNG at the highest available resolution
- Ensure consistent colour mapping and legends

---

## 5) Plotly export (Python)
For consistent PNG exports:
- Use a fixed figure size and scale factor
- Ensure background and font colours match theme guide
- Include a footer annotation for run_id + London timestamp

---

## 6) Streamlit export
Streamlit is interactive; for PNG exports:
- Use a “report mode” route:
  - renders each page at fixed size
  - captures screenshots via Playwright or built-in screenshot tooling
- Always stamp footer and freeze the run_id for that export batch

---

## 7) Footer standard (copy/paste)
`run_id=YYYY-MM-DDTHH:MMZ_xx | London: DD Mon YYYY HH:MM | Freshness: Xm | Not financial advice`

---

## 8) Export QA checklist (must pass)
- [ ] Resolution meets target
- [ ] Footer present and correct
- [ ] Timezone is Europe/London
- [ ] Units are correct (points / % / GBP)
- [ ] No overlapping labels
- [ ] Legends present where needed
- [ ] Export matches filename exactly

---

## 9) Common failure modes
- Stale data mistakenly exported → fix by checking freshness KPI
- Wrong interval (1m vs 5m) → confirm header shows interval
- Missing footer/run_id → export rejected (must redo)
- DQ fail not visible → add banner and/or block forecast interpretation
