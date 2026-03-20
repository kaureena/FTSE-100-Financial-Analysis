# Progress Log — Daily Timeline

A day-by-day delivery timeline for the repo.

> Portfolio note: this timeline is a reconstruction intended to show a realistic project delivery flow.


---

| Date (London) | Focus | Actions | Deliverables | Evidence |
|---|---|---|---|---|
| 2026-01-19 | Planning | Repo charter & UK terminal theme (colors, typography, naming). | Theme guide draft | `assets/branding/REPO_THEME_GUIDE.md` |
| 2026-01-20 | Planning | Dashboard Page Spec drafted (7 pages V1, 22 pages V2). | Spec pack | `docs/dashboards/` |
| 2026-01-21 | Planning | Mermaid architecture + lineage skeletons aligned to medallion pattern. | Mermaid set | `docs/mermaid/` |
| 2026-01-22 | Data | Reference data plan: FTSE100 constituents universe + sectors + weights. | Universe schema | `REFERENCE_DATA.md` |
| 2024-07-27 | V1 Data | Snapshot ingest (1m intraday) + cleaning + London TZ normalisation. | Clean dataset + metadata | `v1_dissertation_baseline/data/processed/` |
| 2024-07-28 | V1 DQ | DQ checks (gaps, duplicates, OHLC sanity) + DQ snapshot JSON. | DQ artefacts | `v1_dissertation_baseline/outputs/metrics/` |
| 2024-08-10 | V1 Models | ARIMA baseline training + 10-minute horizon forecasts. | ARIMA metrics + model summary | `v1_dissertation_baseline/outputs/metrics/arima_*` |
| 2024-08-11 | V1 Models | LSTM training pipeline + training history + forecast export. | LSTM metrics + history | `v1_dissertation_baseline/outputs/metrics/lstm_*` |
| 2024-08-12 | V1 Dashboards | V1 dashboard exports (7 pages) rendered at 4K. | V1 export pack | `docs/dashboards/V1/exports/` |
| 2026-02-13 | V2 Platform | Bronze/silver/gold scaffolding + parquet partitioning conventions. | Medallion storage | `v2_modernisation_realtime/data/` |
| 2026-02-14 | V2 Marts | Mart table design per page (market_overview, drawdown_risk, sector_rotation, etc.). | mart.* tables | `v2_modernisation_realtime/data/mart/` |
| 2026-02-15 | V2 Monitoring | DQ + latency + drift reports; incident timeline + pipeline run history. | Monitoring reports | `v2_modernisation_realtime/monitoring/reports/` |
| 2026-02-16 | V2 Exports | Standardised exports pipeline to read from mart parquet only; DuckDB warehouse populated. | 4K exports + DuckDB | `docs/dashboards/V2/exports/ ; v2_modernisation_realtime/db/` |
| 2026-02-17 | Terminal realism | Constituents loader + events enrichment stub; Power BI export pack; governance logs. | Universe/events + PBI exports + logs | `data/reference/ ; v2_modernisation_realtime/bi_powerbi/exports/ ; docs/logs/` |

---

## Milestone summary

- **V1 complete:** dissertation-style replay with ARIMA + LSTM + 7 dashboard pages.

- **V2 complete:** medallion tables + monitoring + 22 dashboard pages + UK market terminal realism.

- **Final polish:** Power BI export pack + operational governance logs.
