from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..features import add_moving_averages, add_realised_vol, add_returns, compute_session_kpis
from ..monitoring.dq import dq_summary_table, overall_status, run_dq_checks
from ..utils import ensure_dir, now_london_iso
from .style import THEME, apply_theme


def _save(fig: plt.Figure, out_path: Path) -> None:
    """Save exports at a consistent 4K resolution (3840×2160).

    Notes
    -----
    We deliberately avoid `bbox_inches="tight"` because it changes pixel output
    sizes unpredictably (cropping), which breaks portfolio-grade consistency.
    """
    ensure_dir(out_path.parent)

    # Enforce a fixed canvas: 19.2×10.8 inches @ 200 DPI = 3840×2160 px
    fig.set_size_inches(19.2, 10.8)

    fig.savefig(
        out_path,
        dpi=200,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
    )
    plt.close(fig)


def _header(ax, title: str, run_id: str, subtitle: str = "", disclaimer: str = "Not financial advice") -> None:
    ax.axis("off")
    ts = now_london_iso()
    ax.text(0.01, 0.75, title, fontsize=22, fontweight="bold", color=THEME.text)
    if subtitle:
        ax.text(0.01, 0.25, subtitle, fontsize=12, color=THEME.muted)
    ax.text(0.99, 0.75, f"run_id: {run_id}", ha="right", fontsize=11, color=THEME.muted)
    ax.text(0.99, 0.25, f"London: {ts} | {disclaimer}", ha="right", fontsize=11, color=THEME.muted)


def export_page_01_market_overview(df: pd.DataFrame, out_path: Path, run_id: str) -> None:
    apply_theme()
    d = add_realised_vol(add_returns(df), window=20)
    kpis = compute_session_kpis(d).set_index("kpi")["value"].to_dict()

    fig = plt.figure(figsize=(19.2, 10.8))
    gs = fig.add_gridspec(12, 12)

    ax_head = fig.add_subplot(gs[0:2, :])
    _header(ax_head, "FTSE 100 • Market Overview (V1)", run_id, subtitle=f"Intraday 1-minute session replay • {df['date'].iloc[0]}")

    ax_kpi = fig.add_subplot(gs[2:4, 0:12])
    ax_kpi.axis("off")
    tiles = [
        ("Open", kpis["close_first"], "pts"),
        ("Close", kpis["close_last"], "pts"),
        ("Δ%", kpis["intraday_return_pct"], "%"),
        ("High", kpis["high"], "pts"),
        ("Low", kpis["low"], "pts"),
        ("Range", kpis["range"], "pts"),
        ("Realised Vol (20)", kpis["realised_vol_20_mean"], "σ"),
    ]
    n = len(tiles)
    for i, (label, val, unit) in enumerate(tiles):
        x0 = 0.01 + i * (0.98 / n)
        ax_kpi.text(x0, 0.75, label, fontsize=11, color=THEME.muted, transform=ax_kpi.transAxes)
        ax_kpi.text(x0, 0.25, f"{val:,.2f} {unit}", fontsize=16, fontweight="bold", transform=ax_kpi.transAxes)

    ax = fig.add_subplot(gs[4:12, 0:12])
    ax.grid(True)

    ts = pd.to_datetime(d["timestamp"])
    x = mdates.date2num(ts.dt.to_pydatetime())
    ax.plot_date(x, d["close"], fmt='-', linewidth=2.2, color=THEME.neon_cyan, label="Close")
    ax.fill_between(x, d["low"].astype(float).values, d["high"].astype(float).values, color=THEME.neon_purple, alpha=0.08, label="High/Low band")
    ax.xaxis_date()

    ax.set_title("Intraday Trend with High/Low Envelope", loc="left", fontsize=14)
    ax.set_ylabel("Index level (points)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.legend(loc="upper left")

    _save(fig, out_path)


def _candlestick(ax, df: pd.DataFrame, width_minutes: float = 0.8) -> None:
    d = df.copy()
    d["timestamp"] = pd.to_datetime(d["timestamp"])
    x = mdates.date2num(d["timestamp"].dt.to_pydatetime())
    w = width_minutes / (24 * 60)

    for xi, o, h, l, c in zip(x, d["open"], d["high"], d["low"], d["close"]):
        up = c >= o
        col = THEME.neon_green if up else THEME.neon_red
        ax.vlines(xi, l, h, color=col, linewidth=1.2, alpha=0.9)
        rect_y = min(o, c)
        rect_h = max(0.01, abs(c - o))
        ax.add_patch(plt.Rectangle((xi - w / 2, rect_y), w, rect_h, facecolor=col, edgecolor=col, alpha=0.9))


def export_page_02_candles_volume(df: pd.DataFrame, out_path: Path, run_id: str) -> None:
    apply_theme()
    d = df.sort_values("timestamp").reset_index(drop=True)

    fig = plt.figure(figsize=(19.2, 10.8))
    gs = fig.add_gridspec(12, 12)

    ax_head = fig.add_subplot(gs[0:2, :])
    _header(ax_head, "FTSE 100 • Candles + Volume (V1)", run_id, subtitle=f"Intraday 1-minute candlestick replay • {d['date'].iloc[0]}")

    ax_c = fig.add_subplot(gs[2:9, 0:12])
    ax_v = fig.add_subplot(gs[9:12, 0:12], sharex=ax_c)

    ax_c.grid(True)
    ax_v.grid(True)

    _candlestick(ax_c, d)
    ax_c.set_title("1-Min Candlesticks", loc="left", fontsize=14)
    ax_c.set_ylabel("Index level (points)")

    ts = pd.to_datetime(d["timestamp"])
    ax_v.bar(ts, d["volume"], width=0.0008, alpha=0.6, color=THEME.neon_yellow)
    ax_v.set_title("Volume (distributed)", loc="left", fontsize=12)
    ax_v.set_ylabel("Volume")
    ax_v.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    _save(fig, out_path)


def export_page_03_moving_averages(df: pd.DataFrame, out_path: Path, run_id: str) -> None:
    apply_theme()
    d = add_moving_averages(add_returns(df), windows=(20, 50))

    fig = plt.figure(figsize=(19.2, 10.8))
    gs = fig.add_gridspec(12, 12)

    ax_head = fig.add_subplot(gs[0:2, :])
    _header(ax_head, "FTSE 100 • Moving Averages (V1)", run_id, subtitle=f"SMA/EMA overlays + signals • {df['date'].iloc[0]}")

    ax = fig.add_subplot(gs[2:12, 0:12])
    ax.grid(True)

    ts = pd.to_datetime(d["timestamp"])
    ax.plot(ts, d["close"], color=THEME.neon_cyan, linewidth=2.0, label="Close")
    ax.plot(ts, d["sma_20"], color=THEME.neon_pink, linewidth=1.6, label="SMA 20")
    ax.plot(ts, d["sma_50"], color=THEME.neon_purple, linewidth=1.6, label="SMA 50")
    ax.plot(ts, d["ema_20"], color=THEME.neon_green, linewidth=1.2, alpha=0.8, label="EMA 20")

    ax.set_title("Trend Smoothing and Potential Crossover", loc="left", fontsize=14)
    ax.set_ylabel("Index level (points)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.legend(loc="upper left")

    _save(fig, out_path)


def export_page_04_arima_forecast(
    df: pd.DataFrame,
    forecast_df: pd.DataFrame,
    metrics: Dict[str, float],
    out_path: Path,
    run_id: str,
    order=(5, 1, 0),
) -> None:
    apply_theme()
    d = df.sort_values("timestamp").reset_index(drop=True)

    fig = plt.figure(figsize=(19.2, 10.8))
    gs = fig.add_gridspec(12, 12)

    ax_head = fig.add_subplot(gs[0:2, :])
    _header(ax_head, "FTSE 100 • ARIMA Forecast (V1)", run_id, subtitle=f"ARIMA{order} • Horizon: 10 min • {df['date'].iloc[0]}")

    ax = fig.add_subplot(gs[2:12, 0:12])
    ax.grid(True)

    ts = pd.to_datetime(d["timestamp"])
    ax.plot(ts, d["close"], color=THEME.neon_cyan, linewidth=1.8, label="Close")

    fts = pd.to_datetime(forecast_df["timestamp"])
    fx = mdates.date2num(fts.dt.to_pydatetime())
    ax.plot_date(fx, forecast_df["yhat"], fmt='-', color=THEME.neon_pink, linewidth=2.2, label="ARIMA forecast")
    ax.fill_between(fx, forecast_df["yhat_lower"].astype(float).values, forecast_df["yhat_upper"].astype(float).values, color=THEME.neon_pink, alpha=0.15, label="95% CI")
    ax.scatter(fx, forecast_df["y"], color=THEME.neon_yellow, s=35, label="Actual")
    ax.xaxis_date()

    ax.set_title(f"ARIMA Forecast vs Actual (MAE={metrics['mae']:.2f}, RMSE={metrics['rmse']:.2f})", loc="left", fontsize=14)
    ax.set_ylabel("Index level (points)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.legend(loc="upper left")

    _save(fig, out_path)


def export_page_05_lstm_forecast(
    df: pd.DataFrame,
    forecast_df: pd.DataFrame,
    metrics: Dict[str, float],
    loss_df: pd.DataFrame,
    importance: np.ndarray | None,
    out_path: Path,
    run_id: str,
) -> None:
    apply_theme()
    d = df.sort_values("timestamp").reset_index(drop=True)

    fig = plt.figure(figsize=(19.2, 10.8))
    gs = fig.add_gridspec(12, 12)

    ax_head = fig.add_subplot(gs[0:2, :])
    _header(ax_head, "FTSE 100 • LSTM Forecast (V1)", run_id, subtitle=f"Lookback: 60 • Horizon: 10 min • {df['date'].iloc[0]}")

    ax1 = fig.add_subplot(gs[2:8, 0:12])
    ax2 = fig.add_subplot(gs[8:12, 0:6])
    ax3 = fig.add_subplot(gs[8:12, 6:12])

    ax1.grid(True)
    ts = pd.to_datetime(d["timestamp"])
    ax1.plot(ts, d["close"], color=THEME.neon_cyan, linewidth=1.6, label="Close")
    fts = pd.to_datetime(forecast_df["timestamp"])
    ax1.plot(fts, forecast_df["yhat"], color=THEME.neon_green, linewidth=2.2, label="LSTM forecast")
    ax1.scatter(fts, forecast_df["y"], color=THEME.neon_yellow, s=35, label="Actual")

    ax1.set_title(f"LSTM Forecast vs Actual (MAE={metrics['mae']:.2f}, RMSE={metrics['rmse']:.2f})", loc="left", fontsize=14)
    ax1.set_ylabel("Index level (points)")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax1.legend(loc="upper left")

    ax2.grid(True)
    ax2.plot(loss_df["epoch"], loss_df["train_loss"], color=THEME.neon_pink, linewidth=2.0)
    ax2.set_title("Training loss", loc="left", fontsize=12)
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("MSE")

    ax3.axis("off")
    if importance is not None:
        topk = 10
        idx = np.argsort(-importance)[:topk]
        labels = [f"t-{(len(importance)-1-i):02d}" for i in idx]
        vals = importance[idx]
        ax3.barh(labels[::-1], vals[::-1], color=THEME.neon_purple, alpha=0.8)
        ax3.set_title("Input timestep importance (Integrated Gradients)", loc="left", fontsize=12)
    else:
        ax3.text(0.02, 0.5, "Interpretability: n/a", fontsize=12, color=THEME.muted)

    _save(fig, out_path)


def export_page_06_model_comparison(
    df: pd.DataFrame,
    arima_fc: pd.DataFrame,
    lstm_fc: pd.DataFrame,
    comparison_table: pd.DataFrame,
    out_path: Path,
    run_id: str,
) -> None:
    apply_theme()
    d = df.sort_values("timestamp").reset_index(drop=True)

    fig = plt.figure(figsize=(19.2, 10.8))
    gs = fig.add_gridspec(12, 12)

    ax_head = fig.add_subplot(gs[0:2, :])
    _header(ax_head, "FTSE 100 • Model Comparison (V1)", run_id, subtitle=f"ARIMA vs LSTM • {df['date'].iloc[0]}")

    ax1 = fig.add_subplot(gs[2:9, 0:12])
    ax2 = fig.add_subplot(gs[9:12, 0:12])

    ax1.grid(True)

    ts = pd.to_datetime(d["timestamp"])
    ax1.plot(ts, d["close"], color=THEME.neon_cyan, linewidth=1.6, label="Close")

    fts = pd.to_datetime(arima_fc["timestamp"])
    ax1.plot(fts, arima_fc["yhat"], color=THEME.neon_pink, linewidth=2.0, label="ARIMA yhat")
    ax1.plot(pd.to_datetime(lstm_fc["timestamp"]), lstm_fc["yhat"], color=THEME.neon_green, linewidth=2.0, label="LSTM yhat")
    ax1.scatter(fts, arima_fc["y"], color=THEME.neon_yellow, s=30, label="Actual")

    ax1.set_title("Forecast overlay (next 10 minutes)", loc="left", fontsize=14)
    ax1.set_ylabel("Index level (points)")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax1.legend(loc="upper left")

    ax2.axis("off")

    table = comparison_table.copy()
    table["arima"] = table["arima"].map(lambda x: f"{x:.2f}" if pd.notnull(x) else "-")
    table["lstm"] = table["lstm"].map(lambda x: f"{x:.2f}" if pd.notnull(x) else "-")

    ax2.text(0.01, 0.95, "Metric scoreboard", fontsize=12, color=THEME.muted, va="top")
    ax2.text(0.01, 0.85, table.to_string(index=False), family="monospace", fontsize=11, va="top")

    _save(fig, out_path)


def export_page_07_dq_snapshot(df: pd.DataFrame, out_path: Path, run_id: str) -> None:
    apply_theme()
    checks = run_dq_checks(df)
    status = overall_status(checks)
    table = dq_summary_table(checks)

    fig = plt.figure(figsize=(19.2, 10.8))
    gs = fig.add_gridspec(12, 12)

    ax_head = fig.add_subplot(gs[0:2, :])
    _header(ax_head, "FTSE 100 • Data Quality Snapshot (V1)", run_id, subtitle=f"Overall status: {status} • {df['date'].iloc[0]}")

    ax = fig.add_subplot(gs[2:12, 0:12])
    ax.axis("off")

    table2 = table.copy()
    table2["passed"] = table2["passed"].map(lambda x: "PASS" if x else "FAIL")

    ax.text(0.01, 0.95, "DQ checks", fontsize=12, color=THEME.muted, va="top")
    ax.text(0.01, 0.9, table2.to_string(index=False), family="monospace", fontsize=11, va="top")

    _save(fig, out_path)
