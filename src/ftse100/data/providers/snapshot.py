from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from ftse100.config import DEFAULT_TIMEZONE, V1_DATA_RAW_DIR
from .base import MarketDataProvider, ProviderMeta


class SnapshotProvider(MarketDataProvider):
    """Offline provider that serves repo-shipped snapshots.

    This provider makes the portfolio reproducible without external APIs.
    """

    def __init__(self, *, raw_csv: Optional[Path] = None):
        self.raw_csv = raw_csv or (V1_DATA_RAW_DIR / "ftse100_intraday_1m_raw.csv")

    @property
    def meta(self) -> ProviderMeta:
        return ProviderMeta(
            name="snapshot",
            display_name="Repo Snapshot (Offline)",
            requires_api_key=False,
            supports_intraday=True,
            supports_daily=False,
            notes=f"Reads {self.raw_csv} (Europe/London timestamps, converted to UTC).",
        )

    def fetch_intraday(self, symbol: str, start: datetime, end: datetime, interval: str = "1m") -> pd.DataFrame:
        df = pd.read_csv(self.raw_csv)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        # Localise to London time then convert to UTC, to match other providers.
        df["timestamp"] = df["timestamp"].dt.tz_localize(DEFAULT_TIMEZONE).dt.tz_convert("UTC")
        df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
        mask = (df["timestamp"] >= pd.to_datetime(start).tz_convert("UTC")) & (df["timestamp"] <= pd.to_datetime(end).tz_convert("UTC"))
        df = df.loc[mask].reset_index(drop=True)

        keep = [c for c in ["timestamp", "open", "high", "low", "close", "volume"] if c in df.columns]
        return df[keep]
