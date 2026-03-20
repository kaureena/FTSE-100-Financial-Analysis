# Power BI Pack (V2)

This folder contains the **Power BI styling + evidence pack** for the project.

It is designed to feel like a **UK market terminal**:
- dark base + neon accent strips
- subtle gradients + glow borders
- compact, dense panels
- executive-friendly donut/pie and gauge visuals

---

## Evidence exports (4K)

Exports live under:
- `exports/`

These are static PNGs that show how a premium Power BI dashboard could look.

---

## Theme
- `theme/powerbi_theme_uk_neon_terminal.json`

Import via:
Power BI → View → Themes → Browse for themes.

---

## Measures
- `measures/dax_measures.md` (templates)

---

## Data model
Recommended import tables (marts):
- `market_overview`
- `sector_rotation`
- `drawdown_risk`
- `top_movers`
- `pipeline_health`
- `latency_sla`
- `forecasting_metrics`
- `model_monitoring`
- `events_overlay`

Source:
- `../data/mart/`

---

## Notes
- The Power BI pack complements the Plotly-based export packs under `docs/dashboards/`.
- It exists because the original Power BI/Tableau dashboards are not currently available, but the repo should still show **premium BI realism**.
