# REPO AUDIT LOG — Structure & Consistency Checks

This log is used to record audits of consistency between:
- specs ↔ artefacts
- naming ↔ contracts
- exports ↔ resolution requirements
- marts ↔ dashboard inputs

## Audit checklist (baseline)
- [x] Every dashboard page spec references existing datasets (or is clearly marked optional)
- [x] V2 dashboard exports read from mart parquet only
- [x] Exports are fixed-resolution (4K preferred) and pass export audit
- [x] Run register exists and is append-only
- [x] DQ issues are tracked in a register (with status and remediation evidence)
- [x] Constituents and events stubs are clearly labelled as non-official sources
- [x] Disclaimers present (Not financial advice)

## Audit history
| Date | Audit scope | Result | Notes |
|---|---|---|---|
| 2026-02-14 | Marts + DuckDB | PASS (after remediation) | Marts materialised; warehouse populated |
| 2026-02-15 | Export source of truth | PASS | V2 exports forced to read mart parquet only |
| 2026-02-16 | Terminal realism inputs | PASS (with caveats) | Weights/events are stubs; clearly labelled |
| 2026-02-17 | Governance logs | PASS | Logs expanded and centralised in `logs/` |

## Known limitations
- Any live data provider integration depends on external connectivity and provider terms.
- Events/news feeds in this repo are stubs unless explicitly integrated by the maintainer.
