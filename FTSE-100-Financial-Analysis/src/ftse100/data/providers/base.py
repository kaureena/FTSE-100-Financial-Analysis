from __future__ import annotations

"""Provider interface for pulling OHLCV market data.

Why this exists
--------------
The dissertation workflow (V1) is built around *real-time / intraday* FTSE 100
data pulled from online sources (Yahoo Finance is explicitly mentioned as the
data source in the write-up). The portfolio repo ships with offline snapshots
so it runs in any environment, but this module makes the project feel like a
real UK market analytics platform.

The contract
------------
All providers must return a DataFrame with the following columns:

    timestamp (timezone-aware), open, high, low, close, volume

The index is optional.

Timestamps should be timezone-aware. If the upstream source returns naive
timestamps, providers should localise them using the source timezone and
convert to UTC.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable, Optional

import pandas as pd


class ProviderError(RuntimeError):
    """Raised when a provider cannot fulfil a request."""


@dataclass(frozen=True)
class ProviderMeta:
    """Light metadata about a provider."""

    name: str
    requires_api_key: bool
    supports_intraday: bool
    supports_daily: bool
    notes: str = ""


class MarketDataProvider(ABC):
    """Abstract base class for market data providers."""

    name: str = "base"

    @property
    def meta(self) -> ProviderMeta:
        return ProviderMeta(
            name=self.name,
            requires_api_key=False,
            supports_intraday=True,
            supports_daily=True,
            notes="",
        )

    # --------------------------
    # Fetch methods
    # --------------------------
    def fetch_intraday(self, symbol: str, start: datetime, end: datetime, interval: str = "1m") -> pd.DataFrame:
        """Fetch intraday OHLCV bars.

        Parameters
        ----------
        symbol:
            Provider-specific symbol.
        start, end:
            Time window (timezone-aware recommended).
        interval:
            Provider-specific interval string.
        """
        raise NotImplementedError(f"{self.name} does not support intraday fetch")

    def fetch_daily(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        """Fetch daily OHLCV bars."""
        raise NotImplementedError(f"{self.name} does not support daily fetch")


# --------------------------
# Validation helpers
# --------------------------

REQUIRED_COLS = ["timestamp", "open", "high", "low", "close", "volume"]


def validate_ohlcv_frame(df: pd.DataFrame, *, allow_empty: bool = False) -> None:
    """Validate provider output conforms to the expected OHLCV contract."""

    if df is None:
        raise ProviderError("Provider returned None")

    if df.empty:
        if allow_empty:
            return
        raise ProviderError("Provider returned an empty dataframe")

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ProviderError(f"Provider output missing required columns: {missing}")

    ts = pd.to_datetime(df["timestamp"], errors="coerce")
    if ts.isna().any():
        raise ProviderError("Provider output contains non-parsable timestamps")

    if ts.dt.tz is None:
        raise ProviderError("Provider output timestamps must be timezone-aware")

    # Numeric checks (best-effort)
    for c in ["open", "high", "low", "close"]:
        if pd.to_numeric(df[c], errors="coerce").isna().all():
            raise ProviderError(f"Provider output column '{c}' is not numeric")

    # Volume can be missing or float depending on provider; enforce non-negative
    vol = pd.to_numeric(df["volume"], errors="coerce")
    if vol.isna().all():
        raise ProviderError("Provider output volume is not numeric")
    if (vol.fillna(0) < 0).any():
        raise ProviderError("Provider output contains negative volume")


def standardise_ohlcv_frame(df: pd.DataFrame, *, sort: bool = True) -> pd.DataFrame:
    """Coerce columns to canonical names + dtypes and (optionally) sort."""

    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True)
    for c in ["open", "high", "low", "close"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    out["volume"] = pd.to_numeric(out["volume"], errors="coerce").fillna(0).astype(int)

    out = out.dropna(subset=["open", "high", "low", "close"]).reset_index(drop=True)
    if sort:
        out = out.sort_values("timestamp").reset_index(drop=True)
    return out
