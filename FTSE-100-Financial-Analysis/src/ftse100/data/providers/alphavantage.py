from __future__ import annotations

"""Alpha Vantage provider (API key required).

Alpha Vantage is convenient for:
- intraday bars when supported for the chosen symbol
- daily OHLCV history

Notes
-----
- Strict rate limits on free tiers.
- Timezone is provided in metadata; we convert to UTC.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, Optional

import pandas as pd
import requests

from .base import MarketDataProvider, ProviderError, ProviderMeta


_TZ_MAP = {
    "US/Eastern": "America/New_York",
    "UTC": "UTC",
    "Europe/London": "Europe/London",
}


@dataclass
class AlphaVantageProvider(MarketDataProvider):
    api_key: str
    session: Optional[requests.Session] = None

    name: str = "alphavantage"

    @property
    def meta(self) -> ProviderMeta:
        return ProviderMeta(
            name=self.name,
            requires_api_key=True,
            supports_intraday=True,
            supports_daily=True,
            notes="Requires API key; free tier has tight limits.",
        )

    def fetch_intraday(self, symbol: str, start: datetime, end: datetime, interval: str = "1min") -> pd.DataFrame:
        sess = self.session or requests.Session()
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "outputsize": "full",
            "apikey": self.api_key,
        }
        r = sess.get(url, params=params, timeout=30)
        if r.status_code != 200:
            raise ProviderError(f"Alpha Vantage request failed: HTTP {r.status_code} {r.text[:200]}")
        payload = r.json()
        if "Error Message" in payload:
            raise ProviderError(payload["Error Message"])
        if "Note" in payload:
            raise ProviderError(f"Alpha Vantage throttled: {payload['Note']}")

        meta = payload.get("Meta Data", {})
        tz_name = _TZ_MAP.get(meta.get("6. Time Zone", "UTC"), "UTC")

        series_key = f"Time Series ({interval})"
        series = payload.get(series_key)
        if not series:
            raise ProviderError(f"Alpha Vantage response missing '{series_key}'")

        rows = []
        for ts, values in series.items():
            rows.append(
                {
                    "timestamp": ts,
                    "open": float(values.get("1. open")),
                    "high": float(values.get("2. high")),
                    "low": float(values.get("3. low")),
                    "close": float(values.get("4. close")),
                    "volume": float(values.get("5. volume", 0)),
                }
            )
        df = pd.DataFrame(rows)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"]).reset_index(drop=True)
        df["timestamp"] = df["timestamp"].dt.tz_localize(tz_name, ambiguous="infer", nonexistent="shift_forward").dt.tz_convert("UTC")

        start_utc = pd.Timestamp(start).tz_convert("UTC") if pd.Timestamp(start).tzinfo else pd.Timestamp(start, tz="UTC")
        end_utc = pd.Timestamp(end).tz_convert("UTC") if pd.Timestamp(end).tzinfo else pd.Timestamp(end, tz="UTC")
        df = df[(df["timestamp"] >= start_utc) & (df["timestamp"] <= end_utc)].reset_index(drop=True)
        if df.empty:
            raise ProviderError("Alpha Vantage returned no rows in requested time window")
        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    def fetch_daily(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        sess = self.session or requests.Session()
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "full",
            "apikey": self.api_key,
        }
        r = sess.get(url, params=params, timeout=30)
        if r.status_code != 200:
            raise ProviderError(f"Alpha Vantage request failed: HTTP {r.status_code} {r.text[:200]}")
        payload = r.json()
        if "Error Message" in payload:
            raise ProviderError(payload["Error Message"])
        if "Note" in payload:
            raise ProviderError(f"Alpha Vantage throttled: {payload['Note']}")

        series = payload.get("Time Series (Daily)")
        if not series:
            raise ProviderError("Alpha Vantage response missing 'Time Series (Daily)'")

        rows = []
        for d, values in series.items():
            rows.append(
                {
                    "timestamp": d,
                    "open": float(values.get("1. open")),
                    "high": float(values.get("2. high")),
                    "low": float(values.get("3. low")),
                    "close": float(values.get("4. close")),
                    "volume": float(values.get("5. volume", 0)),
                }
            )
        df = pd.DataFrame(rows)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
        df = df.dropna(subset=["timestamp"]).reset_index(drop=True)
        mask = (df["timestamp"].dt.date >= start) & (df["timestamp"].dt.date <= end)
        df = df.loc[mask, ["timestamp", "open", "high", "low", "close", "volume"]].reset_index(drop=True)
        if df.empty:
            raise ProviderError("Alpha Vantage returned no rows in requested date range")
        return df
