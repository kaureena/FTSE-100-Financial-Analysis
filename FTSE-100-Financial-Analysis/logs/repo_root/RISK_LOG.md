# RISK LOG — Repo-wide

Likelihood/Impact scale: Low / Medium / High  
Owner is the accountable role, not necessarily a single person.

| Risk ID | Category | Risk statement | Likelihood | Impact | Mitigation / control | Owner | Status | Last review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RISK-001 | Data | Market data provider limitations (intraday history, throttling) | Medium | High | Provider layer + caching + snapshot fallback; document limitations | V2 Data Lead | Mitigated | 2026-02-12 |
| RISK-002 | Compliance | Misinterpretation of outputs as financial advice | Low | High | Prominent disclaimers in dashboards and docs; avoid buy/sell language | Repo Owner | Mitigated | 2026-02-05 |
| RISK-003 | Dashboards | Inconsistent export resolution reduces portfolio polish | Medium | Medium | Enforce fixed 4K canvas; export audit log | Dashboard Owner | Mitigated | 2026-02-14 |
| RISK-004 | Governance | Dangling references in specs (mart tables not materialised) | Medium | High | Materialise mart layer + DuckDB; update export pipeline to mart-only | Platform Owner | Mitigated | 2026-02-15 |
| RISK-005 | Data | Constituents weights are not official index weights | High | Medium | Mark as portfolio demo weights; provide weight method and validation checks | Data Lead | Accepted | 2026-02-16 |
| RISK-006 | Events | Events calendar is a stub; could be mistaken for production feed | Medium | Medium | Label as stub; provide enrichment roadmap; optional integration hooks only | Data Lead | Mitigated | 2026-02-16 |
| RISK-007 | ML | LSTM variability across runs (non-determinism) | Medium | Medium | Set seeds where possible; log training config; snapshot outputs | ML Owner | Mitigated | 2026-02-08 |
| RISK-008 | Ops | No real CI evidence of build in clean environment | Low | Medium | CI workflow + smoke tests + logs | Repo Owner | Mitigated | 2026-02-14 |

## Risk review cadence
- Weekly during active build phases
- Before any “release” (tagged zip handover)
- After any major structural change (marts/warehouse/exports)
