# METRICS_LIBRARY — Forecast, Drift, DQ & Ops Metrics

This library defines **standard metrics** used across:
- forecasting evaluation (V1 + V2)
- monitoring and drift detection (V2)
- pipeline operations (V2)
- data quality scoring (V1 + V2)

> Keep metric names stable; changing formulas is a breaking change.

---

<a id="forecast-metrics"></a>
## 1) Forecast accuracy metrics

### 1.1 MAE — Mean Absolute Error
- **Meaning:** typical absolute error size
- **Formula:**
  ```text
  MAE = mean(|y - yhat|)
  ```
- **Units:** same as target (FTSE points)
- **Interpretation:** lower is better; less sensitive to large spikes than RMSE

### 1.2 MSE — Mean Squared Error
- **Formula:**
  ```text
  MSE = mean((y - yhat)^2)
  ```
- **Interpretation:** penalises large errors; useful during volatility spikes

### 1.3 RMSE — Root Mean Squared Error
- **Formula:**
  ```text
  RMSE = sqrt(mean((y - yhat)^2))
  ```
- **Interpretation:** “big miss” sensitivity; lower is better

### 1.4 Rolling metrics
Compute metrics over a rolling window to detect drift:
```text
RMSE_roll(t) = RMSE over [t-W+1 .. t]
```

---

## 2) Forecast uncertainty / coverage (optional)
If using forecast bands:
- **Coverage:** % of actual points inside the band
  ```text
  coverage = mean( lower <= y <= upper )
  ```

---

## 3) Drift & stability metrics (V2)

### 3.1 Error drift
- **Definition:** increase in rolling error vs baseline
  ```text
  drift = RMSE_roll - RMSE_baseline
  ```
- **Use:** triggers investigation/retraining

### 3.2 KS statistic (distribution shift proxy)
Compare distributions of returns:
- baseline window vs recent window
- large KS suggests shift in distribution

### 3.3 PSI (Population Stability Index) (optional)
Useful for binned features; indicates shift in feature distribution.

---

<a id="dq-metrics"></a>
## 4) Data Quality (DQ) metrics

### 4.1 DQ pass/fail gates
Hard failures:
- duplicate timestamps at grain
- OHLC sanity violations
- impossible negative volume

Warnings:
- missing bar gaps
- outliers beyond configured z-score threshold

### 4.2 DQ score (0–100)
Weighted pass rate:
```text
score = sum(weight_i * pass_i) / sum(weights) * 100
```

---

<a id="ops-metrics"></a>
## 5) Pipeline & operational metrics

### 5.1 Freshness (minutes)
```text
freshness_minutes = now_london - max(data_timestamp_london)
```

### 5.2 Latency components
Track latency per stage:
- ingestion lag
- transform lag
- model lag
- export lag

### 5.3 SLA pass rate
```text
sla_pass_rate = count(runs where freshness <= SLA) / total_runs
```

---

## 6) Metric QA checklist
- [ ] Units explicitly stated (points vs %)
- [ ] Calculation window specified (rolling size, horizon, etc.)
- [ ] Baseline selection documented (for drift)
- [ ] Outlier policy stated (exclude vs include vs winsorise)
- [ ] Reconciliation test exists (spot-check against raw)

---

## 7) Recommended metric reporting format
Every model run should output:
- run_id
- model_name
- train window
- test window
- horizon H
- MAE, RMSE (+ optional coverage)
- notes (regime, anomalies, DQ status)