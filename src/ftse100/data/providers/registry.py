from __future__ import annotations

"""Provider registry + factory.

We keep provider selection simple and explicit so the repo remains
portfolio-friendly.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import requests

from .base import MarketDataProvider, ProviderMeta
from .cache import CacheConfig, CachedProvider
from .yahoo import YahooFinanceProvider
from .stooq import StooqProvider
from .alphavantage import AlphaVantageProvider
from .polygon import PolygonProvider
from .snapshot import SnapshotProvider


def list_providers() -> List[ProviderMeta]:
    return [
        SnapshotProvider().meta,
        YahooFinanceProvider().meta,
        StooqProvider().meta,
        AlphaVantageProvider(api_key="<api_key>").meta,
        PolygonProvider(api_key="<api_key>").meta,
    ]


def get_provider(
    name: str,
    *,
    api_key: Optional[str] = None,
    cache_dir: Optional[Path] = None,
    force_refresh: bool = False,
    session: Optional[requests.Session] = None,
) -> MarketDataProvider:
    """Create a provider by name.

    Parameters
    ----------
    name:
        One of: yahoo, stooq, alphavantage, polygon
    api_key:
        Used for providers that require a key.
    cache_dir:
        If provided, returns a CachedProvider wrapper.
    force_refresh:
        When caching, bypass existing cache.
    session:
        Optional requests session.
    """

    key = (name or "").strip().lower()
    if key in {"snapshot", "offline", "local"}:
        provider = SnapshotProvider()
    elif key in {"yahoo", "yf", "yfinance"}:
        provider: MarketDataProvider = YahooFinanceProvider(session=session)
    elif key in {"stooq"}:
        provider = StooqProvider(session=session)
    elif key in {"alphavantage", "alpha-vantage", "av"}:
        if not api_key:
            raise ValueError("Alpha Vantage provider requires api_key")
        provider = AlphaVantageProvider(api_key=api_key, session=session)
    elif key in {"polygon", "polygonio"}:
        if not api_key:
            raise ValueError("Polygon provider requires api_key")
        provider = PolygonProvider(api_key=api_key, session=session)
    else:
        raise ValueError(f"Unknown provider: {name}")

    if cache_dir is None:
        return provider
    return CachedProvider(provider=provider, config=CacheConfig(base_dir=cache_dir, force_refresh=force_refresh))
