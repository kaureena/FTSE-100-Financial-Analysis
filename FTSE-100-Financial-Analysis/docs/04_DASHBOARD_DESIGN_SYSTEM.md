# Dashboard Design System (UK Neon Terminal)

This repo’s dashboards are meant to feel like a **UK market terminal**.

---

## Layout principles
1. **Dense, grid-aligned panels**  
   - Minimise dead space  
   - Use consistent panel radius and spacing  
2. **Neon accent strip per panel**  
   - A thin strip at the top of each panel signals section identity  
3. **Glow borders (subtle)**  
   - Glow should support readability, not overpower charts  
4. **Typography hierarchy**  
   - Title (bold) → Subtitle (muted) → KPI label (muted) → KPI value (bold) → axis text (small)  
5. **Always show the as-of timestamp**  
   - Make freshness visible to avoid “fake real-time” perception  

---

## Visual vocabulary
- **Pulse / price movement:** line + last-point marker
- **Sector / composition:** donut/pie (weights), bar (returns)
- **Risk / stress:** drawdown chart, VaR proxy, risk gauge
- **Forecasting:** actual vs forecast, RMSE/MAE trends, drift indicators
- **Ops / reliability:** pipeline SLA gauge, latency p95 trend, incident timeline
- **Governance:** lineage diagram, KPI catalogue, data contracts

---

## Consistency checklist
- [ ] Page uses Europe/London time conventions
- [ ] KPI tiles use units
- [ ] Colour usage is consistent (neon accent strip, muted gridlines)
- [ ] Page has at least one “executive friendly” component (donut/gauge/table)
- [ ] Page has a footer disclaimer

---

## Where the design lives in this repo
- Plotly template: `assets/branding/plotly_template_uk_neon_terminal.json`
- Power BI theme: `assets/branding/powerbi_theme_uk_neon_terminal.json`
- Export packs:
  - `docs/dashboards/V1/exports/`
  - `docs/dashboards/V2/exports/`
  - `v2_modernisation_realtime/bi_powerbi/exports/`

