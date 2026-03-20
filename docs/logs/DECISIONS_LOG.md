# Decisions Log (ADR-lite)

This is a lightweight architecture/analytics decision register for the project.

> Use this alongside `CHANGELOG.md` to understand **why** the repo is structured the way it is.

---

## ADR-001 — Split delivery into V1 (dissertation baseline) and V2 (modern platform)
- **Decision:** keep V1 as a faithful “replay” of the dissertation narrative; build V2 as production-style medallion + monitoring.
- **Rationale:** reviewers can map V1 to the academic story and still see real-world engineering in V2.
- **Impacted paths:** `v1_dissertation_baseline/`, `v2_modernisation_realtime/`, `docs/dashboards/*`

## ADR-002 — Standardise on London time (Europe/London) for all timestamps
- **Decision:** all datasets and dashboard labels use Europe/London.
- **Rationale:** UK market authenticity; avoids “UTC drift” for session windows.
- **Impacted paths:** `src/ftse100/time_utils.py`, V1 cleaning + V2 transforms.

## ADR-003 — Export everything in 4K (3840×2160)
- **Decision:** dashboard export artefacts are always 4K PNG.
- **Rationale:** portfolio review quality (Zoom/Teams screen share) + consistent layout.
- **Impacted paths:** `docs/dashboards/V1/exports/`, `docs/dashboards/V2/exports/`

## ADR-004 — Make V2 dashboards read from `mart.*` parquet only
- **Decision:** exports must not compute metrics “on the fly” from raw tables.
- **Rationale:** production BI expectations: stable semantic layer + reproducible outputs.
- **Impacted paths:** `v2_modernisation_realtime/data/mart/`, V2 export scripts.

## ADR-005 — Include a frozen FTSE100 constituents universe snapshot
- **Decision:** store a universe snapshot with tickers, sectors, weights and as-of date.
- **Rationale:** sector weights, movers context, and a credible “index universe loader”.
- **Impacted paths:** `data/reference/ftse100_constituents_universe_snapshot.csv`

## ADR-006 — Keep macro/earnings events as a stub (extensible)
- **Decision:** start with a CSV-driven events overlay and document extension points.
- **Rationale:** realistic repo structure without binding to paid feeds.
- **Impacted paths:** `data/reference/events/`, `v2_modernisation_realtime/data/mart/events_overlay.*`

## ADR-007 — Maintain CSV mirrors of marts for portability
- **Decision:** publish `mart/*.csv` in addition to `mart/*.parquet`.
- **Rationale:** not all environments have parquet engines; DuckDB can read both.
- **Impacted paths:** `v2_modernisation_realtime/data/mart/`

## ADR-008 — Treat model explainability as “optional extension”
- **Decision:** provide stubs and documentation (SHAP/LIME) rather than shipping heavy artefacts.
- **Rationale:** keeps repo lightweight while showing modern ML thinking.
- **Impacted paths:** `docs/07_MODEL_CARDS.md` (if present), V2 roadmap.

---

## ADR cadence
- Add a new entry whenever we change: data sources, KPI definitions, model approach, or dashboard semantics.
