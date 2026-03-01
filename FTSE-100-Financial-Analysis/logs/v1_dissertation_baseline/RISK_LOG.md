# RISK LOG — V1

| Risk ID | Category | Risk | Likelihood | Impact | Mitigation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| V1-RISK-001 | Data | Intraday gaps break LSTM sequences and moving average continuity | Medium | Medium | DQ gap report + sequence padding rules + note in interpretation | Mitigated |
| V1-RISK-002 | Model | ARIMA assumes stationarity; may lag during rapid moves | High | Low | Use differencing + show residual diagnostics; narrative in report | Accepted |
| V1-RISK-003 | Model | LSTM overfitting or unstable performance on small samples | Medium | High | Scaling + seed + simple architecture + report metrics | Mitigated |