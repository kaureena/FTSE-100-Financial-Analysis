from __future__ import annotations

from typing import Dict

import pandas as pd


def compare_metrics(arima_metrics: Dict[str, float], lstm_metrics: Dict[str, float]) -> pd.DataFrame:
    rows = []
    for m in sorted(set(arima_metrics) | set(lstm_metrics)):
        rows.append(
            {
                "metric": m,
                "arima": arima_metrics.get(m),
                "lstm": lstm_metrics.get(m),
                "winner": "ARIMA" if (arima_metrics.get(m, 1e18) < lstm_metrics.get(m, 1e18)) else "LSTM",
            }
        )
    return pd.DataFrame(rows)
