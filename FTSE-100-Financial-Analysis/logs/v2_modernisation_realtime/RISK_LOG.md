# RISK LOG — V2

| Risk ID | Category | Risk | Likelihood | Impact | Mitigation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| V2-RISK-001 | Data | Provider limits prevent true multi-day intraday history | High | Medium | Daily anchor + intraday simulation; cache; clearly label | Mitigated |
| V2-RISK-002 | Ops | Exports might be generated from inconsistent sources (gold vs mart) | Medium | High | Enforce mart-only export pipeline | Mitigated |
| V2-RISK-003 | Governance | Events/news feeds are stubs; risk of misinterpretation | Medium | Medium | Label as stub; add roadmap; optional integration only | Mitigated |
| V2-RISK-004 | Reference | Constituents weights are demo weights | High | Medium | Explicit `source` field + docs; optional equal-weight mode | Accepted |