# Live Data Providers & Caching (Optional)

This repo ships **offline snapshots** so the dashboards and notebooks run anywhere.
However, the original Master’s dissertation workflow is explicitly grounded in pulling
FTSE100 data from **Yahoo Finance** and visualising it in near real-time.

To make the repo feel like a **real UK market analytics platform**, we include
pluggable providers + an on-disk cache.

> **Not financial advice.**

---

## 1) Quick start (live pull → cached → reproducible)

### V1 (single-session intraday, dissertation baseline)

```bash
python scripts/v1_build_all.py \
  --data-source yahoo \
  --symbol "^FTSE" \
  --date 2026-02-13 \
  --cache-dir ./data_cache
```

If you run it again with the same parameters, it will reuse the cached parquet.

### V2 (platform build; optionally anchor synthetic intraday to real daily prints)

```bash
python scripts/v2_build_all.py \
  --data-source stooq \
  --symbol "^UKX" \
  --start-date 2025-11-03 \
  --end-date 2026-02-13 \
  --cache-dir ./data_cache
```

---

## 2) Provider matrix

| Provider | API key | Intraday | Daily | Best for |
|---|---:|---:|---:|---|
| **Yahoo** | No | ✅ (often limited history) | ✅ | Dissertation-style intraday pulls & quick charts |
| **Stooq** | No | ❌ | ✅ | Daily history (free) and anchoring synthetic intraday |
| **Alpha Vantage** | Yes | ✅ | ✅ | Alternative intraday/daily (rate-limited) |
| **Polygon.io** | Yes | ✅ | ✅ | Professional-grade aggregates (subscription dependent) |

---

## 3) Symbols (important)

Symbols vary between providers.

Defaults used in this repo:
- Yahoo FTSE 100 index: `^FTSE`
- Stooq UKX/FTSE 100: `^UKX` (often case-insensitive in the URL)

If a provider does not support indices on your plan, use a proxy instrument:
- An FTSE100 ETF ticker (e.g., `ISF.L`) or futures/CFD symbol supported by your provider.

---

## 4) Cache layout

The cache stores:
- `*.parquet` (raw provider output standardised to our OHLCV schema)
- `*.meta.json` (symbol, window, rows, fingerprint hash)

Example:

```
data_cache/
  yahoo/
    caret__FTSE/
      intraday/1m/
        20260213T080000Z__20260213T163000Z.parquet
        20260213T080000Z__20260213T163000Z.meta.json
```

---

## 5) Environment variables

You can drive provider selection via CLI flags (recommended) or environment.
See `.env.example`.

Keys:
- `FTSE100_PROVIDER`
- `FTSE100_SYMBOL`
- `FTSE100_CACHE_DIR`
- `ALPHAVANTAGE_API_KEY`
- `POLYGON_API_KEY`

---

## 6) Limitations & realism notes

1) **Yahoo intraday limits:** 1-minute bars may be restricted to a recent window.
2) **Rate limits:** Alpha Vantage free tier throttles heavily.
3) **V2 realism:** When only daily data is available, V2 can generate *intraday-looking*
   minute bars constrained to real daily OHLCV. This preserves realistic daily levels
   while keeping the build reproducible.

---

## Reference datasets (universe + events)

To make the project feel like a **UK market terminal**, V2 uses small offline reference datasets
under `data/reference/`:

- `ftse100_constituents_universe_snapshot.csv` — tickers + sectors + weights (portfolio heuristic)
- `uk_macro_calendar_stub.csv` — macro releases / central bank decisions (stub)
- `ftse100_earnings_calendar_stub_top25.csv` — earnings dates for top names (stub)
- `market_news_headlines_stub.csv` — optional headline feed (stub)

These are loaded via `src/ftse100/reference/*` and assembled into:

- `v2_modernisation_realtime/data/gold/events_calendar.(parquet|csv)`

If you want to refresh the constituents list from Wikipedia (best-effort), run:

```bash
python scripts/v2_build_all.py --constituents-source wikipedia --weights-method equal
```

See also: `REFERENCE_DATA.md`
