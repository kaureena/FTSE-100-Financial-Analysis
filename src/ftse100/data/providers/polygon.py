from __future__ import annotations

"""Polygon.io provider (API key required).

Polygon provides a clean aggregates API for minute/day bars.

Important
---------
Polygon tickers vary by asset class. For indices you may need an index symbol or
an ETF proxy depending on your subscription.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

import pandas as pd
import requests

from .base import MarketDataProvider, ProviderError, ProviderMeta


@dataclass
class PolygonProvider(MarketDataProvider):
    api_key: str
    session: Optional[requests.Session] = None

    name: str = "polygon"

    @property
    def meta(self) -> ProviderMeta:
        return ProviderMeta(
            name=self.name,
            requires_api_key=True,
            supports_intraday=True,
            supports_daily=True,
            notes="Requires API key/subscription; tickers differ for indices vs equities.",
        )

    def fetch_intraday(self, symbol: str, start: datetime, end: datetime, interval: str = "1m") -> pd.DataFrame:
        # Polygon interval format: range/1/minute
        if interval not in {"1m", "1min", "minute"}:
            raise ProviderError("PolygonProvider currently supports 1-minute intraday only")

        sess = self.session or requests.Session()
        start_date = pd.Timestamp(start).date()
        end_date = pd.Timestamp(end).date()

        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/minute/{start_date}/{end_date}"
        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": 50000,
            "apiKey": self.api_key,
        }
        r = sess.get(url, params=params, timeout=30)
        if r.status_code != 200:
            raise ProviderError(f"Polygon request failed: HTTP {r.status_code} {r.text[:200]}")
        payload = r.json()
        results = payload.get("results")
        if not results:
            raise ProviderError("Polygon returned no results")

        df = pd.DataFrame(results)
        # polygon keys: t (ms), o,h,l,c,v
        df = df.rename(columns={"t": "timestamp", "o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"})
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)

        start_utc = pd.Timestamp(start).tz_convert("UTC") if pd.Timestamp(start).tzinfo else pd.Timestamp(start, tz="UTC")
        end_utc = pd.Timestamp(end).tz_convert("UTC") if pd.Timestamp(end).tzinfo else pd.Timestamp(end, tz="UTC")
        df = df[(df["timestamp"] >= start_utc) & (df["timestamp"] <= end_utc)].reset_index(drop=True)
        if df.empty:
            raise ProviderError("Polygon returned no rows in requested time window")
        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    def fetch_daily(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        sess = self.session or requests.Session()
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start}/{end}"
        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": 50000,
            "apiKey": self.api_key,
        }
        r = sess.get(url, params=params, timeout=30)
        if r.status_code != 200:
            raise ProviderError(f"Polygon request failed: HTTP {r.status_code} {r.text[:200]}")
        payload = r.json()
        results = payload.get("results")
        if not results:
            raise ProviderError("Polygon returned no results")
        df = pd.DataFrame(results)
        df = df.rename(columns={"t": "timestamp", "o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"})
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        return df[["timestamp", "open", "high", "low", "close", "volume"]]
