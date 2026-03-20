"""V2 export-only script.

This script regenerates the 22 dashboard images by reading **ONLY** the
`v2_modernisation_realtime/data/mart/*.parquet` tables.

Why it exists:
- Enforces the V2 contract: dashboards are rendered from curated mart tables.
- Allows re-exporting without rebuilding bronze/silver/gold.

Outputs:
- docs/dashboards/V2/exports/*.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from ftse100.config import DOCS_DASH_V2_EXPORTS_DIR, V2_DATA_MART_DIR
from ftse100.viz.export_v2 import export_v2_pages_from_marts


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export V2 dashboard pages from mart parquet tables")
    p.add_argument("--mart-dir", default=str(V2_DATA_MART_DIR), help="Directory containing mart parquet tables")
    p.add_argument("--exports-dir", default=str(DOCS_DASH_V2_EXPORTS_DIR), help="Output directory for exports")
    p.add_argument("--run-id", default=None, help="Optional run_id to display on exports")
    p.add_argument("--overview-sessions", type=int, default=10, help="How many sessions to show on Page 01")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    export_v2_pages_from_marts(
        mart_dir=Path(args.mart_dir),
        exports_dir=Path(args.exports_dir),
        run_id=args.run_id,
        max_sessions_overview=int(args.overview_sessions),
    )
    print(f"V2 exports generated from marts → {args.exports_dir}")


if __name__ == "__main__":
    main()
