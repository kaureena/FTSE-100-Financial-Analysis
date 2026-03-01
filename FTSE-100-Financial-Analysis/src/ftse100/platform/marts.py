from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd

from ftse100.data.io import safe_to_parquet
from ftse100.utils import ensure_dir


def _as_dt(x) -> pd.Timestamp:
    return pd.to_datetime(x, utc=False)


def _rolling_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    # Simple RSI implementation (Wilder's smoothing approximation)
    delta = series.diff()
    gain = delta.clip(lower=0.0)
    loss = (-delta).clip(lower=0.0)

    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()

    rs = avg_gain / (avg_loss.replace(0.0, np.nan))
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi


def _classify_regime(vol_ratio: float, *, calm_max: float, normal_max: float) -> str:
    if np.isnan(vol_ratio):
        return "unknown"
    if vol_ratio < calm_max:
        return "calm"
    if vol_ratio < normal_max:
        return "normal"
    return "stressed"


def build_mart_market_overview(
    *,
    intraday_1m: pd.DataFrame,
    daily_gold: pd.DataFrame,
    run_id: str,
    finished_at: datetime,
) -> pd.DataFrame:
    """Market overview mart (intraday_5m grain)."""
    d = intraday_1m.copy()
    d["timestamp"] = _as_dt(d["timestamp"])
    d = d.sort_values("timestamp")

    # 5-minute aggregation
    ohlc = (
        d.set_index("timestamp")
        .resample("5T")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
        .dropna(subset=["close"])
        .reset_index()
    )
    ohlc["date"] = ohlc["timestamp"].dt.date

    # Prev close lookup (daily close)
    daily = daily_gold.copy()
    daily["date"] = pd.to_datetime(daily["date"]).dt.date
    daily = daily.sort_values("date")
    daily["prev_close"] = daily["close"].shift(1)
    prev_map = daily.set_index("date")["prev_close"].to_dict()
    ohlc["prev_close"] = ohlc["date"].map(prev_map)
    # If first day has no prev close, use first close as prev_close
    ohlc["prev_close"] = ohlc["prev_close"].fillna(method="bfill").fillna(ohlc["close"])

    ohlc["delta_pct"] = (ohlc["close"] / ohlc["prev_close"] - 1.0) * 100.0

    # Session high/low so far
    ohlc["session_high"] = ohlc.groupby("date")["high"].cummax()
    ohlc["session_low"] = ohlc.groupby("date")["low"].cummin()

    # Realised vol proxy: rolling std of 5m returns (20 periods ~ 100 minutes)
    ohlc["ret_5m"] = ohlc["close"].pct_change()
    ohlc["realised_vol_20"] = ohlc.groupby("date")["ret_5m"].transform(lambda s: s.rolling(20, min_periods=5).std() * np.sqrt(20))

    last_ts = ohlc["timestamp"].max()
    freshness_minutes = int(max(0.0, (finished_at - last_ts.to_pydatetime()).total_seconds() / 60.0))

    out = pd.DataFrame(
        {
            "timestamp_london": ohlc["timestamp"],
            "interval": "5m",
            "open": ohlc["open"],
            "high": ohlc["high"],
            "low": ohlc["low"],
            "close": ohlc["close"],
            "prev_close": ohlc["prev_close"],
            "delta_pct": ohlc["delta_pct"],
            "session_high": ohlc["session_high"],
            "session_low": ohlc["session_low"],
            "realised_vol_20": ohlc["realised_vol_20"],
            "volume": ohlc["volume"],
            "run_id": run_id,
            "freshness_minutes": freshness_minutes,
        }
    )
    return out


def build_mart_intraday_terminal(*, intraday_1m: pd.DataFrame, run_id: str) -> pd.DataFrame:
    d = intraday_1m.copy()
    d["timestamp_london"] = _as_dt(d["timestamp"])
    d = d.sort_values("timestamp_london").reset_index(drop=True)
    d["return_1m"] = d["close"].pct_change()
    d["ma_20"] = d["close"].rolling(20, min_periods=5).mean()
    d["ma_60"] = d["close"].rolling(60, min_periods=10).mean()
    d["rsi_14"] = _rolling_rsi(d["close"], window=14)
    # VWAP proxy
    d["vwap"] = (d["close"] * d["volume"]).cumsum() / (d["volume"].cumsum().replace(0.0, np.nan))
    d["run_id"] = run_id
    keep = [
        "timestamp_london",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "return_1m",
        "ma_20",
        "ma_60",
        "rsi_14",
        "vwap",
        "run_id",
    ]
    return d[keep]


def build_mart_volatility_regimes(
    *,
    market_overview_5m: pd.DataFrame,
    run_id: str,
    calm_max: float,
    normal_max: float,
) -> pd.DataFrame:
    d = market_overview_5m.copy()
    d = d.sort_values("timestamp_london").reset_index(drop=True)

    base = d["realised_vol_20"].rolling(50, min_periods=10).median()
    d["vol_ratio"] = d["realised_vol_20"] / base
    d["regime"] = d["vol_ratio"].apply(lambda x: _classify_regime(float(x), calm_max=calm_max, normal_max=normal_max))
    d["run_id"] = run_id

    return d[
        [
            "timestamp_london",
            "interval",
            "realised_vol_20",
            "vol_ratio",
            "regime",
            "run_id",
        ]
    ]


def build_mart_drawdown_risk(*, daily_gold: pd.DataFrame, run_id: str) -> pd.DataFrame:
    d = daily_gold.copy()
    d["date"] = pd.to_datetime(d["date"]).dt.date
    d = d.sort_values("date")

    # Basic VaR approximation (rolling 20d)
    ret = d["daily_return"].fillna(0.0)
    d["var_95"] = ret.rolling(20, min_periods=10).quantile(0.05)
    d["cvar_95"] = ret.rolling(20, min_periods=10).apply(lambda s: s[s <= np.quantile(s, 0.05)].mean() if len(s) else np.nan, raw=False)

    d["run_id"] = run_id
    keep = [
        "date",
        "close",
        "daily_return",
        "rolling_vol_20",
        "drawdown_pct",
        "momentum_10d_pct",
        "rsi_14",
        "var_95",
        "cvar_95",
        "run_id",
    ]
    return d[keep]


def build_mart_sector_rotation(*, sector_returns_daily: pd.DataFrame, run_id: str) -> pd.DataFrame:
    d = sector_returns_daily.copy()
    d["date"] = pd.to_datetime(d["date"]).dt.date
    d = d.sort_values(["sector", "date"])

    d["ret_5d"] = d.groupby("sector")["sector_return"].transform(lambda s: (1 + s).rolling(5, min_periods=3).apply(np.prod, raw=True) - 1)
    d["ret_20d"] = d.groupby("sector")["sector_return"].transform(lambda s: (1 + s).rolling(20, min_periods=10).apply(np.prod, raw=True) - 1)
    d["run_id"] = run_id
    return d[["date", "sector", "sector_return", "ret_5d", "ret_20d", "run_id"]]


def build_mart_top_movers(
    *,
    constituents_daily: pd.DataFrame,
    universe: pd.DataFrame,
    run_id: str,
    top_n: int = 10,
) -> pd.DataFrame:
    d = constituents_daily.copy()
    d["date"] = pd.to_datetime(d["date"]).dt.date

    u = universe.copy()
    u = u.rename(columns={"ticker": "ticker"})
    cols = [c for c in ["ticker", "company_name", "epic", "sector", "index_weight"] if c in u.columns]
    u = u[cols].drop_duplicates("ticker")

    d = d.merge(u, on="ticker", how="left", suffixes=("", "_u"))

    movers = []
    for dt, g in d.groupby("date"):
        g = g.sort_values("return", ascending=False)
        top = g.head(top_n).assign(direction="gainer", rank=lambda x: np.arange(1, len(x) + 1))
        bot = g.tail(top_n).sort_values("return").assign(direction="loser", rank=lambda x: np.arange(1, len(x) + 1))
        movers.append(pd.concat([top, bot], ignore_index=True))
    out = pd.concat(movers, ignore_index=True)
    out["run_id"] = run_id
    keep = [
        "date",
        "ticker",
        "company_name",
        "sector",
        "index_weight",
        "close",
        "return",
        "direction",
        "rank",
        "run_id",
    ]
    return out[keep]


def build_mart_correlation(
    *,
    sector_returns_daily: pd.DataFrame,
    run_id: str,
    window_days: int = 30,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    d = sector_returns_daily.copy()
    d["date"] = pd.to_datetime(d["date"]).dt.date
    d = d.sort_values("date")

    # last N days
    last_dates = sorted(d["date"].unique())[-window_days:]
    d = d[d["date"].isin(last_dates)]

    pivot = d.pivot_table(index="date", columns="sector", values="sector_return")
    corr = pivot.corr()

    # Matrix (long form)
    mat = corr.reset_index().melt(id_vars="sector", var_name="sector_y", value_name="corr")
    mat = mat.rename(columns={"sector": "sector_x"})
    mat["run_id"] = run_id

    # Pairs (upper triangle only)
    pairs = []
    sectors = list(corr.columns)
    for i, a in enumerate(sectors):
        for j, b in enumerate(sectors):
            if j <= i:
                continue
            pairs.append({"sector_a": a, "sector_b": b, "corr": float(corr.loc[a, b])})
    pairs_df = pd.DataFrame(pairs).sort_values("corr", ascending=False)
    pairs_df["run_id"] = run_id
    return mat[["sector_x", "sector_y", "corr", "run_id"]], pairs_df[["sector_a", "sector_b", "corr", "run_id"]]


def build_mart_technical_indicators(*, daily_gold: pd.DataFrame, run_id: str) -> pd.DataFrame:
    d = daily_gold.copy()
    d["date"] = pd.to_datetime(d["date"]).dt.date
    d = d.sort_values("date")

    d["ma_20"] = d["close"].rolling(20, min_periods=10).mean()
    d["std_20"] = d["close"].rolling(20, min_periods=10).std()
    d["bb_upper"] = d["ma_20"] + 2.0 * d["std_20"]
    d["bb_lower"] = d["ma_20"] - 2.0 * d["std_20"]

    ema12 = d["close"].ewm(span=12, adjust=False).mean()
    ema26 = d["close"].ewm(span=26, adjust=False).mean()
    d["macd"] = ema12 - ema26
    d["macd_signal"] = d["macd"].ewm(span=9, adjust=False).mean()
    d["run_id"] = run_id

    keep = ["date", "close", "ma_20", "bb_upper", "bb_lower", "rsi_14", "macd", "macd_signal", "run_id"]
    return d[keep]


def build_mart_pipeline_health(*, pipeline_runs_last14d: pd.DataFrame, run_id: str, runtime_sla_seconds: float) -> pd.DataFrame:
    d = pipeline_runs_last14d.copy()
    d["date"] = pd.to_datetime(d["date"]).dt.date
    d["sla_breach_flag"] = d["duration_sec"] > float(runtime_sla_seconds)
    d["run_id"] = run_id
    return d[["date", "job", "status", "duration_sec", "sla_breach_flag", "run_id"]]


def build_mart_latency_sla(*, latency_samples: pd.DataFrame, run_id: str) -> pd.DataFrame:
    d = latency_samples.copy()
    d["ts"] = pd.to_datetime(d["ts"])
    d = d.sort_values("ts")

    # Aggregate hourly
    d["hour"] = d["ts"].dt.floor("H")
    agg = d.groupby("hour")["latency_ms"].agg(["count", "mean", "median", "max", lambda s: np.quantile(s, 0.95)]).reset_index()
    agg.columns = ["hour", "n", "mean_ms", "p50_ms", "max_ms", "p95_ms"]
    agg["run_id"] = run_id
    return agg


def build_mart_data_quality_health(*, dq_latest_session: pd.DataFrame, dq_status_json: Dict, run_id: str) -> pd.DataFrame:
    d = dq_latest_session.copy()
    passed = int(d["passed"].sum())
    total = int(len(d))
    score = float(passed / max(total, 1) * 100.0)
    out = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "dq_score": score,
                "checks_total": total,
                "checks_passed": passed,
                "overall_status": dq_status_json.get("status", "UNKNOWN"),
                "generated_at": dq_status_json.get("generated_at", ""),
            }
        ]
    )
    return out


def build_mart_incidents(*, incident_timeline: pd.DataFrame, run_id: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    d = incident_timeline.copy()
    d["start"] = pd.to_datetime(d["start"])
    d["end"] = pd.to_datetime(d["end"])
    d["duration_min"] = (d["end"] - d["start"]).dt.total_seconds() / 60.0
    d["run_id"] = run_id

    timeline = d[["start", "end", "incident", "severity", "duration_min", "run_id"]].copy()
    register = timeline.copy()
    register["incident_id"] = [f"INC-{i+1:03d}" for i in range(len(register))]
    register["status"] = "closed"
    register["owner"] = "Data Platform"
    register["notes"] = ""
    return timeline, register


def build_lineage_marts(*, run_id: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    edges = [
        ("bronze.ftse100_intraday_1m_bronze", "silver.ftse100_intraday_1m_silver", "clean_enrich"),
        ("silver.ftse100_intraday_1m_silver", "gold.ftse100_daily_gold", "daily_aggregate"),
        ("gold.ftse100_daily_gold", "mart.drawdown_risk", "curate"),
        ("gold.ftse100_sector_returns_daily", "mart.sector_rotation", "curate"),
        ("gold.ftse100_sector_returns_daily", "mart.correlation_matrix", "curate"),
        ("gold.ftse100_constituents_daily", "mart.top_movers", "curate"),
        ("gold.events_calendar", "mart.board_pack", "enrich"),
        ("mart.market_overview", "dashboards.V2_P01", "render"),
    ]
    lineage_map = pd.DataFrame(edges, columns=["source", "target", "transform"]).assign(run_id=run_id)

    lineage_details = lineage_map.copy()
    lineage_details["owner"] = "Reena"
    lineage_details["sla"] = "5m intraday / 1d end-of-day"
    return lineage_map, lineage_details


def build_release_marts(*, run_id: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    versions = pd.DataFrame(
        [
            {"version_tag": "V1.0", "date": "2026-02-14", "summary": "Dissertation replay baseline (ARIMA + LSTM + 7 pages)"},
            {"version_tag": "V1.1", "date": "2026-02-15", "summary": "Contracts + provider layer + caching"},
            {"version_tag": "V2.0", "date": "2026-02-16", "summary": "Medallion platform + 22 neon terminal dashboards"},
            {"version_tag": "V2.1", "date": "2026-02-17", "summary": "Terminal realism: constituents + macro/earnings calendar + marts + warehouse"},
        ]
    )
    versions["run_id"] = run_id

    impacts = pd.DataFrame(
        [
            {"version_tag": "V2.1", "component": "marts", "impact": "Dashboards read curated mart.* tables", "risk": "low"},
            {"version_tag": "V2.1", "component": "warehouse", "impact": "DuckDB local warehouse created", "risk": "low"},
        ]
    )
    impacts["run_id"] = run_id

    trends = pd.DataFrame(
        [
            {"version_tag": "V1.0", "kpi": "export_pages", "value": 7},
            {"version_tag": "V2.0", "kpi": "export_pages", "value": 22},
            {"version_tag": "V2.1", "kpi": "mart_tables", "value": 35},
        ]
    )
    trends["run_id"] = run_id
    return versions, impacts, trends


def build_usage_maps(*, page_specs: pd.DataFrame, run_id: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # page_specs: columns page_id, page_name, uses_marts (comma-separated)
    d = page_specs.copy()
    d["run_id"] = run_id

    data_usage = []
    for _, r in d.iterrows():
        for t in str(r.get("uses_marts", "")).split(","):
            t = t.strip()
            if not t:
                continue
            data_usage.append({"page_id": r["page_id"], "page_name": r["page_name"], "mart_table": t})
    data_usage_df = pd.DataFrame(data_usage).assign(run_id=run_id)

    # KPI usage / measure usage are simplified (portfolio-friendly)
    kpi_usage = data_usage_df.copy()
    kpi_usage.rename(columns={"mart_table": "artifact"}, inplace=True)
    kpi_usage["kpi_hint"] = "see KPI_CATALOGUE.md"
    kpi_usage["run_id"] = run_id

    measure_usage = data_usage_df.copy()
    measure_usage.rename(columns={"mart_table": "artifact"}, inplace=True)
    measure_usage["measure_hint"] = "see METRICS_LIBRARY.md"
    measure_usage["run_id"] = run_id

    return data_usage_df, kpi_usage, measure_usage


def build_measure_dependencies(*, run_id: str) -> pd.DataFrame:
    deps = [
        ("delta_pct", ["close", "prev_close"]),
        ("realised_vol_20", ["close", "ret_5m"]),
        ("drawdown_pct", ["close", "cummax"]),
        ("rsi_14", ["close"]),
        ("macd", ["ema12", "ema26"]),
    ]
    rows = []
    for m, base in deps:
        for b in base:
            rows.append({"measure": m, "depends_on": b})
    return pd.DataFrame(rows).assign(run_id=run_id)


def build_alerts_register(
    *,
    dq_health: pd.DataFrame,
    latency_sla: pd.DataFrame,
    pipeline_health: pd.DataFrame,
    drift_report: Dict,
    run_id: str,
    thresholds: Dict,
) -> pd.DataFrame:
    alerts: List[Dict] = []

    # DQ score
    dq_score = float(dq_health["dq_score"].iloc[0]) if len(dq_health) else 100.0
    if dq_score < thresholds["data_quality"]["dq_score_fail"]:
        alerts.append({"alert_type": "DQ_SCORE", "severity": "HIGH", "message": f"DQ score {dq_score:.1f} below fail threshold"})
    elif dq_score < thresholds["data_quality"]["dq_score_warn"]:
        alerts.append({"alert_type": "DQ_SCORE", "severity": "MEDIUM", "message": f"DQ score {dq_score:.1f} below warn threshold"})

    # Latency p95
    if len(latency_sla):
        p95 = float(latency_sla["p95_ms"].tail(24).mean())
        if p95 > 1500:
            alerts.append({"alert_type": "LATENCY", "severity": "MEDIUM", "message": f"Mean p95 latency {p95:.0f}ms elevated"})

    # Pipeline breaches
    if len(pipeline_health):
        breaches = int(pipeline_health["sla_breach_flag"].sum())
        if breaches:
            alerts.append({"alert_type": "PIPELINE_RUNTIME", "severity": "LOW", "message": f"{breaches} SLA breach(es) in last 14d"})

    # Drift
    if drift_report:
        mean_shift = abs(float(drift_report.get("mean_shift", 0.0)))
        if mean_shift > 0.001:
            alerts.append({"alert_type": "RETURN_DRIFT", "severity": "LOW", "message": f"Return mean shift detected: {mean_shift:.4f}"})

    if not alerts:
        alerts = [{"alert_type": "NONE", "severity": "INFO", "message": "No active alerts"}]

    out = pd.DataFrame(alerts)
    out["run_id"] = run_id
    out["created_at"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    out["status"] = "open"
    return out


def build_forecasting_marts(*, model_metrics_timeseries: pd.DataFrame, run_id: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ts = model_metrics_timeseries.copy()
    ts["timestamp"] = pd.to_datetime(ts["timestamp"])
    ts["run_id"] = run_id

    # Latest metrics snapshot
    latest = ts.sort_values("timestamp").tail(1)
    cockpit = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "as_of": latest["timestamp"].iloc[0].date().isoformat() if len(latest) else "",
                "mae": float(latest["mae"].iloc[0]) if len(latest) else np.nan,
                "rmse": float(latest["rmse"].iloc[0]) if len(latest) else np.nan,
                "status": "green",
                "notes": "Model metrics from monitoring timeseries",
            }
        ]
    )

    model_runs = pd.DataFrame(
        [
            {"run_id": run_id, "model_name": "ARIMA", "horizon": "10m", "metric": "rmse", "value": float(latest["rmse"].iloc[0]) if len(latest) else np.nan},
            {"run_id": run_id, "model_name": "LSTM", "horizon": "10m", "metric": "mae", "value": float(latest["mae"].iloc[0]) if len(latest) else np.nan},
        ]
    )

    backtest = pd.DataFrame(
        [
            {"run_id": run_id, "backtest_window": "rolling_30d", "hit_rate_direction": 0.54, "notes": "Illustrative backtest summary (portfolio)"},
        ]
    )
    return cockpit, ts, model_runs, backtest


def write_marts(marts: Dict[str, pd.DataFrame], *, mart_dir: Path) -> None:
    mart_dir.mkdir(parents=True, exist_ok=True)
    for name, df in marts.items():
        # Name like 'mart.market_overview' -> file 'market_overview'
        fname = name.split(".", 1)[1] if name.startswith("mart.") else name
        safe_to_parquet(df, mart_dir / f"{fname}.parquet")
        df.to_csv(mart_dir / f"{fname}.csv", index=False)


def build_all_v2_marts(
    *,
    intraday_silver: pd.DataFrame,
    daily_gold: pd.DataFrame,
    constituents_daily: pd.DataFrame,
    sector_returns_daily: pd.DataFrame,
    universe: pd.DataFrame,
    events_calendar: pd.DataFrame,
    dq_latest_session: pd.DataFrame,
    dq_status_json: Dict,
    dq_issue_register: pd.DataFrame,
    pipeline_runs_last14d: pd.DataFrame,
    latency_samples: pd.DataFrame,
    incident_timeline: pd.DataFrame,
    model_metrics_timeseries: pd.DataFrame,
    drift_report: Dict,
    thresholds: Dict,
    page_specs: pd.DataFrame,
    kpi_dictionary: pd.DataFrame,
    measure_catalogue: pd.DataFrame,
    data_inventory: pd.DataFrame,
    run_id: str,
    finished_at: datetime,
) -> Dict[str, pd.DataFrame]:
    """Build all mart.* tables referenced by the V2 dashboard spec pack."""
    marts: Dict[str, pd.DataFrame] = {}

    market_overview = build_mart_market_overview(intraday_1m=intraday_silver, daily_gold=daily_gold, run_id=run_id, finished_at=finished_at)
    marts["mart.market_overview"] = market_overview

    marts["mart.intraday_terminal"] = build_mart_intraday_terminal(intraday_1m=intraday_silver, run_id=run_id)

    marts["mart.volatility_regimes"] = build_mart_volatility_regimes(
        market_overview_5m=market_overview,
        run_id=run_id,
        calm_max=float(thresholds["volatility_regimes"]["calm_max"]),
        normal_max=float(thresholds["volatility_regimes"]["normal_max"]),
    )

    marts["mart.drawdown_risk"] = build_mart_drawdown_risk(daily_gold=daily_gold, run_id=run_id)
    marts["mart.sector_rotation"] = build_mart_sector_rotation(sector_returns_daily=sector_returns_daily, run_id=run_id)
    marts["mart.top_movers"] = build_mart_top_movers(constituents_daily=constituents_daily, universe=universe, run_id=run_id, top_n=10)

    corr_matrix, corr_pairs = build_mart_correlation(sector_returns_daily=sector_returns_daily, run_id=run_id, window_days=30)
    marts["mart.correlation_matrix"] = corr_matrix
    marts["mart.correlation_pairs"] = corr_pairs

    marts["mart.technical_indicators"] = build_mart_technical_indicators(daily_gold=daily_gold, run_id=run_id)

    pipeline_health = build_mart_pipeline_health(
        pipeline_runs_last14d=pipeline_runs_last14d,
        run_id=run_id,
        runtime_sla_seconds=float(thresholds["pipeline"]["runtime_sla_seconds"]),
    )
    marts["mart.pipeline_health"] = pipeline_health

    latency_sla = build_mart_latency_sla(latency_samples=latency_samples, run_id=run_id)
    marts["mart.latency_sla"] = latency_sla

    dq_health = build_mart_data_quality_health(dq_latest_session=dq_latest_session, dq_status_json=dq_status_json, run_id=run_id)
    marts["mart.data_quality_health"] = dq_health

    incident_tl, incident_reg = build_mart_incidents(incident_timeline=incident_timeline, run_id=run_id)
    marts["mart.incident_timeline"] = incident_tl
    marts["mart.incident_register"] = incident_reg

    lineage_map, lineage_details = build_lineage_marts(run_id=run_id)
    marts["mart.lineage_map"] = lineage_map
    marts["mart.lineage_details"] = lineage_details

    versions, impacts, trends = build_release_marts(run_id=run_id)
    marts["mart.release_versions"] = versions
    marts["mart.release_impacts"] = impacts
    marts["mart.release_kpi_trends"] = trends

    data_usage, kpi_usage, measure_usage = build_usage_maps(page_specs=page_specs, run_id=run_id)
    marts["mart.data_usage_map"] = data_usage
    marts["mart.kpi_usage_map"] = kpi_usage
    marts["mart.measure_usage_map"] = measure_usage

    marts["mart.measure_dependencies"] = build_measure_dependencies(run_id=run_id)

    # Governance marts (aliases of gold tables; pages reference mart.*)
    marts["mart.kpi_dictionary"] = kpi_dictionary.copy()
    marts["mart.measure_catalogue"] = measure_catalogue.copy()
    marts["mart.data_inventory"] = data_inventory.copy()
    marts["mart.dq_issue_register"] = dq_issue_register.copy()

    # Alerts register
    marts["mart.alerts_register"] = build_alerts_register(
        dq_health=dq_health,
        latency_sla=latency_sla,
        pipeline_health=pipeline_health,
        drift_report=drift_report,
        run_id=run_id,
        thresholds=thresholds,
    )

    # Forecasting marts
    cockpit, metrics_ts, model_runs, backtest = build_forecasting_marts(model_metrics_timeseries=model_metrics_timeseries, run_id=run_id)
    marts["mart.forecasting_cockpit"] = cockpit
    marts["mart.forecasting_metrics"] = metrics_ts
    marts["mart.model_runs"] = model_runs
    marts["mart.backtesting_report"] = backtest

    # Model monitoring (simple drift extract)
    marts["mart.model_monitoring"] = pd.DataFrame([{"run_id": run_id, **(drift_report or {})}])

    # Board pack (one row)
    last_close = float(daily_gold.sort_values("date").tail(1)["close"].iloc[0]) if len(daily_gold) else np.nan
    marts["mart.board_pack"] = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "as_of": str(pd.to_datetime(daily_gold["date"]).max().date()) if len(daily_gold) else "",
                "close": last_close,
                "headline": "UK Market Terminal — Daily Board Pack",
                "notes": "Portfolio artefact (auto-generated)",
            }
        ]
    )

    # Events overlay (events calendar passthrough)
    ev = events_calendar.copy()
    if "timestamp_local" in ev.columns:
        ev["timestamp_london"] = pd.to_datetime(ev["timestamp_local"], errors="coerce")
    ev["run_id"] = run_id
    marts["mart.events_overlay"] = ev

    # Failure impact (illustrative linkage)
    marts["mart.failure_impact"] = pd.DataFrame(
        [
            {"run_id": run_id, "incident_id": "INC-003", "kpi": "dq_score", "impact": "export_blocked"},
        ]
    )

    return marts
