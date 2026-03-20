from __future__ import annotations

"""Yahoo Finance provider.

Implementation note
-------------------
We use the public `chart` endpoint used by the Yahoo Finance web UI. This keeps
the repo lightweight (no mandatory `yfinance` dependency).

Limitations
-----------
- Yahoo often restricts 1-minute historical bars to a recent window.
- Unofficial API (may change).
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, Optional

import pandas as pd
import requests

from .base import MarketDataProvider, ProviderError, ProviderMeta


@dataclass
class YahooFinanceProvider(MarketDataProvider):
    """Yahoo Finance provider using the v8 chart endpoint."""

    session: Optional[requests.Session] = None

    name: str = "yahoo"

    @property
    def meta(self) -> ProviderMeta:
        return ProviderMeta(
            name=self.name,
            requires_api_key=False,
            supports_intraday=True,
            supports_daily=True,
            notes="Unofficial chart endpoint; 1m history may be limited.",
        )

    def fetch_intraday(self, symbol: str, start: datetime, end: datetime, interval: str = "1m") -> pd.DataFrame:
        return self._fetch_chart(symbol=symbol, start=start, end=end, interval=interval)

    def fetch_daily(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        start_dt = pd.Timestamp(start).tz_localize("UTC")
        # include end date fully
        end_dt = (pd.Timestamp(end) + pd.Timedelta(days=1)).tz_localize("UTC")
        return self._fetch_chart(symbol=symbol, start=start_dt.to_pydatetime(), end=end_dt.to_pydatetime(), interval="1d")

    # --------------------------
    # Internals
    # --------------------------
    def _fetch_chart(self, symbol: str, start: datetime, end: datetime, interval: str) -> pd.DataFrame:
        sess = self.session or requests.Session()
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"

        start_utc = pd.Timestamp(start).tz_convert("UTC") if pd.Timestamp(start).tzinfo else pd.Timestamp(start, tz="UTC")
        end_utc = pd.Timestamp(end).tz_convert("UTC") if pd.Timestamp(end).tzinfo else pd.Timestamp(end, tz="UTC")

        params = {
            "period1": int(start_utc.timestamp()),
            "period2": int(end_utc.timestamp()),
            "interval": interval,
            "includePrePost": "false",
            "events": "div|split",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (FTSE-100-Financial-Analysis; +https://github.com/)"
        }

        r = sess.get(url, params=params, headers=headers, timeout=30)
        if r.status_code != 200:
            raise ProviderError(f"Yahoo request failed: HTTP {r.status_code} {r.text[:200]}")

        payload = r.json()
        try:
            result = payload["chart"]["result"][0]
        except Exception as e:
            raise ProviderError(f"Yahoo response did not contain chart result: {payload.get('chart', {}).get('error')}") from e

        ts = result.get("timestamp") or []
        if not ts:
            # Common failure mode if Yahoo refuses the range.
            raise ProviderError("Yahoo returned no timestamps (range may be unsupported for requested interval)")

        quote = (result.get("indicators", {}).get("quote") or [{}])[0]

        df = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(ts, unit="s", utc=True),
                "open": quote.get("open"),
                "high": quote.get("high"),
                "low": quote.get("low"),
                "close": quote.get("close"),
                "volume": quote.get("volume"),
            }
        )

        # Drop rows where OHLC is missing
        df = df.dropna(subset=["open", "high", "low", "close"]).reset_index(drop=True)
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0)
        return df
