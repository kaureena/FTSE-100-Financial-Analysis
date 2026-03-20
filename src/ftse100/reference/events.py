from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

from ftse100.config import (
    DEFAULT_TIMEZONE,
    FTSE100_EARNINGS_CALENDAR_STUB_CSV,
    MARKET_NEWS_HEADLINES_STUB_CSV,
    UK_MACRO_CALENDAR_STUB_CSV,
)


class EventsLoadError(RuntimeError):
    pass


def load_macro_calendar_stub(path: Path = UK_MACRO_CALENDAR_STUB_CSV) -> pd.DataFrame:
    """Load a UK macro calendar stub (timestamped events).

    Offline-first: the repo ships a small curated calendar to make dashboard
    overlays look like a real market terminal workflow.
    """
    path = Path(path)
    if not path.exists():
        raise EventsLoadError(f"Macro stub not found: {path}")
    df = pd.read_csv(path, parse_dates=["timestamp_local"])
    df["event_type"] = df.get("event_type", "macro")
    return df


def load_earnings_calendar_stub(path: Path = FTSE100_EARNINGS_CALENDAR_STUB_CSV) -> pd.DataFrame:
    """Load an earnings calendar stub (ticker-level events).

    Notes:
        The shipped stub focuses on the top-25 names by weight for readability
        in dashboards. For a full production calendar, connect a proper
        data vendor.
    """
    path = Path(path)
    if not path.exists():
        raise EventsLoadError(f"Earnings stub not found: {path}")
    df = pd.read_csv(path, parse_dates=["timestamp_local"])
    df["event_type"] = df.get("event_type", "earnings")
    return df


def load_news_headlines_stub(path: Path = MARKET_NEWS_HEADLINES_STUB_CSV) -> pd.DataFrame:
    """Load a small UK-market news headlines stub."""
    path = Path(path)
    if not path.exists():
        raise EventsLoadError(f"News stub not found: {path}")
    df = pd.read_csv(path, parse_dates=["timestamp_local"])
    df["event_type"] = df.get("event_type", "news")
    return df


def build_events_calendar(
    *,
    start_date: str,
    end_date: str,
    universe_tickers: Optional[Iterable[str]] = None,
    include_news: bool = False,
    tz: str = DEFAULT_TIMEZONE,
) -> pd.DataFrame:
    """Build a unified events calendar for overlays + enrichment.

    The output is intentionally simple: a single, denormalised events table
    that can be joined/filtered by date in dashboards.

    Parameters
    ----------
    start_date, end_date:
        Date range (YYYY-MM-DD) inclusive bounds.
    universe_tickers:
        Optional filter: only keep earnings events for these tickers.
    include_news:
        If True, include headline rows as event_type='news' (stub).
    tz:
        Timezone label (kept as metadata).
    """
    start_ts = pd.to_datetime(start_date)
    end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    macro = load_macro_calendar_stub()
    earnings = load_earnings_calendar_stub()

    if universe_tickers is not None:
        universe_tickers = set(universe_tickers)
        if "ticker" in earnings.columns:
            earnings = earnings[earnings["ticker"].isin(universe_tickers)].copy()

    frames = [macro, earnings]
    if include_news:
        frames.append(load_news_headlines_stub())

    events = pd.concat(frames, ignore_index=True, sort=False)
    events = events.copy()
    events["timezone"] = events.get("timezone", tz)

    # Filter to range
    if "timestamp_local" not in events.columns:
        raise EventsLoadError("events table must contain timestamp_local")
    events = events[(events["timestamp_local"] >= start_ts) & (events["timestamp_local"] <= end_ts)].copy()

    # Add date helper + stable id
    events["date"] = events["timestamp_local"].dt.strftime("%Y-%m-%d")

    # Normalise optional columns so IDs don't contain 'nan'
    if "ticker" in events.columns:
        events["ticker"] = events["ticker"].fillna("")
    else:
        events["ticker"] = ""

    # Prefer event_name; fall back to headline for news rows
    label = events["event_name"] if "event_name" in events.columns else pd.Series([""] * len(events))
    if "headline" in events.columns:
        label = label.fillna(events["headline"])
    label = label.fillna("")

    events["event_id"] = (
        events["event_type"].astype(str)
        + "|"
        + events["timestamp_local"].astype(str)
        + "|"
        + events["ticker"].astype(str)
        + "|"
        + label.astype(str)
    )

    # Canonical columns order (others retained)
    preferred = [
        "event_id",
        "event_type",
        "timestamp_local",
        "date",
        "timezone",
        "country",
        "category",
        "impact",
        "ticker",
        "company_name",
        "event_name",
        "headline",
        "sentiment",
        "is_stub",
        "source",
    ]
    cols = [c for c in preferred if c in events.columns] + [c for c in events.columns if c not in preferred]
    events = events[cols].sort_values("timestamp_local").reset_index(drop=True)
    return events
