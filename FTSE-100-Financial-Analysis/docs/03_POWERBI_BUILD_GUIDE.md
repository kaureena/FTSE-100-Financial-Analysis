# Power BI Build Guide (V2)

The repo includes a **Power BI export evidence pack** under:
- `v2_modernisation_realtime/bi_powerbi/exports/`

These are designed to look like a high-end UK market terminal:
- dark base, neon accent strips, glow borders
- donut/pie visuals for executive summaries
- gauge/speedometer visuals for risk/ops KPIs

---

## Data source (recommended): mart parquet + DuckDB

### Option A — Read from `mart/*.parquet`
Best when Power BI has parquet connectors available.

Folder:
- `v2_modernisation_realtime/data/mart/`

Suggested tables:
- `market_overview`
- `sector_rotation`
- `drawdown_risk`
- `top_movers`
- `pipeline_health`
- `latency_sla`
- `data_quality_health`
- `events_overlay`

### Option B — DuckDB semantic warehouse
If you want a single query endpoint for Power BI.

File:
- `v2_modernisation_realtime/db/warehouse.duckdb`

Suggested approach:
- Use DuckDB ODBC connector (or export to CSV if needed).
- Treat each `mart.*` table as a BI “fact” or “semantic view”.

---

## Theme / styling
Theme file:
- `assets/branding/powerbi_theme_uk_neon_terminal.json`
- (copy placed under `v2_modernisation_realtime/bi_powerbi/theme/`)

In Power BI:
1. View → Themes → Browse for themes → import JSON.
2. Set Page size to **16:9**.
3. Use compact grid, consistent KPI tile template, and standard typography.

---

## Visuals to include (premium feel)
- KPI tiles with neon accent strips
- Line charts for intraday close and volatility
- Donut charts for sector weights / breadth
- Gauge (speedometer) for risk score, SLA pass rate, drift score
- Dense tables for top movers and pipeline incidents

---

## Export settings (screenshots)
Recommended:
- 3840×2160 PNG export (4K)
- consistent naming: `pbi_page_XX_<slug>.png`

Repo evidence pack:
- `v2_modernisation_realtime/bi_powerbi/exports/README.md`

