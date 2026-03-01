# FEATURE ENGINEERING LOG — V1

This log lists features created for V1 and why they exist.

## Features (intraday, 1-minute)
### 1) Returns
- `return_simple`: (close_t / close_{t-1}) - 1
- Purpose: modelling baseline; risk metrics; drift proxies

### 2) Moving average
- `ma20`: mean(close_{t-19..t})
- `ma_gap`: close - ma20
- `crossover_flag`: close crosses ma20
- Purpose: dissertation-aligned visualisation + additional context for forecasts

### 3) Volatility proxies
- `realised_vol_20`: std(returns window) * sqrt(20)
- Purpose: regime and error interpretation

### 4) Volume signals
- `volume_spike_flag`: volume >= p95(volume)
- Purpose: contextualise candle moves and forecast errors

## Output artefacts
- `v1_dissertation_baseline/outputs/tables/moving_average_features.*`
- `v1_dissertation_baseline/outputs/metrics/volume_spike_flags.csv`
