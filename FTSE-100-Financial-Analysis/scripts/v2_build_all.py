"""V2 build: modern platform tables + monitoring + premium neon dashboards.

This script is intentionally *offline-first*: it generates a realistic synthetic
FTSE 100 environment (index + constituents + sectors) and produces all
medallion tables, monitoring artifacts, and 22 dashboard exports.

Dashboard export filenames follow the dense dashboard spec pack under:
- docs/dashboards/V2/pages/*.md

Exports are written to:
- docs/dashboards/V2/exports/
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

# Matplotlib (neon terminal look)
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from ftse100.config import (
    DATA_CACHE_DIR,
    DEFAULT_TIMEZONE,
    DOCS_DASH_V2_EXPORTS_DIR,
    INDEX_SYMBOL_PRIMARY,
    INDEX_SYMBOL_STOOQ,
    V2_DATA_BRONZE_DIR,
    V2_DATA_GOLD_DIR,
    V2_DATA_SILVER_DIR,
    V2_DATA_MART_DIR,
    V2_DB_DIR,
    V2_LOGS_DIR,
    V2_METRICS_DIR,
    V2_MONITORING_DIR,
)
from ftse100.data.io import safe_to_parquet
from ftse100.monitoring import append_run_register
from ftse100.platform import build_all_v2_marts, write_marts, build_duckdb_warehouse
from ftse100.data.providers.registry import get_provider
from ftse100.data.synthetic import generate_multi_session_intraday, generate_multi_session_intraday_from_daily
from ftse100.monitoring.dq import dq_summary_table, overall_status, run_dq_checks
from ftse100.utils import SimpleLogger, make_run_id, write_json
from ftse100.viz.export_v2 import export_v2_pages_from_marts
from ftse100.viz.style import THEME, apply_theme
from ftse100.reference import build_events_calendar, load_ftse100_universe


# -----------------------------
# Helpers
# -----------------------------

def _ensure(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def _save(fig: plt.Figure, out_path: Path) -> None:
    """Save at a consistent 4K resolution (3840×2160)."""
    _ensure(out_path)

    # 19.2×10.8 inches @ 200 DPI = 3840×2160 pixels
    fig.set_size_inches(19.2, 10.8)
    fig.savefig(
        out_path,
        dpi=200,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
    )
    plt.close(fig)


def _header(fig: plt.Figure, gs, title: str, subtitle: str, run_id: str):
    ax_head = fig.add_subplot(gs[0:2, :])
    ax_head.axis("off")
    ax_head.text(0.01, 0.75, title, fontsize=22, fontweight="bold", color=THEME.text)
    ax_head.text(0.01, 0.25, subtitle, fontsize=12, color=THEME.muted)
    ax_head.text(0.99, 0.75, f"run_id: {run_id}", ha="right", fontsize=11, color=THEME.muted)
    ax_head.text(0.99, 0.25, "London: Europe/London | Not financial advice", ha="right", fontsize=11, color=THEME.muted)
    return ax_head


def compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / (avg_loss + 1e-12)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def make_constituent_universe(n: int = 100, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    sectors = [
        "Financials",
        "Energy",
        "Materials",
        "Industrials",
        "Consumer Discretionary",
        "Consumer Staples",
        "Health Care",
        "Technology",
        "Utilities",
        "Real Estate",
    ]
    tickers = [f"FTSE{i:03d}.L" for i in range(1, n + 1)]
    sector_assign = rng.choice(sectors, size=n, replace=True)
    weights = rng.random(n)
    weights = weights / weights.sum()
    return pd.DataFrame({"ticker": tickers, "sector": sector_assign, "index_weight": weights})


def simulate_constituent_daily(
    daily_index: pd.DataFrame,
    universe: pd.DataFrame,
    seed: int = 11,
) -> pd.DataFrame:
    """Factor-model simulation: each constituent return = beta * index_return + noise."""
    rng = np.random.default_rng(seed)

    idx = daily_index.copy().sort_values("date")
    idx["index_ret"] = idx["close"].pct_change().fillna(0.0)

    rows = []
    for _, row in universe.iterrows():
        beta = float(rng.normal(0.9, 0.25))
        sigma = float(abs(rng.normal(0.012, 0.006)))
        eps = rng.normal(0.0, sigma, size=len(idx))
        ret = beta * idx["index_ret"].values + eps
        price0 = float(rng.uniform(50.0, 500.0))
        price = price0 * np.cumprod(1.0 + ret)
        df = pd.DataFrame(
            {
                "date": idx["date"].values,
                "timestamp": pd.to_datetime(idx["date"].values),
                "ticker": row["ticker"],
                "sector": row["sector"],
                "index_weight": row["index_weight"],
                "close": price,
                "return": ret,
            }
        )
        rows.append(df)

    return pd.concat(rows, ignore_index=True)


def render_table(ax, df: pd.DataFrame, title: str, max_rows: int = 20) -> None:
    ax.axis("off")
    ax.text(0.01, 0.98, title, fontsize=14, fontweight="bold", color=THEME.text, va="top")
    show = df.head(max_rows).copy()
    text = show.to_string(index=False)
    ax.text(0.01, 0.90, text, family="monospace", fontsize=11, color=THEME.text, va="top")


# -----------------------------
# Build
# -----------------------------


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="V2 build (platform): medallion tables → monitoring → exports")
    p.add_argument(
        "--data-source",
        default=os.getenv("FTSE100_PROVIDER", "synthetic"),
        help="Data source: synthetic | yahoo | stooq | alphavantage | polygon",
    )
    p.add_argument(
        "--symbol",
        default=os.getenv("FTSE100_SYMBOL", INDEX_SYMBOL_STOOQ),
        help="Provider-specific symbol for V2 daily anchor.",
    )
    p.add_argument(
        "--start-date",
        default=os.getenv("FTSE100_V2_START", "2025-11-03"),
        help="Start date for V2 multi-session build (YYYY-MM-DD).",
    )
    p.add_argument(
        "--end-date",
        default=os.getenv("FTSE100_V2_END", "2026-02-13"),
        help="End date for V2 multi-session build (YYYY-MM-DD).",
    )
    p.add_argument(
        "--cache-dir",
        default=os.getenv("FTSE100_CACHE_DIR", str(DATA_CACHE_DIR)),
        help="Cache dir for provider pulls.",
    )
    p.add_argument(
        "--force-refresh",
        action="store_true",
        help="Bypass cache and re-pull from provider (if live mode).",
    )
    p.add_argument(
        "--constituents-source",
        default=os.getenv("FTSE100_CONSTITUENTS_SOURCE", "snapshot"),
        help="Constituents universe source: snapshot | wikipedia | synthetic",
    )
    p.add_argument(
        "--weights-method",
        default=os.getenv("FTSE100_WEIGHTS_METHOD", "snapshot"),
        help="Universe weights: snapshot | equal",
    )
    p.add_argument(
        "--include-news",
        action="store_true",
        help="Include a (stub) UK market news headlines feed in the events calendar.",
    )
    return p.parse_args()

def main() -> None:
    args = _parse_args()
    started_at = datetime.utcnow()
    run_id = make_run_id(prefix="v2")
    log = SimpleLogger(V2_LOGS_DIR / "build_v2.jsonl")
    log.info("start_v2_build", run_id=run_id)

    # --------------------------------------------------------
    # 1) Generate multi-session intraday dataset (bronze)
    # --------------------------------------------------------
    data_source = (args.data_source or "synthetic").strip().lower()
    start_date = args.start_date
    end_date = args.end_date

    if data_source == "synthetic":
        intraday = generate_multi_session_intraday(start_date=start_date, end_date=end_date, seed=7, base_open=10400.0)
        log.info("intraday_generated", mode="synthetic", start_date=start_date, end_date=end_date)
    else:
        # Provider mode for V2:
        # - Pull DAILY bars for the range
        # - Generate minute-level intraday paths constrained to daily OHLCV
        cache_dir = Path(args.cache_dir)

        api_key = None
        if data_source in {"alphavantage", "alpha-vantage", "av"}:
            api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if data_source in {"polygon", "polygonio"}:
            api_key = os.getenv("POLYGON_API_KEY")

        provider = get_provider(
            data_source,
            api_key=api_key,
            cache_dir=cache_dir,
            force_refresh=bool(args.force_refresh),
        )

        log.info(
            "provider_daily_anchor_start",
            provider=getattr(provider, "name", data_source),
            symbol=args.symbol,
            start_date=start_date,
            end_date=end_date,
            cache_dir=str(cache_dir),
        )

        try:
            daily_df = provider.fetch_daily(symbol=args.symbol, start=pd.to_datetime(start_date).date(), end=pd.to_datetime(end_date).date())
        except Exception as e:
            log.warn("provider_daily_anchor_failed_fallback_to_synthetic", error=str(e), provider=data_source)
            intraday = generate_multi_session_intraday(start_date=start_date, end_date=end_date, seed=7, base_open=10400.0)
        else:
            # Convert timestamps to London date strings for the synthetic bridge.
            dd = daily_df.copy()
            dd["timestamp"] = pd.to_datetime(dd["timestamp"], utc=True).dt.tz_convert(DEFAULT_TIMEZONE)
            dd["date"] = dd["timestamp"].dt.date.astype(str)

            # Keep only required columns for the bridge.
            dd = dd[["date", "open", "high", "low", "close", "volume"]].dropna().reset_index(drop=True)
            # Ensure within requested range
            dd = dd[(dd["date"] >= start_date) & (dd["date"] <= end_date)].reset_index(drop=True)
            if dd.empty:
                log.warn("provider_daily_anchor_empty_after_filter_fallback_to_synthetic", provider=data_source)
                intraday = generate_multi_session_intraday(start_date=start_date, end_date=end_date, seed=7, base_open=10400.0)
            else:
                intraday = generate_multi_session_intraday_from_daily(dd, seed=7)
                # Persist the daily anchor for auditability
                daily_anchor_path = V2_DATA_BRONZE_DIR / f"ftse100_daily_anchor_{data_source}.parquet"
                _ensure(daily_anchor_path)
                safe_to_parquet(dd, daily_anchor_path, index=False)
                log.info("intraday_generated", mode=f"daily_anchor:{data_source}", rows=int(intraday.shape[0]), daily_anchor_rows=int(dd.shape[0]))

    bronze_path = V2_DATA_BRONZE_DIR / "ftse100_intraday_1m_bronze.parquet"
    _ensure(bronze_path)
    safe_to_parquet(intraday, bronze_path, index=False)
    log.info("bronze_written", rows=int(intraday.shape[0]), path=str(bronze_path))

    # --------------------------------------------------------
    # 2) Silver: cleaned + enriched
    # --------------------------------------------------------
    silver = intraday.copy()
    silver["timestamp"] = pd.to_datetime(silver["timestamp"])
    silver = silver.sort_values(["date", "timestamp"]).reset_index(drop=True)
    silver["return_1m"] = silver.groupby("date")["close"].pct_change().fillna(0.0)
    silver["vol_20m"] = silver.groupby("date")["return_1m"].rolling(20).std().reset_index(level=0, drop=True)

    silver_path = V2_DATA_SILVER_DIR / "ftse100_intraday_1m_silver.parquet"
    _ensure(silver_path)
    safe_to_parquet(silver, silver_path, index=False)
    log.info("silver_written", rows=int(silver.shape[0]), path=str(silver_path))

    # --------------------------------------------------------
    # 3) Gold: daily aggregates + risk measures
    # --------------------------------------------------------
    daily = (
        silver.groupby("date")
        .agg(
            open=("open", "first"),
            high=("high", "max"),
            low=("low", "min"),
            close=("close", "last"),
            volume=("volume", "sum"),
        )
        .reset_index()
    )
    daily["timestamp"] = pd.to_datetime(daily["date"])
    daily = daily.sort_values("date").reset_index(drop=True)
    daily["daily_return"] = daily["close"].pct_change().fillna(0.0)
    daily["rolling_vol_20"] = daily["daily_return"].rolling(20).std() * np.sqrt(252)
    daily["cummax"] = daily["close"].cummax()
    daily["drawdown_pct"] = (daily["close"] / daily["cummax"] - 1.0) * 100.0
    daily["momentum_10d_pct"] = daily["close"].pct_change(10) * 100.0
    daily["rsi_14"] = compute_rsi(daily["close"], window=14)

    gold_daily_path = V2_DATA_GOLD_DIR / "ftse100_daily_gold.parquet"
    _ensure(gold_daily_path)
    safe_to_parquet(daily, gold_daily_path, index=False)
    # Also ship a CSV for quick preview / GitHub rendering
    daily.to_csv(V2_DATA_GOLD_DIR / "ftse100_daily_gold.csv", index=False)
    log.info("gold_daily_written", rows=int(daily.shape[0]), path=str(gold_daily_path))

    # --------------------------------------------------------
    # 4) Constituents + sectors (gold)
    # --------------------------------------------------------
    universe = load_ftse100_universe(source=args.constituents_source, weight_method=args.weights_method, seed=7)
    constituents = simulate_constituent_daily(daily_index=daily[["date", "close"]], universe=universe, seed=11)

    sector_daily = (
        constituents.groupby(["date", "sector"]).apply(lambda g: np.average(g["return"], weights=g["index_weight"])).reset_index(name="sector_return")
    )
    sector_pivot = sector_daily.pivot(index="date", columns="sector", values="sector_return").fillna(0.0)
    sector_corr = sector_pivot.corr()

    gold_universe_path = V2_DATA_GOLD_DIR / "ftse100_constituent_universe.parquet"
    _ensure(gold_universe_path)
    safe_to_parquet(universe, gold_universe_path, index=False)
    universe.to_csv(V2_DATA_GOLD_DIR / "ftse100_constituent_universe.csv", index=False)

    gold_const_path = V2_DATA_GOLD_DIR / "ftse100_constituents_daily.parquet"
    _ensure(gold_const_path)
    safe_to_parquet(constituents, gold_const_path, index=False)
    constituents.to_csv(V2_DATA_GOLD_DIR / "ftse100_constituents_daily.csv", index=False)

    gold_sector_path = V2_DATA_GOLD_DIR / "ftse100_sector_returns_daily.parquet"
    _ensure(gold_sector_path)
    safe_to_parquet(sector_daily, gold_sector_path, index=False)
    sector_daily.to_csv(V2_DATA_GOLD_DIR / "ftse100_sector_returns_daily.csv", index=False)

    log.info("gold_constituents_written", rows=int(constituents.shape[0]))

    # --------------------------------------------------------
    # 4b) Events calendar enrichment (gold)
    # --------------------------------------------------------
    events_calendar = build_events_calendar(
        start_date=start_date,
        end_date=end_date,
        universe_tickers=universe["ticker"].tolist(),
        include_news=bool(getattr(args, "include_news", False)),
        tz=DEFAULT_TIMEZONE,
    )
    events_path = V2_DATA_GOLD_DIR / "events_calendar.parquet"
    _ensure(events_path)
    safe_to_parquet(events_calendar, events_path, index=False)
    events_calendar.to_csv(V2_DATA_GOLD_DIR / "events_calendar.csv", index=False)
    log.info("events_calendar_written", rows=int(events_calendar.shape[0]), path=str(events_path))

    # --------------------------------------------------------
    # 5) Monitoring artifacts (DQ + drift + pipeline ops mock)
    # --------------------------------------------------------
    latest_date = daily["date"].iloc[-1]
    latest_intraday = silver[silver["date"] == latest_date].copy()

    dq_checks = run_dq_checks(latest_intraday[["timestamp", "open", "high", "low", "close", "volume"]].rename(columns={"timestamp": "timestamp"}))
    dq_df = dq_summary_table(dq_checks)
    dq_status = overall_status(dq_checks)

    _ensure(V2_MONITORING_DIR / "reports" / "dq_latest_session.csv")
    dq_df.to_csv(V2_MONITORING_DIR / "reports" / "dq_latest_session.csv", index=False)
    write_json(V2_MONITORING_DIR / "reports" / "dq_latest_session_status.json", {"run_id": run_id, "date": latest_date, "status": dq_status})

    # Drift: compare last 20 days vs previous 20 days on daily_return distribution
    last20 = daily["daily_return"].tail(20)
    prev20 = daily["daily_return"].tail(40).head(20)
    drift = {
        "mean_last20": float(last20.mean()),
        "mean_prev20": float(prev20.mean()),
        "std_last20": float(last20.std()),
        "std_prev20": float(prev20.std()),
        "mean_shift": float(last20.mean() - prev20.mean()),
        "std_shift": float(last20.std() - prev20.std()),
    }
    write_json(V2_MONITORING_DIR / "reports" / "return_drift_last20_vs_prev20.json", {"run_id": run_id, "as_of": latest_date, **drift})

    # Pipeline ops mock: 3 jobs x last 14 days
    rng = np.random.default_rng(99)
    jobs = ["bronze_ingest", "silver_transform", "gold_publish"]
    days = pd.date_range(end=pd.to_datetime(latest_date), periods=14, freq="D")
    ops = []
    for day in days:
        for job in jobs:
            status = "SUCCESS" if rng.random() > 0.08 else "FAIL"
            duration = float(abs(rng.normal(180.0, 45.0)))
            ops.append({"date": day.strftime("%Y-%m-%d"), "job": job, "status": status, "duration_sec": round(duration, 1)})
    ops_df = pd.DataFrame(ops)
    ops_df.to_csv(V2_MONITORING_DIR / "reports" / "pipeline_runs_last14d.csv", index=False)

    # Latency SLA mock
    latency = pd.DataFrame({"ts": pd.date_range(end=pd.to_datetime(latest_date), periods=200, freq="H"), "latency_ms": np.abs(rng.normal(850.0, 220.0, size=200))})
    latency.to_csv(V2_MONITORING_DIR / "reports" / "latency_samples.csv", index=False)

    # Incident timeline (mock register for monitoring realism)
    days = pd.date_range(end=pd.to_datetime(latest_date), periods=14, freq="D")
    incidents = pd.DataFrame(
        [
            {"start": days[-12].strftime("%Y-%m-%d"), "end": days[-12].strftime("%Y-%m-%d"), "incident": "Bronze ingest retry", "severity": "low"},
            {"start": days[-7].strftime("%Y-%m-%d"), "end": days[-6].strftime("%Y-%m-%d"), "incident": "Vendor API latency", "severity": "medium"},
            {"start": days[-3].strftime("%Y-%m-%d"), "end": days[-3].strftime("%Y-%m-%d"), "incident": "DQ fail: duplicate timestamps", "severity": "high"},
        ]
    )
    incidents.to_csv(V2_MONITORING_DIR / "reports" / "incident_timeline.csv", index=False)

    # Model metrics timeseries (monitoring)
    rng_mon = np.random.default_rng(202)
    model_metrics_timeseries = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=pd.to_datetime(latest_date), periods=len(daily), freq="D"),
            "rmse": np.abs(rng_mon.normal(0.0, 1.0, size=len(daily))) + np.linspace(0.0, 2.5, len(daily)),
            "mae": np.abs(rng_mon.normal(0.0, 0.8, size=len(daily))) + np.linspace(0.0, 3.0, len(daily)),
        }
    )
    model_metrics_timeseries.to_csv(V2_MONITORING_DIR / "reports" / "model_metrics_timeseries.csv", index=False)

    log.info("monitoring_written", dq_status=dq_status)

    # --------------------------------------------------------
    # 6) Curated marts + DuckDB local warehouse (terminal realism)
    # --------------------------------------------------------
    # V2 page specs mandate dashboards read from `mart.*` tables.
    # We therefore materialise all mart tables referenced by the spec pack, and
    # also populate a local DuckDB warehouse for the "modern platform" feel.
    import re
    import yaml

    marts_finished_at = datetime.utcnow()

    # Build a lightweight page index (used by mart usage-maps)
    pages_dir = REPO_ROOT / "docs" / "dashboards" / "V2" / "pages"
    pages = []
    for md in sorted(pages_dir.glob("*.md")):
        txt = md.read_text(encoding="utf-8")
        meta = {}
        if txt.startswith("---"):
            try:
                meta = yaml.safe_load(txt.split("---", 2)[1]) or {}
            except Exception:
                meta = {}
        uses = sorted(set(re.findall(r"mart\.[a-zA-Z0-9_]+", txt)))
        pages.append(
            {
                "page_id": meta.get("page_id", md.stem),
                "page_name": meta.get("page_name", md.stem),
                "uses_marts": ",".join(uses),
            }
        )
    page_specs_df = pd.DataFrame(pages)

    # Governance tables (gold → mart passthrough)
    kpi_dictionary = pd.read_csv(V2_DATA_GOLD_DIR / "kpi_dictionary.csv")
    measure_catalogue = pd.read_csv(V2_DATA_GOLD_DIR / "measure_catalogue.csv")
    data_inventory = pd.read_csv(V2_DATA_GOLD_DIR / "data_inventory.csv")

    dq_issue_path = REPO_ROOT / "docs" / "logs" / "07_dq_issue_register.csv"
    if dq_issue_path.exists():
        dq_issue_register = pd.read_csv(dq_issue_path)
    else:
        dq_issue_register = pd.DataFrame(
            columns=["issue_id", "detected_ts_london", "check_name", "severity", "description", "status", "owner", "notes"]
        )

    # Thresholds config
    thresholds = yaml.safe_load((REPO_ROOT / "config" / "thresholds.yaml").read_text(encoding="utf-8"))

    # Build all marts
    marts = build_all_v2_marts(
        intraday_silver=silver,
        daily_gold=daily,
        constituents_daily=constituents,
        sector_returns_daily=sector_daily,
        universe=universe,
        events_calendar=events_calendar,
        dq_latest_session=dq_df,
        dq_status_json={"status": dq_status, "generated_at": marts_finished_at.isoformat(timespec="seconds")},
        dq_issue_register=dq_issue_register,
        pipeline_runs_last14d=ops_df,
        latency_samples=latency,
        incident_timeline=incidents,
        model_metrics_timeseries=model_metrics_timeseries,
        drift_report={"as_of": latest_date, **drift},
        thresholds=thresholds,
        page_specs=page_specs_df,
        kpi_dictionary=kpi_dictionary,
        measure_catalogue=measure_catalogue,
        data_inventory=data_inventory,
        run_id=run_id,
        finished_at=marts_finished_at,
    )

    # Ensure every referenced mart.* in the spec pack exists as a file.
    referenced = sorted(
        set(
            ",".join(page_specs_df["uses_marts"].fillna("").tolist()).split(",")
        )
    )
    for t in referenced:
        t = t.strip()
        if not t:
            continue
        if t not in marts:
            marts[t] = pd.DataFrame([{"run_id": run_id}])

    # Persist marts to disk (parquet + csv)
    write_marts(marts, mart_dir=V2_DATA_MART_DIR)

    # DuckDB local warehouse (populated)
    parquet_tables = {
        "bronze.ftse100_intraday_1m_bronze": V2_DATA_BRONZE_DIR / "ftse100_intraday_1m_bronze.parquet",
        "silver.ftse100_intraday_1m_silver": V2_DATA_SILVER_DIR / "ftse100_intraday_1m_silver.parquet",
        "gold.ftse100_daily_gold": V2_DATA_GOLD_DIR / "ftse100_daily_gold.parquet",
        "gold.ftse100_constituents_daily": V2_DATA_GOLD_DIR / "ftse100_constituents_daily.parquet",
        "gold.ftse100_sector_returns_daily": V2_DATA_GOLD_DIR / "ftse100_sector_returns_daily.parquet",
        "gold.ftse100_constituent_universe": V2_DATA_GOLD_DIR / "ftse100_constituent_universe.parquet",
        "gold.events_calendar": V2_DATA_GOLD_DIR / "events_calendar.parquet",
    }
    for name in marts.keys():
        fname = name.split(".", 1)[1] if name.startswith("mart.") else name
        parquet_tables[name] = V2_DATA_MART_DIR / f"{fname}.parquet"

    build_duckdb_warehouse(db_path=V2_DB_DIR / "warehouse.duckdb", parquet_tables=parquet_tables)

    (V2_DB_DIR / "README.md").write_text(
        "# Local Warehouse (DuckDB)\n\n"
        "This DuckDB file is populated during the V2 build and mirrors the platform layers:\n\n"
        "- bronze.* (raw ingest)\n"
        "- silver.* (clean/enriched)\n"
        "- gold.* (curated core tables)\n"
        "- mart.* (dashboard-ready tables)\n\n"
        "Open with DuckDB CLI / DBeaver / Python duckdb to query locally.\n"
    )

    # --------------------------------------------------------
    # 7) V2 dashboard exports (22 pages) — mart parquet only
    # --------------------------------------------------------
    # Contract: V2 pages must read ONLY from v2_modernisation_realtime/data/mart/*.parquet
    export_v2_pages_from_marts(
        mart_dir=V2_DATA_MART_DIR,
        exports_dir=DOCS_DASH_V2_EXPORTS_DIR,
        run_id=run_id,
        max_sessions_overview=10,
    )

    log.info("exports_done", count=22, exports=str(DOCS_DASH_V2_EXPORTS_DIR))
    log.info("end_v2_build", run_id=run_id)

    finished_at = datetime.utcnow()
    append_run_register(
        run_id=run_id,
        pipeline="V2",
        started_at=started_at,
        finished_at=finished_at,
        status="SUCCESS",
        data_source=str(args.data_source),
        version_tag="V2.1",
        notes="V2 modern platform build (marts + DuckDB + 22 exports)",
    )

    print(f"V2 build complete. run_id={run_id}")


if __name__ == "__main__":
    main()
