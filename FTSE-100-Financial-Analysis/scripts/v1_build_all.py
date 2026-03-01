"""V1 build: dissertation-baseline workflow.

Outputs
-------
Data
- v1_dissertation_baseline/data/raw/ftse100_intraday_1m_raw.csv
- v1_dissertation_baseline/data/processed/ftse100_intraday_1m_clean.parquet
- v1_dissertation_baseline/data/processed/ftse100_intraday_1m_metadata.json

Model outputs
- v1_dissertation_baseline/outputs/forecasts/arima_forecast_10m.csv
- v1_dissertation_baseline/outputs/forecasts/lstm_forecast_10m.csv
- v1_dissertation_baseline/outputs/metrics/*.json, *.csv

Dashboard exports (high-res PNG)
- docs/dashboards/V1/exports/v1_page_01_market_overview.png
...
- docs/dashboards/V1/exports/v1_page_07_data_quality_snapshot.png
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

import numpy as np
import pandas as pd

from ftse100.config import (
    DATA_CACHE_DIR,
    DEFAULT_TIMEZONE,
    DOCS_DASH_V1_EXPORTS_DIR,
    INDEX_SYMBOL_PRIMARY,
    LONDON_SESSION_END,
    LONDON_SESSION_START,
    V1_INTRADAY_FREQ,
    V1_SESSION_DATE,
    V1_DATA_PROCESSED_DIR,
    V1_DATA_RAW_DIR,
    V1_DATA_SNAPSHOTS_DIR,
    V1_FORECASTS_DIR,
    V1_LOGS_DIR,
    V1_METRICS_DIR,
    V1_TABLES_DIR,
    V1_FIGURES_DIR,
)
from ftse100.data.io import read_intraday_clean, save_intraday_snapshot, save_intraday_snapshot_from_dataframe, safe_to_parquet
from ftse100.data.synthetic import DailyOHLCV
from ftse100.data.providers.registry import get_provider
from ftse100.features import compute_session_kpis, add_returns, add_moving_averages, add_realised_vol
from ftse100.models.arima_model import fit_arima_forecast
from ftse100.models.compare import compare_metrics
from ftse100.models.forecast_format import to_contract_forecast
from ftse100.models.lstm_model import fit_lstm_forecast, integrated_gradients_importance
from ftse100.monitoring.dq import dq_summary_table, overall_status, run_dq_checks
from ftse100.monitoring import append_run_register
from ftse100.utils import SimpleLogger, make_run_id, write_json
from ftse100.viz.export_v1 import (
    export_page_01_market_overview,
    export_page_02_candles_volume,
    export_page_03_moving_averages,
    export_page_04_arima_forecast,
    export_page_05_lstm_forecast,
    export_page_06_model_comparison,
    export_page_07_dq_snapshot,
)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="V1 build (dissertation baseline): data → models → exports")
    p.add_argument(
        "--data-source",
        default=os.getenv("FTSE100_PROVIDER", "synthetic"),
        help="Data source: synthetic | yahoo | stooq | alphavantage | polygon",
    )
    p.add_argument(
        "--symbol",
        default=os.getenv("FTSE100_SYMBOL", INDEX_SYMBOL_PRIMARY),
        help="Provider-specific symbol (default is Yahoo FTSE100 index symbol).",
    )
    p.add_argument(
        "--date",
        default=os.getenv("FTSE100_V1_DATE", V1_SESSION_DATE),
        help="London session date (YYYY-MM-DD) for the V1 baseline.",
    )
    p.add_argument(
        "--interval",
        default=os.getenv("FTSE100_V1_INTERVAL", "1m"),
        help="Intraday interval for provider pulls (e.g., 1m, 5m, 15m).",
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
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    started_at = datetime.utcnow()
    run_id = make_run_id(prefix="v1")
    log = SimpleLogger(V1_LOGS_DIR / "build_v1.jsonl")
    log.info("start_v1_build", run_id=run_id)

    # ------------------------------------------------------------------
    # 1) Create reproducible intraday snapshot
    # ------------------------------------------------------------------
    raw_csv = V1_DATA_RAW_DIR / "ftse100_intraday_1m_raw.csv"
    clean_parquet = V1_DATA_PROCESSED_DIR / "ftse100_intraday_1m_clean.parquet"
    meta_json = V1_DATA_PROCESSED_DIR / "ftse100_intraday_1m_metadata.json"

    data_source = (args.data_source or "synthetic").strip().lower()
    session_date = args.date

    if data_source == "synthetic":
        # Anchored to Stooq OHLC for ^UKX (FTSE 100) on 2026-02-13.
        daily = DailyOHLCV(
            date=session_date,
            open=10402.48,
            high=10454.54,
            low=10380.87,
            close=10446.35,
            volume=660_022_612,
        )

        df = save_intraday_snapshot(daily=daily, raw_csv_path=raw_csv, clean_parquet_path=clean_parquet, metadata_path=meta_json, seed=42)
        log.info("snapshot_created", rows=int(df.shape[0]), raw=str(raw_csv), clean=str(clean_parquet), source="synthetic")
    else:
        # Live provider pull (cached). Default window is the London cash session.
        cache_dir = Path(args.cache_dir)
        start_london = pd.Timestamp(f"{session_date} {LONDON_SESSION_START}").tz_localize(DEFAULT_TIMEZONE)
        end_london = pd.Timestamp(f"{session_date} {LONDON_SESSION_END}").tz_localize(DEFAULT_TIMEZONE)

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
            "provider_pull_start",
            provider=getattr(provider, "name", data_source),
            symbol=args.symbol,
            start_london=str(start_london),
            end_london=str(end_london),
            interval=args.interval,
            cache_dir=str(cache_dir),
        )

        try:
            live = provider.fetch_intraday(symbol=args.symbol, start=start_london, end=end_london, interval=args.interval)
        except Exception as e:
            # Fall back to synthetic so the repo still runs, but surface the error.
            log.warn("provider_pull_failed_fallback_to_synthetic", error=str(e), provider=data_source)
            daily = DailyOHLCV(
                date=session_date,
                open=10402.48,
                high=10454.54,
                low=10380.87,
                close=10446.35,
                volume=660_022_612,
            )
            df = save_intraday_snapshot(daily=daily, raw_csv_path=raw_csv, clean_parquet_path=clean_parquet, metadata_path=meta_json, seed=42)
        else:
            # Convert to London time + add semantic columns used across the repo.
            d = live.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True).dt.tz_convert(DEFAULT_TIMEZONE)
            d = d.sort_values("timestamp").reset_index(drop=True)
            d["date"] = d["timestamp"].dt.date.astype(str)
            d["time"] = d["timestamp"].dt.time.astype(str)
            d["symbol"] = "FTSE100"

            # Keep only the requested London session date.
            d = d[d["date"] == session_date].reset_index(drop=True)
            df = save_intraday_snapshot_from_dataframe(
                d,
                raw_csv_path=raw_csv,
                clean_parquet_path=clean_parquet,
                metadata_path=meta_json,
                source=f"provider:{data_source}",
                source_details={
                    "provider": data_source,
                    "symbol": args.symbol,
                    "interval": args.interval,
                    "start_london": str(start_london),
                    "end_london": str(end_london),
                    "cache_dir": str(cache_dir),
                },
            )
            log.info("snapshot_created", rows=int(df.shape[0]), raw=str(raw_csv), clean=str(clean_parquet), source=f"provider:{data_source}")

    dclean = read_intraday_clean(clean_parquet)

    # ------------------------------------------------------------------
    # 2) KPIs
    # ------------------------------------------------------------------
    kpis = compute_session_kpis(dclean)
    kpis_path = V1_METRICS_DIR / "session_kpis.csv"
    kpis_path.parent.mkdir(parents=True, exist_ok=True)
    kpis.to_csv(kpis_path, index=False)
    log.info("session_kpis_written", path=str(kpis_path))

    # ------------------------------------------------------------------
    # 3) ARIMA(5,1,0)
    # ------------------------------------------------------------------
    arima_res = fit_arima_forecast(dclean, order=(5, 1, 0), horizon=10)
    arima_fc_path = V1_FORECASTS_DIR / "arima_forecast_10m.csv"
    arima_fc_path.parent.mkdir(parents=True, exist_ok=True)
    arima_res.forecast.to_csv(arima_fc_path, index=False)
    # Canonical contract output (used by docs + dashboard specs)
    origin_ts = dclean.sort_values("timestamp").iloc[-(10 + 1)]["timestamp"]
    arima_contract = to_contract_forecast(
        forecast_df=arima_res.forecast,
        model_name="ARIMA",
        origin_timestamp=origin_ts,
        run_id=run_id,
    )
    arima_contract.to_csv(V1_FORECASTS_DIR / "arima_forecast.csv", index=False)

    write_json(V1_METRICS_DIR / "arima_metrics.json", {"run_id": run_id, "model": "ARIMA", "order": arima_res.order, **arima_res.metrics})
    (V1_METRICS_DIR / "arima_model_summary.txt").write_text(arima_res.model_summary_text, encoding="utf-8")
    log.info("arima_done", **arima_res.metrics)

    # ------------------------------------------------------------------
    # 4) LSTM
    # ------------------------------------------------------------------
    lstm_res = fit_lstm_forecast(dclean, lookback=60, horizon=10, epochs=25, hidden_size=32, lr=3e-3, seed=42, return_model=True)
    lstm_fc_path = V1_FORECASTS_DIR / "lstm_forecast_10m.csv"
    lstm_res.forecast.to_csv(lstm_fc_path, index=False)
    origin_ts = dclean.sort_values("timestamp").iloc[-(10 + 1)]["timestamp"]
    lstm_contract = to_contract_forecast(
        forecast_df=lstm_res.forecast,
        model_name="LSTM",
        origin_timestamp=origin_ts,
        run_id=run_id,
    )
    lstm_contract.to_csv(V1_FORECASTS_DIR / "lstm_forecast.csv", index=False)

    lstm_res.training_history.to_csv(V1_METRICS_DIR / "lstm_training_history.csv", index=False)
    write_json(V1_METRICS_DIR / "lstm_metrics.json", {"run_id": run_id, "model": "LSTM", "lookback": lstm_res.lookback, **lstm_res.metrics})
    log.info("lstm_done", **lstm_res.metrics)

    # Integrated gradients importance for interpretability
    train_y = dclean["close"].values[:-10].astype(float)
    window_scaled = ((train_y - lstm_res.scaler_mu) / lstm_res.scaler_std)[-60:]
    importance = integrated_gradients_importance(lstm_res.model, window_scaled, steps=24) if lstm_res.model is not None else None

    # ------------------------------------------------------------------
    # 5) Model comparison
    # ------------------------------------------------------------------
    comp = compare_metrics(arima_res.metrics, lstm_res.metrics)
    comp.to_csv(V1_METRICS_DIR / "model_comparison.csv", index=False)

    # ------------------------------------------------------------------
    # 6) Data quality snapshot
    # ------------------------------------------------------------------
    checks = run_dq_checks(dclean)
    dq_table = dq_summary_table(checks)
    dq_table.to_csv(V1_METRICS_DIR / "dq_checks.csv", index=False)
    dq_status = overall_status(checks)
    write_json(V1_METRICS_DIR / "dq_status.json", {"run_id": run_id, "status": dq_status})

    # -----------------------------
    # V1 intermediate tables (portfolio realism)
    # -----------------------------
    # These tables make V1 reproducible and align with DATA_CONTRACTS + page specs.
    V1_TABLES_DIR.mkdir(parents=True, exist_ok=True)

    feat_tbl = dclean.copy()
    feat_tbl = add_returns(feat_tbl)
    feat_tbl = add_moving_averages(feat_tbl, windows=(20, 50, 100))
    feat_tbl = add_realised_vol(feat_tbl, window=20)

    safe_to_parquet(feat_tbl, V1_TABLES_DIR / "moving_average_features.parquet")
    feat_tbl.to_csv(V1_TABLES_DIR / "moving_average_features.csv", index=False)

    # Volume spike flags (simple z-score rule)
    vol = feat_tbl["volume"].astype(float)
    z = (vol - float(vol.mean())) / float(vol.std(ddof=0) or 1.0)
    vol_flags = pd.DataFrame(
        {
            "timestamp": feat_tbl["timestamp"],
            "volume": vol,
            "volume_z": z,
            "is_spike": (z >= 3.0),
        }
    )
    vol_flags.to_csv(V1_METRICS_DIR / "volume_spike_flags.csv", index=False)

    # Gap report (any gap > 60s)
    td = feat_tbl.sort_values("timestamp")
    dt_s = td["timestamp"].diff().dt.total_seconds()
    gaps = td.loc[dt_s > 60.0, ["timestamp"]].copy()
    gaps.rename(columns={"timestamp": "gap_end"}, inplace=True)
    gaps["gap_start"] = td["timestamp"].shift(1).loc[gaps.index].values
    gaps["gap_seconds"] = dt_s.loc[gaps.index].values
    gaps = gaps[["gap_start", "gap_end", "gap_seconds"]]
    gaps.to_csv(V1_METRICS_DIR / "time_gap_report.csv", index=False)

    # DQ snapshot (single JSON used by dashboards)
    dq_score = float(np.mean([c.passed for c in checks]) * 100.0)
    write_json(
        V1_METRICS_DIR / "dq_snapshot.json",
        {
            "run_id": run_id,
            "dataset": "V1 intraday 1m",
            "rows": int(len(dclean)),
            "dq_status": dq_status,
            "dq_score": dq_score,
            "volume_spike_count": int(vol_flags["is_spike"].sum()),
            "gap_count": int(len(gaps)),
        },
    )

    log.info("dq_done", status=dq_status)

    issue_register_path = REPO_ROOT / "docs" / "logs" / "07_dq_issue_register.csv"
    if not issue_register_path.exists():
        issue_register_path.write_text("issue_id,detected_ts_london,check_name,severity,description,status,owner,notes\n", encoding="utf-8")

    # ------------------------------------------------------------------
    # 7) Export dashboard pages (4K PNG)
    # ------------------------------------------------------------------
    export_page_01_market_overview(dclean, DOCS_DASH_V1_EXPORTS_DIR / "v1_page_01_market_overview.png", run_id)
    export_page_02_candles_volume(dclean, DOCS_DASH_V1_EXPORTS_DIR / "v1_page_02_candles_volume.png", run_id)
    export_page_03_moving_averages(dclean, DOCS_DASH_V1_EXPORTS_DIR / "v1_page_03_moving_averages.png", run_id)
    export_page_04_arima_forecast(dclean, arima_res.forecast, arima_res.metrics, DOCS_DASH_V1_EXPORTS_DIR / "v1_page_04_arima_forecast.png", run_id, order=arima_res.order)
    export_page_05_lstm_forecast(dclean, lstm_res.forecast, lstm_res.metrics, lstm_res.training_history, importance, DOCS_DASH_V1_EXPORTS_DIR / "v1_page_05_lstm_forecast.png", run_id)
    export_page_06_model_comparison(dclean, arima_res.forecast, lstm_res.forecast, comp, DOCS_DASH_V1_EXPORTS_DIR / "v1_page_06_model_comparison.png", run_id)
    export_page_07_dq_snapshot(dclean, DOCS_DASH_V1_EXPORTS_DIR / "v1_page_07_data_quality_snapshot.png", run_id)

    log.info("dashboard_exports_done", exports=str(DOCS_DASH_V1_EXPORTS_DIR))
    log.info("end_v1_build", run_id=run_id)

    finished_at = datetime.utcnow()
    append_run_register(
        run_id=run_id,
        pipeline="V1",
        started_at=started_at,
        finished_at=finished_at,
        status="SUCCESS",
        data_source=str(args.data_source),
        version_tag="V1.1",
        notes="V1 dissertation baseline replay (7 exports + ARIMA/LSTM)",
    )

    print(f"V1 build complete. run_id={run_id}")


if __name__ == "__main__":
    main()
