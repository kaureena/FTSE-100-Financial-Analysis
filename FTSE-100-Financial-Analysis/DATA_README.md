# DATA_README — FTSE 100 Financial Analysis (V1 + V2)

This document explains **what data exists**, **what it represents**, and **how it is used** across:
- **V1 (Dissertation baseline)** — reproducible snapshot aligned to the MSc dissertation
- **V2 (Modernised platform)** — longer-horizon + operational dashboards with near real-time feel

> **Disclaimer:** This project is for analytics and educational purposes. It is **not financial advice**.

---

## 1) V1 dataset (Dissertation baseline)

### 1.1 Purpose (V1)
V1 is designed to reproduce the dissertation’s core workflow:
- Real-time-style visualisation (line, candlestick, moving average, volume)
- Short-horizon forecasting using **ARIMA** and **LSTM**
- Evaluation using **MAE** and **RMSE**
- A trust layer (DQ snapshot) before interpreting model outputs

### 1.2 Data source
- Primary source: **Yahoo Finance** (retrieved via Python tooling)
- Dataset type: **secondary data** (no primary data collection)
- Granularity: **minute-by-minute bars**
- Dissertation baseline usage: **effectively one trading day** of minute bars (V1 snapshot)

### 1.3 Expected fields (OHLCV)
V1 intraday bars follow a standard OHLCV schema:
- `timestamp` (UTC or Europe/London depending on provider; display is always Europe/London)
- `open`, `high`, `low`, `close` (index level in **points**)
- `volume` (provider-defined; treat as *proxy* for “market activity” at index level)

### 1.4 Known limitations (V1)
- Index “volume” may not equal summed constituent volume; treat it as a proxy.
- One-day intraday snapshots cannot support robust claims about long-term performance.
- Forecast horizon is short (e.g., 1–10 steps) and will be sensitive to noise/outliers.
- LSTM model training may vary by hardware and random seed; use fixed seeds for reproducibility.

---

## 2) V2 datasets (Modernised platform)

### 2.1 Purpose (V2)
V2 aims to make the project feel like a UK-market analytics platform:
- **Near real-time** intraday experience (or replay fallback)
- Multi-session/daily datasets suitable for **regime analysis**, **risk**, **backtesting**
- Operational credibility: **freshness, DQ, pipeline health, SLA, incidents**
- Governance: KPI dictionary, measure catalogue, lineage, versioning

### 2.2 Target coverage
V2 targets two complementary time horizons:

1) **Daily close (multi-year)**
- Used for: drawdown/risk, volatility regimes (daily), correlation, backtesting baselines
- Typical coverage goal: 3–10 years (depending on availability)

2) **Intraday (recent window)**
- Used for: intraday terminal, near real-time feel, short-horizon forecasting cockpit
- Typical coverage goal: last 30–90 trading sessions (provider limits may apply)

### 2.3 Dataset layers (medallion style)
V2 uses a layered structure (conceptual; implementation may vary):
- **raw**: provider snapshots as-ingested
- **staged**: cleaned + timezone normalised + deduplicated
- **curated**: derived features (returns, vol, indicators)
- **marts**: dashboard-ready tables (`mart.*`)

---

## 3) Time handling (UK authenticity)

### 3.1 Display timezone
- All dashboard timestamps are displayed in **Europe/London**.

### 3.2 DST (BST/GMT) edge cases
- When clocks change, local times can be duplicated or skipped.
- Store timestamps in UTC where possible; convert to London for display.
- DQ checks must explicitly handle DST boundaries.

---

## 4) Data Quality (DQ) rules (minimum standard)
All pages must pass (or explicitly banner) the following checks:

- **No duplicates** at the primary key grain (timestamp × instrument × interval)
- **Continuity checks** for intraday expected intervals during session
- **OHLC sanity**
  - `high >= max(open, close)`
  - `low <= min(open, close)`
  - `volume >= 0`
- **Outlier flags** for returns/volume spikes (not auto-deleted; flagged)

---

## 5) Where data lives in the repo
This starter pack is documentation-only. In the full repo, data typically lives under:
- `data/raw/`
- `data/staged/`
- `data/curated/`
- `data/marts/`

Contracts for these datasets are defined in: `DATA_CONTRACTS.md`

---

## Reference data (UK terminal realism)

In addition to the time-series tables, the repo ships small reference datasets:

- `data/reference/ftse100_constituents_universe_snapshot.csv`
- `data/reference/uk_macro_calendar_stub.csv`
- `data/reference/ftse100_earnings_calendar_stub_top25.csv`
- `data/reference/market_news_headlines_stub.csv`

V2 assembles these into the unified gold table:

- `v2_modernisation_realtime/data/gold/events_calendar.(parquet|csv)`

See: `REFERENCE_DATA.md`
