from __future__ import annotations

"""Stooq provider.

Stooq provides free daily OHLCV CSV downloads. It is useful for:
- backfilling daily history
- anchoring synthetic intraday generation to *real* daily prints

Stooq does **not** reliably provide 1-minute intraday for indices, so intraday
fetch is intentionally not implemented.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

import pandas as pd
import requests

from .base import MarketDataProvider, ProviderError, ProviderMeta


@dataclass
class StooqProvider(MarketDataProvider):
    session: Optional[requests.Session] = None

    name: str = "stooq"

    @property
    def meta(self) -> ProviderMeta:
        return ProviderMeta(
            name=self.name,
            requires_api_key=False,
            supports_intraday=False,
            supports_daily=True,
            notes="Daily CSV only (intraday not supported for this repo).",
        )

    def fetch_daily(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        sess = self.session or requests.Session()

        # Stooq endpoint: daily CSV, includes full history; we filter.
        url = f"https://stooq.com/q/d/l/?s={symbol.lower()}&i=d"
        r = sess.get(url, timeout=30)
        if r.status_code != 200:
            raise ProviderError(f"Stooq request failed: HTTP {r.status_code} {r.text[:200]}")

        from io import StringIO

        df = pd.read_csv(StringIO(r.text))
        if df.empty:
            raise ProviderError("Stooq returned empty CSV")

        # Expected columns: Date, Open, High, Low, Close, Volume
        cols = {c.lower(): c for c in df.columns}
        for need in ["date", "open", "high", "low", "close", "volume"]:
            if need not in cols:
                raise ProviderError(f"Stooq CSV missing column '{need}'")

        df = df.rename(columns={cols["date"]: "date", cols["open"]: "open", cols["high"]: "high", cols["low"]: "low", cols["close"]: "close", cols["volume"]: "volume"})
        df["timestamp"] = pd.to_datetime(df["date"], errors="coerce", utc=True)

        df = df.dropna(subset=["timestamp"]).reset_index(drop=True)
        mask = (df["timestamp"].dt.date >= start) & (df["timestamp"].dt.date <= end)
        df = df.loc[mask, ["timestamp", "open", "high", "low", "close", "volume"]].reset_index(drop=True)
        if df.empty:
            raise ProviderError("Stooq returned no rows in requested date range")
        return df
