# INTERPRETABILITY LOG — V1 (LSTM SHAP Surrogate)

## Problem statement
Direct SHAP explanations do not natively support a 3D LSTM input tensor:
- (batch, timesteps, features)

## Approach used (surrogate)
1) Reshape 3D sequences into 2D feature vectors:
   - combine timesteps and features into a single dimension
2) Train a lightweight Dense surrogate model to approximate LSTM outputs
3) Apply SHAP to the Dense surrogate

## What this provides
- A **proxy** importance ranking indicating which timesteps/features influenced the prediction most.

## Limitations (be explicit)
- Surrogate ≠ original LSTM:
  - explanations are approximate
  - temporal dynamics are compressed
- Use explanations for transparency and narrative, not as causal proof.

## Evidence paths
- `v1_dissertation_baseline/outputs/metrics/shap_proxy.csv` (if enabled)
- `docs/dashboards/V1/exports/v1_page_05_lstm_forecast.png` (interpretability panel area)
