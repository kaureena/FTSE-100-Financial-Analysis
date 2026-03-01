from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


@dataclass
class ArimaResult:
    order: Tuple[int, int, int]
    forecast: pd.DataFrame  # timestamp, yhat, yhat_lower, yhat_upper, y
    metrics: Dict[str, float]
    model_summary_text: str


def fit_arima_forecast(df: pd.DataFrame, order: Tuple[int, int, int] = (5, 1, 0), horizon: int = 10) -> ArimaResult:
    d = df.sort_values("timestamp").reset_index(drop=True)
    y = d["close"].astype(float).values

    if len(y) <= horizon + 20:
        raise ValueError("Not enough rows to train and forecast.")

    train_y = y[:-horizon]
    test_y = y[-horizon:]
    test_ts = d.loc[d.index[-horizon:], "timestamp"].reset_index(drop=True)

    model = ARIMA(train_y, order=order)
    fitted = model.fit()

    fc = fitted.get_forecast(steps=horizon)
    mean = fc.predicted_mean
    ci = fc.conf_int(alpha=0.05)

    forecast_df = pd.DataFrame(
        {
            "timestamp": test_ts,
            "yhat": mean,
            "yhat_lower": ci[:, 0],
            "yhat_upper": ci[:, 1],
            "y": test_y,
        }
    )

    err = forecast_df["yhat"].values - forecast_df["y"].values
    mae = float(np.mean(np.abs(err)))
    rmse = float(np.sqrt(np.mean(err**2)))
    mape = float(np.mean(np.abs(err / forecast_df["y"].values)) * 100.0)

    metrics = {"mae": mae, "rmse": rmse, "mape_pct": mape}
    return ArimaResult(order=order, forecast=forecast_df, metrics=metrics, model_summary_text=str(fitted.summary()))
