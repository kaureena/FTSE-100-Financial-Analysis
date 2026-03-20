# V1 Dashboard Gallery — Dissertation Baseline (Reproducible)

V1 is the **dissertation-aligned baseline**: a clean, reproducible pack that focuses on:
- Real-time-style FTSE100 visualisation (intraday minute bars)
- Line chart + candlestick + moving average + volume
- Short-horizon forecasting with **ARIMA** and **LSTM**
- Quantitative evaluation using **MAE / RMSE**
- A minimum governance layer (DQ snapshot + export evidence)

> Goal: demonstrate that the work is academically grounded and technically reproducible.

---

## Folder layout

- Specs: `docs/dashboards/V1/pages/*.md`
- Exports: `docs/dashboards/V1/exports/*.png`

---

## Naming convention (do not change)

`v1_page_{NN}_{slug}.png`

Rules:
- `{NN}` = `01..07`
- `{slug}` lowercase and underscores only
- Names are stable (avoid breaking links)

---

## How to review V1 (recommended order)

1) **P01 → P03**: Understand market behaviour (trend → candles/volume → MA structure)  
2) **P07**: Confirm data quality (trust gate)  
3) **P04 → P06**: Review forecasts and compare models (ARIMA vs LSTM)

---

## Pages

| Page ID | Title | What it answers | Spec | Export |
|---|---|---|---|---|
| **V1-P01** | Market Overview (Intraday) | Session direction, volatility, range | [Spec](pages/page_01_market_overview.md) | [PNG](exports/v1_page_01_market_overview.png) |
| **V1-P02** | Candlestick + Volume | Microstructure patterns + volume confirmation | [Spec](pages/page_02_candles_volume.md) | [PNG](exports/v1_page_02_candles_volume.png) |
| **V1-P03** | Moving Averages & Trend | Trend smoothing, crossovers, lag | [Spec](pages/page_03_moving_averages.md) | [PNG](exports/v1_page_03_moving_averages.png) |
| **V1-P04** | ARIMA Forecast (Short Horizon) | ARIMA vs actual, residual diagnostics | [Spec](pages/page_04_arima_forecast.md) | [PNG](exports/v1_page_04_arima_forecast.png) |
| **V1-P05** | LSTM Forecast (Short Horizon) | LSTM vs actual, rolling error stability | [Spec](pages/page_05_lstm_forecast.md) | [PNG](exports/v1_page_05_lstm_forecast.png) |
| **V1-P06** | Model Comparison & Metrics | Winner summary using MAE/RMSE by horizon | [Spec](pages/page_06_model_comparison.md) | [PNG](exports/v1_page_06_model_comparison.png) |
| **V1-P07** | Data Quality Snapshot | Missing bars, duplicates, OHLC sanity | [Spec](pages/page_07_data_quality_snapshot.md) | [PNG](exports/v1_page_07_data_quality_snapshot.png) |

---

## Export standards (V1)

- Minimum: **2560×1440**
- Preferred: **3840×2160 (4K)**
- Every export must include footer:
  - `run_id`
  - London timestamp (**Europe/London**)
  - freshness note (“snapshot / replay”)
  - “Not financial advice”

---

## Documentation links (source of truth)

- Theme: `assets/branding/REPO_THEME_GUIDE.md`
- KPI definitions: `KPI_CATALOGUE.md`
- Data contracts: `DATA_CONTRACTS.md`
- Metrics: `METRICS_LIBRARY.md`
- Export runbook: `DASHBOARD_EXPORT_RUNBOOK.md`
