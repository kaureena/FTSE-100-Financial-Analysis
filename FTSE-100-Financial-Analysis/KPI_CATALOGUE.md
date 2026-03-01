# KPI_CATALOGUE — KPI Dictionary & Threshold Policy

This is the KPI source of truth used by:
- Dashboard KPI tiles
- Alert banners (freshness / DQ / drift)
- Board Pack one-pager (executive summary)

> **Format rule:** KPIs must have stable names and clear units.

---

## 1) Threshold policy (V2)
Thresholds are stored in `config/thresholds.yaml` (preferred) and documented here.

Common threshold patterns:
- **Freshness** (minutes since refresh)
- **DQ score** (0–100)
- **Volatility** (rolling vol bands)
- **Latency** (p95 thresholds)
- **Drift** (distribution shift proxies)

---

<a id="v1-kpis"></a>
## 2) V1 KPIs (Dissertation baseline)

| KPI ID | Name | Unit | Definition | Calculation | Used on pages |
|---|---|---:|---|---|---|
| V1KPI001 | Last Close | points | Last close within the session | close[last_bar] | V1-P01 |
| V1KPI002 | Intraday Δ | % | Change vs session start | (close_last/close_first - 1)*100 | V1-P01 |
| V1KPI003 | Session Range | points | High - Low in session | max(high) - min(low) | V1-P01 |
| V1KPI004 | Avg Volume | bars | Average volume per bar | mean(volume) | V1-P02 |
| V1KPI005 | Max Volume Spike | bars | Max volume in session | max(volume) | V1-P02 |
| V1KPI006 | MA(20) Slope | points/bar | Trend of MA(20) | slope(ma20 over last N) | V1-P03 |
| V1KPI007 | Crossover Count | count | Count of close↔MA crosses | count(crossover_flag) | V1-P03 |
| V1KPI008 | MAE (ARIMA) | points | Mean abs error | mean(|y-yhat|) | V1-P04, V1-P06 |
| V1KPI009 | RMSE (ARIMA) | points | Root mean sq error | sqrt(mean((y-yhat)^2)) | V1-P04, V1-P06 |
| V1KPI010 | MAE (LSTM) | points | Mean abs error | mean(|y-yhat|) | V1-P05, V1-P06 |
| V1KPI011 | RMSE (LSTM) | points | Root mean sq error | sqrt(mean((y-yhat)^2)) | V1-P05, V1-P06 |
| V1KPI012 | DQ Missing Bars | count | Missing expected bars | expected - actual | V1-P07 |
| V1KPI013 | DQ Duplicates | count | Duplicate timestamps | count(dupes) | V1-P07 |
| V1KPI014 | DQ OHLC Failures | count | OHLC sanity failures | count(violations) | V1-P07 |

---

<a id="v2-kpis"></a>
## 3) V2 KPIs (Modern platform)

| KPI ID | Name | Unit | Definition | Calculation | Pages |
|---|---|---:|---|---|---|
| V2KPI001 | Last | points | Latest index level | last(close) | V2-P01 |
| V2KPI002 | Δ vs Prev Close | % | Change vs previous close | (close/prev_close-1)*100 | V2-P01 |
| V2KPI003 | Realised Vol (20) | % | Rolling realised vol proxy | std(r_20)*sqrt(20) | V2-P01, V2-P03 |
| V2KPI004 | VWAP (Proxy) | points | VWAP proxy for session | sum(tp*vol)/sum(vol) | V2-P02 |
| V2KPI005 | Gap Minutes | minutes | Missing minutes in session | sum(gap>1) | V2-P02, V2-P12 |
| V2KPI006 | Regime | label | Calm/Normal/Stressed | bucket(vol) | V2-P03 |
| V2KPI007 | Current Drawdown | % | Peak-to-trough from recent high | close/max(close)-1 | V2-P04 |
| V2KPI008 | VaR 95 | % | Value-at-Risk | q05(returns) | V2-P04 |
| V2KPI009 | Avg Corr | corr | Average off-diagonal corr | mean(corr_ij) | V2-P05 |
| V2KPI010 | Sector Dispersion | % | Dispersion of sector returns | std(sector_returns) | V2-P06 |
| V2KPI011 | RSI(14) | index | Momentum oscillator | RSI(close,14) | V2-P08 |
| V2KPI012 | Horizon MAE | points | MAE on selected horizon | MAE_h | V2-P09 |
| V2KPI013 | Rolling RMSE | points | Rolling RMSE | RMSE_roll | V2-P10 |
| V2KPI014 | Error Drift | points | Change vs baseline | RMSE_now - RMSE_base | V2-P11 |
| V2KPI015 | DQ Score | 0-100 | Weighted DQ rule pass rate | weighted_pass_rate | V2-P12 |
| V2KPI016 | Last Success | datetime | Last successful pipeline run | max(success_time) | V2-P13 |
| V2KPI017 | p95 Latency | minutes | 95th percentile latency | p95(latency) | V2-P14 |
| V2KPI018 | Open Incidents | count | Incidents still open | count(open) | V2-P21 |

---

## 4) KPI microcopy guidelines (premium polish)
- Always include **unit** in tooltip or label.
- Use “vs prev close” explicitly for deltas.
- Use “rolling(N)” in small text for rolling KPIs.
- Avoid ambiguous terms (“volatility high”); show the value and threshold.

---

## 5) Ownership and governance
- KPI owner: **Reena**
- Any threshold change must be logged in:
  - `docs/dashboards/V2/pages/page_22_release_notes_and_versions.md`