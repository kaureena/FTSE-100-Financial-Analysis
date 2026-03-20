# UK Neon Terminal Theme Rules (v1.1)

This theme makes **FTSE-100-Financial-Analysis** feel like a UK-built, London trading-desk analytics product.
It is intentionally designed to be:
- **High-end** (clean hierarchy, controlled accents)
- **Operationally credible** (freshness + DQ + run_id on every export)
- **Recruiter-friendly** (self-explanatory visuals, glossary-backed KPIs)
- **UK authentic** (Europe/London time, Footsie language, LSE session framing)

---

## 1) Non‑negotiables (quality bar)

1) **Trust signals always visible**
   - Every export has a footer with `run_id`, London timestamp, freshness, and “Not financial advice”.
2) **Consistency across pages**
   - Same grid, same KPI tiles, same typography, same number formatting.
3) **Meaningful neon**
   - Neon is a semantic accent, never the background.
4) **UK conventions**
   - Display time in **Europe/London**.
   - Index level in **points**.
   - Percentages for returns; `+` sign for positive deltas.
   - Use “Footsie” sparingly as flavour; keep labels professional.
5) **No visual lies**
   - Axes must show units; avoid misleading truncated axes unless explicitly justified.

---

## 2) Colour system (hex)

### 2.1 Base colours (UI)
- Background: `#0B0F14`
- Panel: `#111826`
- Elevated panel: `#141D2D`
- Border / gridline: `#263248`
- Text primary: `#E6EDF7`
- Text secondary: `#A7B4C6`
- Muted label: `#71829B`

### 2.2 Semantic colours (meaning)
- Up / Positive: `#2DE38A`
- Down / Negative: `#FF5C7A`
- Warning: `#FFB020`
- Info: `#52A8FF`
- Accent (selection / focus): `#B067FF`
- Neutral highlight: `#38D9FF`

### 2.3 Rules (how to use colours)
- Up/Down must be paired with:
  - icon `▲` / `▼` and/or explicit “Up/Down” microcopy
- Warning must be used for:
  - stale data
  - DQ warnings (minor)
  - threshold breach warnings
- Red (Down) is reserved for:
  - negative deltas
  - DQ FAIL / pipeline FAIL (do not overuse)

---

## 3) Typography (trading terminal but corporate)

### Recommended font stacks
- Headings: `Inter` → fallback `Segoe UI` (Power BI friendly)
- Body: `Inter` / `Segoe UI`
- Monospace: `Roboto Mono` → fallback `Consolas` (tickers, run_id, hashes)

### Type scale
- Page title: 28–32px (600)
- Section header: 16–18px (600)
- KPI value: 28–36px (700)
- KPI label: 11–12px (500, tracking +2%)
- Axis labels: 11–12px
- Table text: 11–12px

---

## 4) Layout & spacing (12-column grid)

### Grid structure (standard)
- Header bar
- KPI row (3–4 tiles)
- Primary chart row
- Secondary row (chart + table/diagnostics)

### Spacing
- Base unit: 8px
- Panel padding: 16px
- Panel gap: 16px
- Safe margin for exports: 48px

---

## 5) Component standards

### 5.1 Header bar
Right-side header always shows:
- **London time**
- **Freshness**
- **run_id** (monospace)
- Optional: interval / horizon / selected ticker

### 5.2 KPI tiles (standard)
Each KPI tile contains:
- Label (muted)
- Value (large)
- Delta (▲/▼ + colour + unit)
- Micro-note (optional): “vs prev close”, “rolling(20)”
- Status chip (optional): OK / WARN / FAIL

### 5.3 Charts
- Gridlines: subtle (`#263248` at ~25% opacity)
- Legends: consistent order (actual → forecast → bands)
- Tooltips always include:
  - London timestamp
  - key measures with units
  - data source label (optional for trust)

### 5.4 Tables
- Zebra striping is allowed but subtle
- Always show units in column headers
- Default sort must be explicitly specified (e.g., “Return desc”)

---

## 6) Data trust banner (recommended)
Use a small banner at top of page:
- **GREEN** = Fresh + DQ pass
- **AMBER** = borderline freshness or minor DQ warnings
- **RED** = DQ fail or pipeline fail; show a “Do not interpret forecasts” warning

---

## 7) Footer standard (required for every export)
Format:
`run_id=... | London: DD Mon YYYY HH:MM | Freshness: Xm | Not financial advice`

---

## 8) Export standards (premium)
- Preferred export: **3840×2160 (4K)** PNG
- Minimum: **2560×1440**
- Enforce consistent aspect ratio across pages
- Filenames must match `page_index.md` exactly

---

## 9) Implementation guardrails (Power BI / Plotly / Streamlit)

### Power BI
- Use a theme JSON (optional) aligned to the palette above.
- Use measure naming conventions: `m_*` for measures, `kpi_*` for KPI definitions.
- Avoid custom visuals that break export consistency.

### Plotly
- Use dark background and controlled accent colours.
- Candlestick:
  - wick colour = text-secondary at reduced opacity
  - volume bars muted; spikes highlighted with warning colour

### Streamlit
- Create a global `theme.css` to enforce padding and fonts.
- Use caching:
  - `st.cache_data` for data loads
  - `st.cache_resource` for models
- Always print `run_id` + freshness in footer.

---

## 10) UK authenticity checklist
- [ ] London timezone shown (not UTC)
- [ ] Index level shown as “points”
- [ ] Returns are percentages with `+` sign
- [ ] Session framing mentioned (“London session”, “Daily close snapshot”)
- [ ] Disclaimers present (“Not financial advice”)


---

## 11) Theme assets (ready to use)
- Power BI theme: `assets/branding/powerbi_theme_uk_neon_terminal.json`
- Plotly template: `assets/branding/plotly_template_uk_neon_terminal.json`
