from __future__ import annotations

"""Caching layer for market data providers.

Goals
-----
1) First run can pull **real market data** (when network is available).
2) Subsequent runs are **reproducible** and **fast**.
3) The cache is explicit and inspectable (parquet + metadata JSON).

Design
------
We cache *raw provider outputs* keyed by:

    provider + symbol + request window + interval

The build scripts then transform that cached data into V1/V2 datasets.
"""

import hashlib
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

from ..io import safe_read_parquet, safe_to_parquet
from ...utils import ensure_dir, write_json
from .base import MarketDataProvider, ProviderError, standardise_ohlcv_frame, validate_ohlcv_frame


def _safe_token(s: str) -> str:
    """Make strings filesystem-friendly."""

    return (
        s.replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("^", "caret_")
        .replace(" ", "_")
    )


def _fingerprint_df(df: pd.DataFrame) -> str:
    """Deterministic content fingerprint (CSV hash)."""

    payload = df.to_csv(index=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class CacheConfig:
    base_dir: Path
    force_refresh: bool = False


class CachedProvider:
    """Wrap a provider with an on-disk cache."""

    def __init__(self, provider: MarketDataProvider, config: CacheConfig) -> None:
        self.provider = provider
        self.config = config
        ensure_dir(self.config.base_dir)

    @property
    def name(self) -> str:
        return self.provider.name

    # --------------------------
    # Intraday
    # --------------------------
    def fetch_intraday(self, symbol: str, start: datetime, end: datetime, interval: str = "1m") -> pd.DataFrame:
        start_utc = pd.Timestamp(start).tz_convert("UTC") if pd.Timestamp(start).tzinfo else pd.Timestamp(start, tz="UTC")
        end_utc = pd.Timestamp(end).tz_convert("UTC") if pd.Timestamp(end).tzinfo else pd.Timestamp(end, tz="UTC")

        path = self._intraday_path(symbol, start_utc, end_utc, interval)
        meta_path = path.with_suffix(".meta.json")

        if (path.exists() or path.with_suffix(".csv").exists()) and meta_path.exists() and not self.config.force_refresh:
            return safe_read_parquet(path)

        df = self.provider.fetch_intraday(symbol=symbol, start=start_utc.to_pydatetime(), end=end_utc.to_pydatetime(), interval=interval)
        df = standardise_ohlcv_frame(df)
        validate_ohlcv_frame(df)

        ensure_dir(path.parent)
        written = safe_to_parquet(df, path, index=False)

        meta = {
            "provider": self.provider.name,
            "symbol": symbol,
            "kind": "intraday",
            "interval": interval,
            "start_utc": str(start_utc),
            "end_utc": str(end_utc),
            "rows": int(df.shape[0]),
            "columns": list(df.columns),
            "fingerprint_sha256": _fingerprint_df(df),
            "cached_path": str(written),
        }
        write_json(meta_path, meta)
        return df

    # --------------------------
    # Daily
    # --------------------------
    def fetch_daily(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        path = self._daily_path(symbol, start, end)
        meta_path = path.with_suffix(".meta.json")

        if (path.exists() or path.with_suffix(".csv").exists()) and meta_path.exists() and not self.config.force_refresh:
            return safe_read_parquet(path)

        df = self.provider.fetch_daily(symbol=symbol, start=start, end=end)
        df = standardise_ohlcv_frame(df)
        validate_ohlcv_frame(df)

        ensure_dir(path.parent)
        written = safe_to_parquet(df, path, index=False)
        meta = {
            "provider": self.provider.name,
            "symbol": symbol,
            "kind": "daily",
            "start": str(start),
            "end": str(end),
            "rows": int(df.shape[0]),
            "columns": list(df.columns),
            "fingerprint_sha256": _fingerprint_df(df),
            "cached_path": str(written),
        }
        write_json(meta_path, meta)
        return df

    # --------------------------
    # Paths
    # --------------------------
    def _intraday_path(self, symbol: str, start_utc: pd.Timestamp, end_utc: pd.Timestamp, interval: str) -> Path:
        sym = _safe_token(symbol)
        s = start_utc.strftime("%Y%m%dT%H%M%SZ")
        e = end_utc.strftime("%Y%m%dT%H%M%SZ")
        return self.config.base_dir / self.provider.name / sym / "intraday" / interval / f"{s}__{e}.parquet"

    def _daily_path(self, symbol: str, start: date, end: date) -> Path:
        sym = _safe_token(symbol)
        return self.config.base_dir / self.provider.name / sym / "daily" / f"{start}__{end}.parquet"
