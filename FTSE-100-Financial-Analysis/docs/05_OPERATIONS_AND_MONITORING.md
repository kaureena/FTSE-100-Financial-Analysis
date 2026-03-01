# Operations & Monitoring (V2)

V2 is intentionally written like a small analytics platform.

---

## Monitoring artefacts (evidence)
Folder:
- `v2_modernisation_realtime/monitoring/reports/`

Key outputs:
- `dq_latest_session.csv` — latest DQ session checks and outcomes
- `pipeline_runs_last14d.csv` — recent pipeline history
- `latency_samples.csv` / `latency_sla.csv` — performance & SLA
- `model_metrics_timeseries.csv` — RMSE/MAE monitoring checkpoints
- `incident_timeline.csv` — incident timeline (portfolio register)
- `return_drift_last20_vs_prev20.json` — drift proxy

---

## Incident model (portfolio)
Incidents are recorded with:
- ID
- date/time
- severity
- symptoms
- impacted KPIs
- mitigation actions

See:
- `v2_modernisation_realtime/data/mart/incident_register.*`
- `v2_modernisation_realtime/data/mart/alerts_register.*`

---

## Run audit
Every refresh/export run should append to:
- `docs/logs/refresh_run_register.csv`

Purpose:
- prove “operational realism”
- show repeatability and traceability

---

## Production hardening ideas (roadmap)
- Alert routing: Slack/Teams/email with escalation policy.
- Automated remediation: retry + backfill for missed bars.
- Data contracts enforcement: schema drift detection.
- Model monitoring: champion/challenger + data drift + concept drift.

