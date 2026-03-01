"""Reference datasets & enrichment stubs (UK terminal realism).

This subpackage focuses on *reference* information that is not part of the raw
price time-series, but is essential for a realistic market workflow:

- FTSE 100 constituents universe (tickers, sectors, weights)
- Macro calendar (UK-centric releases / rate decisions)
- Earnings calendar (ticker-level events)
- Optional news headlines stub

The repo ships with offline snapshots under `data/reference/` so every build
runs without internet access.
"""

from .constituents import load_ftse100_universe
from .events import build_events_calendar, load_macro_calendar_stub, load_earnings_calendar_stub, load_news_headlines_stub

__all__ = [
    "load_ftse100_universe",
    "build_events_calendar",
    "load_macro_calendar_stub",
    "load_earnings_calendar_stub",
    "load_news_headlines_stub",
]
