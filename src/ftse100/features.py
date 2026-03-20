from __future__ import annotations

import numpy as np
import pandas as pd


def add_returns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["return_simple"] = out["close"].pct_change()
    out["return_log"] = np.log(out["close"]).diff()
    return out


def add_moving_averages(df: pd.DataFrame, windows=(20, 50)) -> pd.DataFrame:
    out = df.copy()
    for w in windows:
        out[f"sma_{w}"] = out["close"].rolling(w).mean()
        out[f"ema_{w}"] = out["close"].ewm(span=w, adjust=False).mean()
    return out


def add_realised_vol(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    out = df.copy()
    if "return_simple" not in out.columns:
        out = add_returns(out)
    out[f"realised_vol_{window}"] = out["return_simple"].rolling(window).std() * np.sqrt(window)
    return out


def compute_session_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Session-level KPIs used by dashboard tiles."""
    d = df.sort_values("timestamp").reset_index(drop=True)
    close_first = float(d.loc[0, "close"])
    close_last = float(d.loc[d.index[-1], "close"])
    high = float(d["high"].max())
    low = float(d["low"].min())
    volume = int(d["volume"].sum())
    ret_pct = (close_last / close_first - 1.0) * 100.0
    rng = high - low

    d2 = add_realised_vol(add_returns(d), window=20)
    rv = float(d2["realised_vol_20"].mean(skipna=True))

    return pd.DataFrame(
        [
            {"kpi": "close_first", "value": close_first, "unit": "points"},
            {"kpi": "close_last", "value": close_last, "unit": "points"},
            {"kpi": "intraday_return_pct", "value": ret_pct, "unit": "%"},
            {"kpi": "high", "value": high, "unit": "points"},
            {"kpi": "low", "value": low, "unit": "points"},
            {"kpi": "range", "value": rng, "unit": "points"},
            {"kpi": "volume", "value": volume, "unit": "shares"},
            {"kpi": "realised_vol_20_mean", "value": rv, "unit": "std"},
        ]
    )
