"""Central configuration for the FTSE-100-Financial-Analysis repo.

The repo is designed to be *portfolio-first*: it ships with cached datasets so
all dashboards/export notebooks run offline, while still including optional
code hooks for live refresh outside this sandbox.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

DEFAULT_TIMEZONE = "Europe/London"
LONDON_SESSION_START = "08:00"
LONDON_SESSION_END = "16:30"

CURRENCY = "GBP"
INDEX_NAME = "FTSE 100"
INDEX_SYMBOL_PRIMARY = "^FTSE"   # Yahoo Finance symbol (for optional live pulls)
INDEX_SYMBOL_STOOQ = "^UKX"      # Stooq symbol often used for UK100 / Footsie views

# V1 baseline parameters (as described in the dissertation)
V1_SESSION_DATE = "2026-02-13"
V1_INTRADAY_FREQ = "1min"
V1_FORECAST_HORIZON_STEPS = 10
V1_LSTM_LOOKBACK = 60
V1_ARIMA_ORDER: Tuple[int, int, int] = (5, 1, 0)

REPO_ROOT = Path(__file__).resolve().parents[2]

# Global cache root for optional provider pulls.
# (The repo ships with offline snapshots; this cache is for *live refresh*.)
DATA_CACHE_DIR = REPO_ROOT / "data_cache"


# Reference data (portfolio-shipped, updateable)
# These files provide a realistic FTSE 100 "universe" and a UK macro/events stub
# used to enrich the dashboards with terminal-like context.
REFERENCE_DATA_DIR = REPO_ROOT / "data" / "reference"

FTSE100_UNIVERSE_SNAPSHOT_CSV = REFERENCE_DATA_DIR / "ftse100_constituents_universe_snapshot.csv"
UK_MACRO_CALENDAR_STUB_CSV = REFERENCE_DATA_DIR / "uk_macro_calendar_stub.csv"
FTSE100_EARNINGS_CALENDAR_STUB_CSV = REFERENCE_DATA_DIR / "ftse100_earnings_calendar_stub_top25.csv"
MARKET_NEWS_HEADLINES_STUB_CSV = REFERENCE_DATA_DIR / "market_news_headlines_stub.csv"


V1_ROOT = REPO_ROOT / "v1_dissertation_baseline"
V2_ROOT = REPO_ROOT / "v2_modernisation_realtime"

V1_DATA_RAW_DIR = V1_ROOT / "data" / "raw"
V1_DATA_PROCESSED_DIR = V1_ROOT / "data" / "processed"
V1_DATA_SNAPSHOTS_DIR = V1_ROOT / "data" / "snapshots"

V1_OUTPUTS_DIR = V1_ROOT / "outputs"
V1_FIGURES_DIR = V1_OUTPUTS_DIR / "figures"
V1_FORECASTS_DIR = V1_OUTPUTS_DIR / "forecasts"
V1_METRICS_DIR = V1_OUTPUTS_DIR / "metrics"
V1_TABLES_DIR = V1_OUTPUTS_DIR / "tables"
V1_LOGS_DIR = V1_ROOT / "logs"

V2_DATA_BRONZE_DIR = V2_ROOT / "data" / "bronze"
V2_DATA_SILVER_DIR = V2_ROOT / "data" / "silver"
V2_DATA_GOLD_DIR = V2_ROOT / "data" / "gold"
V2_DATA_MART_DIR = V2_ROOT / "data" / "mart"
V2_DB_DIR = V2_ROOT / "db"
V2_OUTPUTS_DIR = V2_ROOT / "outputs"
V2_FIGURES_DIR = V2_OUTPUTS_DIR / "figures"
V2_METRICS_DIR = V2_OUTPUTS_DIR / "metrics"
V2_TABLES_DIR = V2_OUTPUTS_DIR / "tables"
V2_MONITORING_DIR = V2_ROOT / "monitoring"
V2_LOGS_DIR = V2_ROOT / "logs"

DOCS_DASH_V1_EXPORTS_DIR = REPO_ROOT / "docs" / "dashboards" / "V1" / "exports"
DOCS_DASH_V2_EXPORTS_DIR = REPO_ROOT / "docs" / "dashboards" / "V2" / "exports"

DOCS_LOGS_DIR = REPO_ROOT / "docs" / "logs"
RUN_REGISTER_CSV = DOCS_LOGS_DIR / "refresh_run_register.csv"


@dataclass(frozen=True)
class BuildContext:
    run_id: str
    tz: str = DEFAULT_TIMEZONE
    currency: str = CURRENCY
    index_name: str = INDEX_NAME
    v1_session_date: str = V1_SESSION_DATE
    intraday_freq: str = V1_INTRADAY_FREQ
    forecast_horizon: int = V1_FORECAST_HORIZON_STEPS
    lstm_lookback: int = V1_LSTM_LOOKBACK
    arima_order: Tuple[int, int, int] = V1_ARIMA_ORDER
