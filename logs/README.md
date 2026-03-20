# FTSE-100-Financial-Analysis — Logs Pack (Logs Only)

This ZIP contains **only log artefacts**, organised into a single `logs/` folder to keep governance and execution traceability in one place.

## Purpose of this pack
These logs are designed to make the repository feel **UK-market / enterprise-grade** by documenting:
- What was built (V1 dissertation baseline + V2 modern platform)
- Why decisions were made (trade-offs, constraints, governance)
- How time was spent (hours tracking + weekly summaries)
- What went wrong / risks (issue register, risk log, incident register)
- How quality is maintained (DQ run log, export audit, dashboard QA)

## Folder structure
- `logs/repo_root/` — cross-project governance logs for the whole repo
- `logs/v1_dissertation_baseline/` — V1-only execution logs (dissertation replication)
- `logs/v2_modernisation_realtime/` — V2-only platform logs (medallion + marts + monitoring + terminal)
- `logs/templates/` — schemas and templates used to keep logging consistent

## UK conventions used throughout
- **Timezone:** Europe/London (GMT/BST)
- **Currency:** GBP where relevant
- **Index units:** FTSE level in points; returns in %

## Not financial advice
All dashboards, forecasts, and analysis outputs referenced by these logs are for **portfolio / educational** purposes only.
