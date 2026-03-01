# CHANGELOG — FTSE-100-Financial-Analysis

This changelog captures release-level changes across the entire repository.
Versioning uses a pragmatic SemVer style: MAJOR.MINOR.PATCH.

## [2.5.0] — 2026-02-17 — Logs Pack Expansion (Governance Upgrade)
### Added
- Centralised `logs/` folder with **dense, audit-ready** logs for:
  - Repo-wide governance
  - V1 dissertation baseline execution
  - V2 modern platform execution
- Expanded registers:
  - Issue register, risk log, decision log, assumptions log
  - Pipeline run register, DQ run log, incident register
  - Model experiment log, monitoring log, backtesting log
  - Export audits (V1 + V2), dashboard review log, Power BI QA log
- Time tracking:
  - Daily timelog, weekly hours, detailed hours breakdown

### Improved
- Cross-linking: every entry points to evidence paths inside the main repo.
- UK authenticity: London session framing, Europe/London timestamps, GBP conventions.

---

## [2.4.0] — 2026-02-16 — Terminal Realism + Governance Pack
### Added
- Constituents universe loader (tickers, sectors, portfolio demo weights)
- Events enrichment stub (macro + earnings + optional news headlines)
- Power BI export pack (4K PNGs) including donut/pie + gauge visuals
- Expanded documentation and logs (initial governance pack)

---

## [2.3.0] — 2026-02-15 — V2 Exports Read From Mart Parquet Only
### Changed
- V2 export generation reads exclusively from `v2_modernisation_realtime/data/mart/*.parquet`
- Added export-only runner for fast regeneration

---

## [2.2.0] — 2026-02-14 — Mart Layer + DuckDB Warehouse (Platform Completion)
### Added
- Materialised `mart` layer and populated DuckDB warehouse with bronze/silver/gold/mart tables
- Run register and pipeline health artefacts

---

## [2.1.0] — 2026-02-12 — V2 Modernisation (Medallion + Monitoring)
### Added
- Bronze/Silver/Gold data zones
- DQ, monitoring snapshots, SLA/latency artefacts
- Neon terminal dashboard export pack (22 pages)

---

## [1.0.0] — 2024-008-08 — V1 Dissertation Baseline (Reproducible)
### Added
- V1 dataset snapshot (intraday 1m) + DQ checks
- ARIMA baseline forecast (10-minute horizon)
- LSTM forecast (60-lookback sequence) + metrics and comparison
- 7-page V1 dashboard export pack
