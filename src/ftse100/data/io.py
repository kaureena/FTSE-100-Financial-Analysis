from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import pandas as pd

from ..utils import ensure_dir, write_json
from .synthetic import DailyOHLCV, generate_intraday_1m


def safe_to_parquet(df: pd.DataFrame, path: Path, *, index: bool = False) -> Path:
    """Write parquet if possible; otherwise fall back to CSV.

    This makes the repo more robust in environments where `pyarrow` isn't
    available (e.g., quick portfolio previews).
    """

    try:
        df.to_parquet(path, index=index)
        return path
    except Exception as e:
        # Pandas raises ImportError when parquet engines are missing.
        csv_path = path.with_suffix(".csv")
        df.to_csv(csv_path, index=index)
        return csv_path


def safe_read_parquet(path: Path) -> pd.DataFrame:
    """Read parquet, falling back to CSV if needed."""

    try:
        return pd.read_parquet(path)
    except Exception:
        csv_path = path.with_suffix(".csv")
        if not csv_path.exists():
            raise
        return pd.read_csv(csv_path)


def save_intraday_snapshot_from_dataframe(
    df: pd.DataFrame,
    *,
    raw_csv_path: Path,
    clean_parquet_path: Path,
    metadata_path: Path,
    source: str,
    source_details: dict | None = None,
) -> pd.DataFrame:
    """Persist an intraday snapshot from an existing dataframe.

    This is used for *live provider pulls* (Yahoo/Stooq/etc.) where the dataframe
    is already produced by a connector.
    """

    ensure_dir(raw_csv_path.parent)
    ensure_dir(clean_parquet_path.parent)
    ensure_dir(metadata_path.parent)

    out = df.copy()
    out.to_csv(raw_csv_path, index=False)
    written_processed = safe_to_parquet(out, clean_parquet_path, index=False)

    meta = {
        "dataset": "ftse100_intraday_1m",
        "timezone": "Europe/London",
        "source": source,
        "source_details": source_details or {},
        "rows": int(out.shape[0]),
        "columns": list(out.columns),
        "processed_path": str(written_processed),
    }
    write_json(metadata_path, meta)
    return out


def save_intraday_snapshot(
    daily: DailyOHLCV,
    raw_csv_path: Path,
    clean_parquet_path: Path,
    metadata_path: Path,
    seed: int = 42,
) -> pd.DataFrame:
    df = generate_intraday_1m(daily=daily, seed=seed)

    ensure_dir(raw_csv_path.parent)
    ensure_dir(clean_parquet_path.parent)
    ensure_dir(metadata_path.parent)

    df.to_csv(raw_csv_path, index=False)
    written_processed = safe_to_parquet(df, clean_parquet_path, index=False)

    meta = {
        "dataset": "ftse100_intraday_1m",
        "date": daily.date,
        "timezone": "Europe/London",
        "source": "synthetic_bridge_constrained_to_daily_ohlc",
        "daily_ohlc": asdict(daily),
        "rows": int(df.shape[0]),
        "columns": list(df.columns),
        "processed_path": str(written_processed),
        "notes": "Snapshot dataset included for offline reproducibility. Live pull hooks can be added outside this sandbox.",
    }
    write_json(metadata_path, meta)

    return df


def read_intraday_clean(parquet_path: Path) -> pd.DataFrame:
    df = safe_read_parquet(parquet_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    for c in ["open", "high", "low", "close"]:
        df[c] = df[c].astype(float)
    df["volume"] = df["volume"].astype(int)
    return df.sort_values("timestamp").reset_index(drop=True)
