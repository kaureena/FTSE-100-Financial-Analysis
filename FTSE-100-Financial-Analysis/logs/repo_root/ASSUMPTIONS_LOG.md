# ASSUMPTIONS LOG — Repo-wide

Assumptions are tracked explicitly to improve credibility and reduce hidden risk.

| Assumption ID | Domain | Assumption | If false, impact | How we validate/monitor | Residual risk |
| --- | --- | --- | --- | --- | --- |
| ASM-001 | Data | Intraday timestamps displayed in Europe/London; session framing uses UK trading session | Dashboards show wrong session boundaries | Validate session window filtering rules; manual spot check | Low |
| ASM-002 | Data | Index-level volume is treated as a proxy; interpretations are descriptive only | Over-interpretation of volume signals | Add warnings in dashboard interpretation text | Medium |
| ASM-003 | Models | ARIMA is a baseline benchmark; LSTM is expected to better capture non-linear patterns | Model comparison narrative becomes inconsistent | Use objective MAE/RMSE and show both | Low |
| ASM-004 | V2 Ops | DQ gates run before exports; if failing, exports are flagged/blocked | Exports published from bad data | Export audit log + DQ status banner | Medium |
| ASM-005 | Reference | Constituents weights are demo weights, not official | Misleading claims about official index weights | Explicitly label as demo in docs/logs and dataset column `source` | High |
| ASM-006 | Events | Macro/earnings/news are stub feeds unless configured otherwise | Users assume it is a live feed | Label as stub + include roadmap section | Medium |