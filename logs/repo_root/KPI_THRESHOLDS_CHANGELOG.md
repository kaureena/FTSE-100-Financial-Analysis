# KPI / Thresholds Change Log

This log records any changes to KPI definitions, formatting, or alert thresholds.

## Principles
- Thresholds must be:
  - explicitly defined
  - versioned
  - explainable
- Do not silently change KPI calculations between releases.

## Change history
| Date | KPI/Rule | Change | Reason | Impact | Evidence |
|---|---|---|---|---|---|
| 2026-02-12 | Realised Vol (20) | Added warning threshold band | Needed risk signalling on dashboards | Adds OK/WARN status chip | `config/thresholds.yaml` |
| 2026-02-14 | DQ Score | Weighted pass rate formalised (0–100) | Standardise reporting | Consistent DQ across pages | `v2_modernisation_realtime/dq_data_quality/*` |
| 2026-02-15 | Freshness SLA | Set default SLA to 10 minutes in-session | Align with near real-time posture | Monitoring alerts use SLA | `logs/v2_modernisation_realtime/SLA_LATENCY_REPORT.md` |
