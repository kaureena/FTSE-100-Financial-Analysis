# Assumptions Log

A curated list of key assumptions used throughout V1 and V2.

> Portfolio note: assumptions are explicit so reviewers can see what would be validated in a real delivery.

---

## Market / domain assumptions
1. **Primary session window:** 08:00–16:30 Europe/London represents the core LSE trading session.
2. **Index proxy:** the repo uses a FTSE 100 index proxy series (`^FTSE`) for intraday movement.
3. **Index weights snapshot:** constituent weights are treated as a frozen “as-of” snapshot (index membership changes are out-of-scope for V1).
4. **Sector mapping:** sector labels are approximations (ICB-style categories). Some companies could be classified differently by official vendors.

## Data assumptions
5. **Minute bars quality:** intraday OHLCV bars may include gaps; gaps are handled by DQ rules and documented in the DQ snapshot.
6. **Volume semantics:** volume is treated as an indicative series (provider-dependent); comparisons are mainly relative within the same session.
7. **Corporate actions:** corporate actions are not explicitly adjusted at the index level for V1 (handled implicitly by provider).

## Modelling assumptions
8. **Forecast horizon:** 10-minute forecasting is used to match dissertation-style “near-term” forecasting.
9. **ARIMA as baseline:** ARIMA is a baseline model; violations of stationarity are expected intraday.
10. **LSTM scale:** LSTM is kept lightweight and evaluated with simple metrics (MAE/RMSE), not for trading deployment.

## BI / dashboard assumptions
11. **Dashboard exports:** PNG exports are treated as evidence packs; interactive dashboards can be rebuilt from marts + theme.
12. **Power BI pages:** the Power BI export pack is a visual reference for layout/branding; it’s not tied to a distributed PBIX file.

## Monitoring assumptions (V2)
13. **Latency SLA:** latency metrics are illustrative; in production, SLAs would be tuned to the actual ingestion frequency and downstream consumers.
14. **Drift proxy:** drift is measured via simple return distribution shifts; in production, additional drift detectors would be added.

---

## Next validation steps (if productionised)
- Validate data licensing and vendor SLAs.
- Validate index constituent universe via an official vendor feed.
- Add a true event/calendar provider (economic calendar + earnings).
- Add benchmark comparisons (e.g., FTSE 250 / STOXX / S&P 500).
