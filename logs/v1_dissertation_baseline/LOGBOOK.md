# LOGBOOK — V1 Dissertation Baseline

Timezone: Europe/London  
Objective: Provide a reproducible baseline aligned to the dissertation:
- minute-by-minute intraday data
- visualisation (line/candles/volume/MA)
- ARIMA baseline forecast + LSTM forecast
- MAE/RMSE evaluation + comparison
- 7 dashboard exports

---

## Run philosophy
V1 is a **snapshot-first reproducible build**:
- Keep the dataset stable for reviewers.
- Prefer clarity and traceability over “live” integration complexity.

---

## Key implementation notes
- Data:
  - raw snapshot is preserved; processed version is used for analytics.
- DQ:
  - gaps, duplicates, OHLC sanity checks are run before modelling.
- Models:
  - ARIMA acts as a statistical baseline (fast, interpretable).
  - LSTM acts as non-linear benchmark (sequence modelling).
- Evaluation:
  - MAE = typical error; RMSE = big-miss penalty.

---

## 2026-02-08 — Baseline hardening
Added intermediate artefacts:
- MA feature table and crossover markers
- volume spike flags
- gap report + dq snapshot json

Evidence paths:
- `v1_dissertation_baseline/outputs/tables/*`
- `v1_dissertation_baseline/outputs/metrics/*`

---

## 2026-02-05 — Delivery
Produced:
- V1 exports (7 pages) and metrics summary
Evidence paths:
- `docs/dashboards/V1/exports/*`
- `v1_dissertation_baseline/outputs/metrics/*`
