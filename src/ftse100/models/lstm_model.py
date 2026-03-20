from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import torch
from torch import nn

# Make CPU training predictable and fast
try:
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
except Exception:
    pass


class LSTMRegressor(nn.Module):
    def __init__(self, hidden_size: int = 32):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=hidden_size, num_layers=1, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        last = out[:, -1, :]
        return self.fc(last)


@dataclass
class LstmResult:
    lookback: int
    horizon: int
    forecast: pd.DataFrame
    metrics: Dict[str, float]
    training_history: pd.DataFrame
    scaler_mu: float
    scaler_std: float
    model: nn.Module | None = None


def _scale_series(y: np.ndarray) -> Tuple[np.ndarray, float, float]:
    mu = float(np.mean(y))
    std = float(np.std(y) + 1e-8)
    return (y - mu) / std, mu, std


def _inverse_scale(y_scaled: np.ndarray, mu: float, std: float) -> np.ndarray:
    return y_scaled * std + mu


def _make_sequences(series: np.ndarray, lookback: int) -> Tuple[np.ndarray, np.ndarray]:
    n = len(series) - lookback
    X = np.zeros((n, lookback, 1), dtype=np.float32)
    y = np.zeros((n, 1), dtype=np.float32)
    for i in range(n):
        X[i, :, 0] = series[i : i + lookback]
        y[i, 0] = series[i + lookback]
    return X, y


def fit_lstm_forecast(
    df: pd.DataFrame,
    lookback: int = 60,
    horizon: int = 10,
    epochs: int = 25,
    lr: float = 3e-3,
    hidden_size: int = 32,
    seed: int = 42,
    return_model: bool = False,
) -> LstmResult:
    """Fast LSTM training + 10-minute iterative forecast.

    Implementation note:
    - Builds all sequences once and uses full-batch training.
    - This avoids DataLoader overhead and keeps runtime small for portfolio builds.
    """

    torch.manual_seed(seed)
    np.random.seed(seed)

    d = df.sort_values("timestamp").reset_index(drop=True)
    y_full = d["close"].astype(float).values

    if len(y_full) <= horizon + lookback + 20:
        raise ValueError("Not enough rows to train and forecast.")

    train_y = y_full[:-horizon]
    test_y = y_full[-horizon:]
    test_ts = d.loc[d.index[-horizon:], "timestamp"].reset_index(drop=True)

    y_scaled, mu, std = _scale_series(train_y)
    X, y = _make_sequences(y_scaled.astype(np.float32), lookback=lookback)

    X_t = torch.from_numpy(X)
    y_t = torch.from_numpy(y)

    model = LSTMRegressor(hidden_size=hidden_size)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()

    history = []
    model.train()
    for epoch in range(1, epochs + 1):
        opt.zero_grad()
        pred = model(X_t)
        loss = loss_fn(pred, y_t)
        loss.backward()
        opt.step()
        history.append({"epoch": epoch, "train_loss": float(loss.item())})

    hist_df = pd.DataFrame(history)

    # Iterative forecast
    model.eval()
    window = y_scaled[-lookback:].astype(np.float32).copy()
    preds_scaled = []
    with torch.no_grad():
        for _ in range(horizon):
            xb = torch.from_numpy(window.reshape(1, lookback, 1))
            yhat = model(xb).numpy().ravel()[0]
            preds_scaled.append(yhat)
            window = np.concatenate([window[1:], np.array([yhat], dtype=np.float32)])

    preds = _inverse_scale(np.array(preds_scaled), mu=mu, std=std)

    forecast_df = pd.DataFrame({"timestamp": test_ts, "yhat": preds, "y": test_y})

    err = forecast_df["yhat"].values - forecast_df["y"].values
    mae = float(np.mean(np.abs(err)))
    rmse = float(np.sqrt(np.mean(err**2)))
    mape = float(np.mean(np.abs(err / forecast_df["y"].values)) * 100.0)

    metrics = {"mae": mae, "rmse": rmse, "mape_pct": mape}

    return LstmResult(
        lookback=lookback,
        horizon=horizon,
        forecast=forecast_df,
        metrics=metrics,
        training_history=hist_df,
        scaler_mu=mu,
        scaler_std=std,
        model=model if return_model else None,
    )


def integrated_gradients_importance(model: nn.Module, window_scaled: np.ndarray, steps: int = 32) -> np.ndarray:
    """Integrated gradients over timesteps for a single univariate window."""
    model.eval()
    x = torch.from_numpy(window_scaled.astype(np.float32)).reshape(1, -1, 1)
    baseline = torch.zeros_like(x)

    alphas = torch.linspace(0.0, 1.0, steps)
    grads = []
    for a in alphas:
        xi = baseline + a * (x - baseline)
        xi.requires_grad_(True)
        y = model(xi)
        y.sum().backward()
        grads.append(xi.grad.detach().numpy())

    avg_grad = np.mean(np.stack(grads, axis=0), axis=0)
    ig = (x.detach().numpy() - baseline.detach().numpy()) * avg_grad
    imp = np.abs(ig[0, :, 0])
    imp = imp / (imp.sum() + 1e-12)
    return imp
