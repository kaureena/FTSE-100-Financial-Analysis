from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import json
import pandas as pd

from ftse100.config import RUN_REGISTER_CSV
from ftse100.utils import ensure_dir


def append_run_register(
    *,
    run_id: str,
    pipeline: str,
    started_at: datetime,
    finished_at: datetime,
    status: str,
    data_source: str,
    version_tag: str,
    notes: str = "",
    extra: Optional[Dict[str, Any]] = None,
    path: Path = RUN_REGISTER_CSV,
) -> Path:
    """Append one row to the repo-wide refresh run register.

    This file is a key "production realism" artifact: it provides an audit trail
    across V1 and V2 runs (status, freshness, and what outputs were published).

    Parameters
    ----------
    run_id:
        Build run id (e.g., v2_YYYYMMDD_HHMMSS_...).
    pipeline:
        'V1' or 'V2'
    status:
        'SUCCESS' or 'FAIL'
    data_source:
        'synthetic' | 'yahoo' | ...
    version_tag:
        e.g. 'V1.1' or 'V2.1'
    extra:
        Optional dict that will be JSON-encoded into `extra_json`.
    """

    ensure_dir(path.parent)

    row = {
        "run_id": run_id,
        "pipeline": pipeline,
        "started_at": started_at.isoformat(timespec="seconds"),
        "finished_at": finished_at.isoformat(timespec="seconds"),
        "duration_sec": round((finished_at - started_at).total_seconds(), 3),
        "status": status,
        "data_source": data_source,
        "version_tag": version_tag,
        "notes": notes,
        "extra_json": json.dumps(extra or {}, separators=(',', ':'), sort_keys=True),
    }

    if path.exists():
        df = pd.read_csv(path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(path, index=False)
    return path
