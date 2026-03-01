# Data Governance & Lineage

This repo includes “real-world” governance artefacts so it reads like a premium analytics delivery.

---

## Data contracts
See:
- `DATA_CONTRACTS.md`

Contracts define:
- required fields (timestamp, open/high/low/close/volume)
- schema expectations for marts
- constraints (e.g., high >= max(open,close), low <= min(open,close))

---

## Semantic layer discipline (V2)
V2 dashboards are designed to read from:
- `v2_modernisation_realtime/data/mart/*`

This means:
- KPI definitions are stable
- dashboards can be rebuilt in BI tools without rewriting metric logic
- monitoring is consistent (same definitions across pages)

---

## Lineage (diagram-first)
Mermaid diagrams:
- `docs/mermaid/01_end_to_end_architecture.mmd`
- `docs/mermaid/02_data_lineage_medallion.mmd`
- `docs/mermaid/04_forecasting_lifecycle.mmd`
- `docs/mermaid/06_monitoring_alerts_sequence.mmd`

V1 rendered diagrams:
- `v1_dissertation_baseline/docs/diagrams/v1_data_pipeline.png`
- `v1_dissertation_baseline/docs/diagrams/v1_dashboard_lineage.png`

---

## Governance registers
Folder:
- `docs/logs/`

Includes:
- Decisions / ADR-lite (`DECISIONS_LOG.md`)
- Assumptions (`ASSUMPTIONS_LOG.md`)
- Issue register (`issue_register.csv`)
- Model experiment log (`model_experiment_log.csv`)
- Dashboard review log (`dashboard_review_log.md`)

