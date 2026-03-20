# MEETING NOTES — Repo-wide

## Meeting: Kick-off (FTSE repo positioning)
Date: 2026-01-27 (Europe/London)

### Agenda
- Confirm final project selection: FTSE-100-Financial-Analysis
- Define V1 vs V2 narrative
- Define “UK market terminal realism” expectations

### Decisions
- Use V1 as dissertation baseline replication.
- Use V2 as platform-grade modernisation.
- Include premium dashboard exports (4K) with terminal-like theme.
- Add governance logs (issue/risk/decisions/time tracking) for credibility.

### Action items
- Draft dashboard page spec template and mermaid diagrams
- Prepare V1 pipeline + 7 exports
- Prepare V2 pipeline + marts + monitoring + 22 exports
- Add constituents + events realism
- Expand logs suite and centralise into `logs/`

---

## Meeting: Quality review (marts + exports)
Date: 2026-02-15 (Europe/London)

### Key findings
- Specs referenced mart tables not present.
- DuckDB warehouse was placeholder.
- Export resolution inconsistent.

### Decisions
- Materialise marts + load DuckDB.
- Force V2 exports from mart parquet only.
- Enforce fixed 4K export canvas + audit logs.

### Action items
- Add mart build logs, export audit logs, and run register.
