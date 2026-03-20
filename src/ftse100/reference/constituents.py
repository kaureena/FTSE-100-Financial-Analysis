from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Literal, Optional

import numpy as np
import pandas as pd

from ftse100.config import FTSE100_UNIVERSE_SNAPSHOT_CSV


class UniverseLoadError(RuntimeError):
    pass


_TICKER_RE = re.compile(r"^[A-Z0-9]{1,6}(?:-[A-Z0-9]+)?$")


def epic_to_yahoo(epic: str) -> str:
    """Convert a London Stock Exchange EPIC (as seen on Wikipedia) to a Yahoo-style ticker.

    Examples:
        - "AZN"   -> "AZN.L"
        - "BT-A"  -> "BT.A.L"

    Notes:
        This is a *best-effort* conversion. In real production you would use a
        proper symbology service (OpenFIGI, Refinitiv, Bloomberg, etc.).
    """
    epic = (epic or "").strip().upper()
    if not epic:
        raise ValueError("Empty EPIC")
    return epic.replace("-", ".") + ".L"


def _icb_to_broad_sector(icb_sector: str) -> str:
    """Map ICB-ish sector labels into a compact 10-sector palette used by dashboards."""
    s = (icb_sector or "").strip().lower()

    # Financials
    if any(k in s for k in ["bank", "financial", "insurance", "investment trust", "collective investments"]):
        return "Financials"
    # Real estate
    if "real estate" in s:
        return "Real Estate"
    # Energy
    if "oil" in s or "gas" in s:
        return "Energy"
    # Utilities
    if "utilities" in s or "electric" in s:
        return "Utilities"
    # Health care
    if "pharmaceutical" in s or "health care" in s:
        return "Health Care"
    # Technology
    if "software" in s or "electronic equipment" in s:
        return "Technology"
    # Comms
    if "telecommunication" in s or "media" in s:
        return "Communication Services"
    # Consumer staples
    if any(k in s for k in ["food", "beverage", "tobacco"]):
        return "Consumer Staples"
    # Consumer discretionary
    if any(k in s for k in ["travel", "leisure", "retail", "personal goods", "household goods", "homebuilding"]):
        return "Consumer Discretionary"
    # Materials
    if any(k in s for k in ["mining", "metals", "chemic", "containers", "packaging", "precious"]):
        return "Materials"

    return "Industrials"


def validate_universe(df: pd.DataFrame) -> None:
    required = {"company_name", "epic", "ticker", "sector", "icb_sector", "index_weight"}
    missing = required - set(df.columns)
    if missing:
        raise UniverseLoadError(f"Universe missing required columns: {sorted(missing)}")

    if df["ticker"].isna().any():
        raise UniverseLoadError("Universe contains null tickers")
    if df["ticker"].duplicated().any():
        dups = df[df["ticker"].duplicated()]["ticker"].unique().tolist()
        raise UniverseLoadError(f"Universe contains duplicate tickers: {dups[:10]}")

    w = pd.to_numeric(df["index_weight"], errors="coerce")
    if w.isna().any():
        raise UniverseLoadError("Universe contains non-numeric weights")
    s = float(w.sum())
    if not (0.99 <= s <= 1.01):
        raise UniverseLoadError(f"Universe weights must sum to 1.0 (±1%), got {s:.6f}")


def load_universe_snapshot(path: Path = FTSE100_UNIVERSE_SNAPSHOT_CSV) -> pd.DataFrame:
    if not Path(path).exists():
        raise UniverseLoadError(f"Snapshot not found: {path}")
    df = pd.read_csv(path)
    # Normalise expected columns
    if "ticker" not in df.columns and "epic" in df.columns:
        df["ticker"] = df["epic"].astype(str).map(epic_to_yahoo)
    if "sector" not in df.columns and "icb_sector" in df.columns:
        df["sector"] = df["icb_sector"].astype(str).map(_icb_to_broad_sector)

    validate_universe(df)
    return df


def _make_synthetic_universe(n: int = 100, seed: int = 7) -> pd.DataFrame:
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

    df = pd.DataFrame(
        {
            "company_name": [f"Synthetic Co {i:03d}" for i in range(1, n + 1)],
            "epic": [f"SYN{i:03d}" for i in range(1, n + 1)],
            "ticker": tickers,
            "icb_sector": sector_assign,
            "sector": sector_assign,
            "index_weight": weights,
            "as_of_date": pd.Timestamp.today().strftime("%Y-%m-%d"),
            "source": "synthetic",
        }
    )
    validate_universe(df)
    return df


def load_ftse100_universe(
    source: Literal["snapshot", "synthetic", "wikipedia"] = "snapshot",
    *,
    snapshot_path: Path = FTSE100_UNIVERSE_SNAPSHOT_CSV,
    weight_method: Literal["snapshot", "equal"] = "snapshot",
    seed: int = 7,
) -> pd.DataFrame:
    """Load an FTSE 100 constituents universe (tickers, sectors, weights).

    Parameters
    ----------
    source:
        - "snapshot": load the repo-shipped snapshot CSV (offline-first).
        - "synthetic": generate a fully synthetic universe (useful for tests).
        - "wikipedia": attempt to scrape Wikipedia for constituents (best-effort).
          If this path fails (missing deps / network), fall back to snapshot.
    weight_method:
        - "snapshot": use whatever weights exist in the loaded dataset.
        - "equal": override weights to equal-weight.
    """
    source = (source or "snapshot").strip().lower()

    if source == "synthetic":
        df = _make_synthetic_universe(n=100, seed=seed)
    elif source == "wikipedia":
        try:
            df = fetch_universe_from_wikipedia()
        except Exception:
            # Offline-first fallback
            df = load_universe_snapshot(snapshot_path)
    else:
        df = load_universe_snapshot(snapshot_path)

    if weight_method == "equal":
        df = df.copy()
        df["index_weight"] = 1.0 / len(df)

    # Revalidate after changes
    validate_universe(df)
    return df


def fetch_universe_from_wikipedia(
    url: str = "https://en.wikipedia.org/wiki/FTSE_100_Index",
) -> pd.DataFrame:
    """Scrape the FTSE 100 constituents table from Wikipedia (best-effort).

    This helper is provided as an *optional* refresh path for users outside the
    sandbox. It is not used during offline CI/builds.

    Returns
    -------
    DataFrame with columns:
        company_name, epic, ticker, icb_sector, sector, index_weight (equal-weight)
    """
    import requests

    html = requests.get(url, timeout=30).text
    tables = pd.read_html(html)

    target = None
    for t in tables:
        cols = [str(c).strip().lower() for c in t.columns]
        if "company" in cols and "ticker" in cols:
            target = t
            break

    if target is None:
        raise UniverseLoadError("Could not locate constituents table on Wikipedia page")

    # Normalise column names
    target.columns = [str(c).strip().lower() for c in target.columns]
    company_col = "company"
    ticker_col = "ticker"

    # This column name appears on Wikipedia (can change; this is best-effort)
    sector_col = None
    for c in target.columns:
        if "sector" in c:
            sector_col = c
            break
    if sector_col is None:
        raise UniverseLoadError("Could not locate sector column in Wikipedia table")

    df = pd.DataFrame(
        {
            "company_name": target[company_col].astype(str).str.strip(),
            "epic": target[ticker_col].astype(str).str.strip().str.upper(),
            "icb_sector": target[sector_col].astype(str).str.strip(),
        }
    )

    # Filter obvious noise rows
    df = df[df["epic"].map(lambda x: bool(_TICKER_RE.match(str(x))))].copy()
    df["ticker"] = df["epic"].map(epic_to_yahoo)
    df["sector"] = df["icb_sector"].map(_icb_to_broad_sector)
    df["index_weight"] = 1.0 / len(df)
    df["as_of_date"] = pd.Timestamp.today().strftime("%Y-%m-%d")
    df["source"] = "wikipedia_scrape"

    validate_universe(df)
    return df
