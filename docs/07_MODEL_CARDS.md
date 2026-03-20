# Model Cards (Portfolio)

This repo includes two modelling tracks:

- **V1:** dissertation-style short-horizon forecasting (ARIMA + LSTM)
- **V2:** monitoring + operationalisation of forecast KPIs (marts + drift proxy)

> Note: These models are included for learning/portfolio purposes and are **not** intended for trading deployment.

---

## Model Card — ARIMA (V1)

### Intended use
- 10-minute horizon baseline forecast of the FTSE index proxy series
- Demonstration of classical time-series modelling

### Inputs
- Intraday close series (1m bars) cleaned and normalised to Europe/London

### Outputs
- 10-minute ahead point forecast (and optional interval)

### Metrics
- Stored under `v1_dissertation_baseline/outputs/metrics/arima_metrics.json`
- Diagnostics summary in `arima_model_summary.txt`

### Limitations
- Intraday series may not be stationary; ARIMA can underperform in regime shifts
- Does not incorporate exogenous variables (macro, constituents news)

---

## Model Card — LSTM (V1)

### Intended use
- Short-horizon sequence model baseline (10 minutes)
- Demonstration of ML approach (training history, evaluation metrics)

### Inputs
- Feature window derived from intraday data (returns + moving averages)

### Outputs
- 10-minute ahead forecast

### Metrics
- `v1_dissertation_baseline/outputs/metrics/lstm_metrics.json`
- Training history: `lstm_training_history.csv`

### Limitations
- Can overfit in small datasets
- Requires careful scaling/regularisation for stability

---

## Monitoring (V2)

V2 tracks:
- RMSE/MAE over time (monitoring checkpoints)
- Return distribution drift proxy (last20 vs prev20)

Evidence:
- `v2_modernisation_realtime/data/mart/forecasting_metrics.*`
- `v2_modernisation_realtime/data/mart/model_monitoring.*`

---

## Modernisation roadmap (optional V2.3+)
- Add Prophet / ETS baselines for comparison (academic completeness)
- Add exogenous regressors (calendar effects, events overlay)
- Add champion/challenger model registry + scheduled evaluation

