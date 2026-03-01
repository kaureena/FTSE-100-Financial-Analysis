# V2 Dashboard Gallery — UK Market Analytics Platform (Neon Terminal)

V2 is the **premium modernisation** track: a UK-market analytics platform feel with:
- Near real-time refresh patterns (or replay fallback)
- DQ gates + run register + SLA health
- Forecasting cockpit + backtesting + monitoring
- Governance artifacts (KPI dictionary, measures catalogue, lineage, release notes)
- Consistent high-end exports (4K preferred)

> Goal: make this feel like a modern UK analytics product a hiring manager can trust.

---

## Folder layout

- Specs: `docs/dashboards/V2/pages/*.md`
- Exports: `docs/dashboards/V2/exports/*.png`

---

## Naming convention (do not change)

`v2_page_{NN}_{slug}.png`

Rules:
- `{NN}` = `01..22`
- `{slug}` lowercase and underscores only

---

## How to review V2 (recommended story order)

**Story A — Market behaviour**
- P01 Overview → P02 Intraday → P03 Vol regimes → P04 Drawdown → P05 Corr → P06 Sector → P07 Movers → P08 Technical

**Story B — Forecasting maturity**
- P09 Forecast cockpit → P10 Backtesting → P11 Monitoring

**Story C — Platform credibility**
- P12 DQ → P13 Pipeline health → P14 Latency/SLA → P21 Incident timeline → P22 Release notes

**Story D — Governance & traceability**
- P17 KPI dictionary → P18 Measures → P19 Inventory → P20 Lineage

---

## Pages (22-page premium pack)

| Page ID | Title | Spec | Export |
|---|---|---|---|
| V2-P01 | Footsie Pulse — Overview | [Spec](pages/page_01_footsie_pulse_overview.md) | [PNG](exports/v2_page_01_footsie_pulse_overview.png) |
| V2-P02 | Intraday Terminal | [Spec](pages/page_02_intraday_terminal.md) | [PNG](exports/v2_page_02_intraday_terminal.png) |
| V2-P03 | Volatility Regimes | [Spec](pages/page_03_volatility_regimes.md) | [PNG](exports/v2_page_03_volatility_regimes.png) |
| V2-P04 | Drawdown & Risk | [Spec](pages/page_04_drawdown_risk.md) | [PNG](exports/v2_page_04_drawdown_risk.png) |
| V2-P05 | Correlation Heatmap | [Spec](pages/page_05_correlation_heatmap.md) | [PNG](exports/v2_page_05_correlation_heatmap.png) |
| V2-P06 | Sector Rotation | [Spec](pages/page_06_sector_rotation.md) | [PNG](exports/v2_page_06_sector_rotation.png) |
| V2-P07 | Top Movers Watchlist | [Spec](pages/page_07_top_movers_watchlist.md) | [PNG](exports/v2_page_07_top_movers_watchlist.png) |
| V2-P08 | Technical Indicators | [Spec](pages/page_08_technical_indicators.md) | [PNG](exports/v2_page_08_technical_indicators.png) |
| V2-P09 | Forecasting Cockpit | [Spec](pages/page_09_forecasting_cockpit.md) | [PNG](exports/v2_page_09_forecasting_cockpit.png) |
| V2-P10 | Backtesting Report | [Spec](pages/page_10_backtesting_report.md) | [PNG](exports/v2_page_10_backtesting_report.png) |
| V2-P11 | Model Monitoring | [Spec](pages/page_11_model_monitoring.md) | [PNG](exports/v2_page_11_model_monitoring.png) |
| V2-P12 | Data Quality & Coverage | [Spec](pages/page_12_data_quality_coverage.md) | [PNG](exports/v2_page_12_data_quality_coverage.png) |
| V2-P13 | Pipeline Health & Refresh | [Spec](pages/page_13_pipeline_health_refresh.md) | [PNG](exports/v2_page_13_pipeline_health_refresh.png) |
| V2-P14 | Latency & SLA | [Spec](pages/page_14_latency_and_sla.md) | [PNG](exports/v2_page_14_latency_and_sla.png) |
| V2-P15 | Events Overlay | [Spec](pages/page_15_events_overlay.md) | [PNG](exports/v2_page_15_events_overlay.png) |
| V2-P16 | Board Pack One‑Pager | [Spec](pages/page_16_board_pack_one_pager.md) | [PNG](exports/v2_page_16_board_pack_one_pager.png) |
| V2-P17 | KPI Dictionary | [Spec](pages/page_17_kpi_dictionary.md) | [PNG](exports/v2_page_17_kpi_dictionary.png) |
| V2-P18 | Measure Catalogue | [Spec](pages/page_18_measure_catalogue.md) | [PNG](exports/v2_page_18_measure_catalogue.png) |
| V2-P19 | Data Inventory | [Spec](pages/page_19_data_inventory.md) | [PNG](exports/v2_page_19_data_inventory.png) |
| V2-P20 | Lineage Explained | [Spec](pages/page_20_lineage_explained.md) | [PNG](exports/v2_page_20_lineage_explained.png) |
| V2-P21 | Incident Timeline | [Spec](pages/page_21_incident_timeline.md) | [PNG](exports/v2_page_21_incident_timeline.png) |
| V2-P22 | Release Notes & Versions | [Spec](pages/page_22_release_notes_and_versions.md) | [PNG](exports/v2_page_22_release_notes_and_versions.png) |

---

## Export standards (V2)
- Preferred: **3840×2160 (4K)** PNG
- Footer always required (run_id + London timestamp + freshness + disclaimer)
- Design must follow: `assets/branding/REPO_THEME_GUIDE.md`

---

## Documentation links (source of truth)
- KPI definitions: `KPI_CATALOGUE.md`
- Measures and formulas: `METRICS_LIBRARY.md`
- Data contracts: `DATA_CONTRACTS.md`
- Export runbook: `DASHBOARD_EXPORT_RUNBOOK.md`
