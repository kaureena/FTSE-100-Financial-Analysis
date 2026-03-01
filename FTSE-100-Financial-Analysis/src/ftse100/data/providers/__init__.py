"""Pluggable market data providers + caching.

This repo is **offline-first** (ships with cached snapshots), but the dissertation
workflow is explicitly based on pulling FTSE100 data from online sources
(e.g., Yahoo Finance).  To make the repo feel *real* and *refreshable*, we ship a
provider interface and optional connectors:

- Yahoo Finance (no API key)
- Stooq (daily CSV, no API key)
- Alpha Vantage (API key)
- Polygon.io (API key)

The build scripts default to `synthetic` mode so they run anywhere. You can
switch to live mode via CLI flags:

    python scripts/v1_build_all.py --data-source yahoo

Caching is handled in :mod:`ftse100.data.providers.cache`.
"""

from .registry import get_provider, list_providers

__all__ = ["get_provider", "list_providers"]
