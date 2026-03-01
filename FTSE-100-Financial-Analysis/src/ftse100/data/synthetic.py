from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DailyOHLCV:
    date: str  # YYYY-MM-DD (London local)
    open: float
    high: float
    low: float
    close: float
    volume: int


def _london_minutes(date: str, start_time: str = "08:00", end_time: str = "16:30") -> pd.DatetimeIndex:
    start = pd.Timestamp(f"{date} {start_time}")
    end = pd.Timestamp(f"{date} {end_time}")
    # inclusive so the close print is included
    return pd.date_range(start=start, end=end, freq="1min")


def brownian_bridge_path(n: int, start: float, end: float, sigma: float, seed: int = 42) -> np.ndarray:
    """Generate a Brownian bridge path of length n (including endpoints)."""
    rng = np.random.default_rng(seed)
    inc = rng.normal(0.0, sigma, size=n - 1)
    w = np.concatenate([[0.0], np.cumsum(inc)])
    t = np.linspace(0.0, 1.0, n)
    bridge = w - t * w[-1]
    return start + t * (end - start) + bridge


def _scale_to_bounds(path: np.ndarray, low: float, high: float, start: float, end: float) -> np.ndarray:
    """Scale the deviation component to keep endpoints fixed and fit within [low, high]."""
    n = len(path)
    t = np.linspace(0.0, 1.0, n)
    base = start + t * (end - start)
    dev = path - base

    if path.min() >= low and path.max() <= high:
        return path

    k_max = 1.0
    eps = 1e-12
    for b, d in zip(base, dev):
        if abs(d) < eps:
            continue
        if d > 0:
            k_max = min(k_max, (high - b) / d)
        else:
            k_max = min(k_max, (b - low) / (-d))
    k_max = max(0.0, k_max)
    return base + k_max * dev


def generate_intraday_1m(
    daily: DailyOHLCV,
    start_time: str = "08:00",
    end_time: str = "16:30",
    seed: int = 42,
    sigma: float = 0.6,
    wick_sigma: float = 0.15,
) -> pd.DataFrame:
    """Generate a realistic-looking intraday 1-minute OHLCV dataset.

    - Constrained to match daily open/close and stay inside daily low/high
    - Minute bars have small wicks
    - Volume follows a U-shape and sums to the daily volume
    """
    idx = _london_minutes(daily.date, start_time, end_time)
    n = len(idx)

    close = brownian_bridge_path(n, daily.open, daily.close, sigma=sigma, seed=seed)
    close = _scale_to_bounds(close, low=daily.low, high=daily.high, start=daily.open, end=daily.close)

    open_ = np.concatenate([[daily.open], close[:-1]])

    rng = np.random.default_rng(seed + 1)
    wick = np.abs(rng.normal(0.0, wick_sigma, size=n))
    high = np.maximum(open_, close) + wick
    low = np.minimum(open_, close) - wick

    high = np.minimum(high, daily.high)
    low = np.maximum(low, daily.low)
    high = np.maximum(high, np.maximum(open_, close))
    low = np.minimum(low, np.minimum(open_, close))

    # Volume curve
    x = np.linspace(0.0, 1.0, n)
    weights = 1.0 + 3.0 * np.exp(-x * 10.0) + 3.0 * np.exp(-(1.0 - x) * 10.0)
    weights = weights / weights.sum()
    vol = np.floor(weights * daily.volume).astype(int)

    drift = int(daily.volume - vol.sum())
    if drift != 0:
        order = np.argsort(-weights)
        for i in order[: abs(drift)]:
            vol[i] += 1 if drift > 0 else -1

    df = pd.DataFrame(
        {
            "timestamp": idx,
            "open": np.round(open_, 2),
            "high": np.round(high, 2),
            "low": np.round(low, 2),
            "close": np.round(close, 2),
            "volume": vol,
        }
    )

    df["date"] = df["timestamp"].dt.date.astype(str)
    df["time"] = df["timestamp"].dt.time.astype(str)
    df["symbol"] = "FTSE100"  # semantic label used in docs

    return df


def generate_multi_session_intraday(start_date: str, end_date: str, seed: int = 7, base_open: float = 10400.0) -> pd.DataFrame:
    """Generate multiple sessions of intraday minute data (V2 demo set)."""
    dates = pd.bdate_range(start=start_date, end=end_date, freq="C")
    rng = np.random.default_rng(seed)
    price = base_open

    out = []
    for i, d in enumerate(dates):
        daily_ret = rng.normal(0.0, 60.0)
        open_ = price
        close_ = max(1000.0, open_ + daily_ret)
        hi_extra = abs(rng.normal(35.0, 12.0))
        lo_extra = abs(rng.normal(35.0, 12.0))
        high = max(open_, close_) + hi_extra
        low = min(open_, close_) - lo_extra
        vol = int(abs(rng.normal(650_000_000, 120_000_000)))

        daily = DailyOHLCV(date=d.strftime("%Y-%m-%d"), open=float(open_), high=float(high), low=float(low), close=float(close_), volume=vol)
        day_df = generate_intraday_1m(daily, sigma=0.8, seed=seed + i)
        out.append(day_df)
        price = close_

    return pd.concat(out, ignore_index=True)


def generate_multi_session_intraday_from_daily(daily: pd.DataFrame, seed: int = 7) -> pd.DataFrame:
    """Generate intraday minute bars for multiple sessions using *real daily* OHLCV.

    This is the bridge that makes the V2 platform feel realistic even when only
    daily provider data is available.

    Parameters
    ----------
    daily:
        DataFrame containing at least: date, open, high, low, close, volume.
        Date should be YYYY-MM-DD (London).
    seed:
        Random seed for deterministic intraday paths.
    """

    required = {"date", "open", "high", "low", "close", "volume"}
    if not required.issubset(set(daily.columns)):
        missing = sorted(required - set(daily.columns))
        raise ValueError(f"daily dataframe missing required columns: {missing}")

    df = daily.copy().sort_values("date").reset_index(drop=True)
    out = []
    for i, row in df.iterrows():
        d = DailyOHLCV(
            date=str(row["date"]),
            open=float(row["open"]),
            high=float(row["high"]),
            low=float(row["low"]),
            close=float(row["close"]),
            volume=int(row["volume"]),
        )
        out.append(generate_intraday_1m(d, sigma=0.8, seed=seed + int(i)))
    return pd.concat(out, ignore_index=True)
