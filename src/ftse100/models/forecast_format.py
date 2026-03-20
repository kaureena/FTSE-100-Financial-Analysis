from __future__ import annotations

from datetime import datetime
from typing import Optional

import pandas as pd


def to_contract_forecast(
    *,
    forecast_df: pd.DataFrame,
    model_name: str,
    origin_timestamp: datetime,
    run_id: str,
    horizon_unit: str = "minute",
) -> pd.DataFrame:
    """Convert an internal forecast dataframe into the repo's canonical contract schema.

    The canonical schema is defined in DATA_CONTRACTS.md#v1-forecasts.

    Parameters
    ----------
    forecast_df:
        Must contain: timestamp (target), yhat, y (actual).
        May contain: yhat_lower, yhat_upper.
    origin_timestamp:
        Timestamp when the forecast was issued (last timestamp in the training window).
    """
    d = forecast_df.copy()
    if "timestamp" not in d.columns:
        raise ValueError("forecast_df must contain 'timestamp'")
    if "yhat" not in d.columns:
        raise ValueError("forecast_df must contain 'yhat'")
    if "y" not in d.columns:
        raise ValueError("forecast_df must contain 'y' (actual)")

    d = d.sort_values("timestamp").reset_index(drop=True)
    d["origin_timestamp"] = origin_timestamp
    d["target_timestamp"] = d["timestamp"]
    d["horizon_step"] = d.index + 1
    d["y_true"] = d["y"]
    d["model_name"] = str(model_name).upper()
    d["residual"] = d["y_true"] - d["yhat"]
    d["run_id"] = run_id
    d["horizon_unit"] = horizon_unit

    cols = [
        "run_id",
        "model_name",
        "origin_timestamp",
        "target_timestamp",
        "horizon_step",
        "horizon_unit",
        "y_true",
        "yhat",
        "residual",
    ]
    # Keep optional bands if present
    for opt in ["yhat_lower", "yhat_upper"]:
        if opt in d.columns:
            cols.append(opt)

    return d[cols]
