from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd


@dataclass
class DQCheck:
    name: str
    passed: bool
    severity: str  # INFO/WARN/FAIL
    details: str


def run_dq_checks(df: pd.DataFrame) -> List[DQCheck]:
    d = df.sort_values("timestamp").reset_index(drop=True)
    checks: List[DQCheck] = []

    dup = int(d.duplicated(subset=["timestamp"]).sum())
    checks.append(DQCheck("no_duplicate_timestamps", dup == 0, "FAIL" if dup > 0 else "INFO", f"duplicate_timestamps={dup}"))

    mono = bool(d["timestamp"].is_monotonic_increasing)
    checks.append(DQCheck("timestamp_monotonic_increasing", mono, "FAIL" if not mono else "INFO", f"is_monotonic={mono}"))

    ts = pd.to_datetime(d["timestamp"])
    if len(ts) > 1:
        diffs = ts.diff().dropna().dt.total_seconds().values
        gaps = int(np.sum(diffs > 60.0 + 1e-9))
    else:
        gaps = 0
    checks.append(DQCheck("no_large_time_gaps", gaps == 0, "WARN" if gaps > 0 else "INFO", f"gaps_gt_60s={gaps}"))

    o = d["open"].astype(float).values
    h = d["high"].astype(float).values
    l = d["low"].astype(float).values
    c = d["close"].astype(float).values
    bad = int(np.sum((h < np.maximum(o, c)) | (l > np.minimum(o, c)) | (h < l)))
    checks.append(DQCheck("ohlc_sanity", bad == 0, "FAIL" if bad > 0 else "INFO", f"bad_rows={bad}"))

    vol = d["volume"].astype(int).values
    neg = int(np.sum(vol < 0))
    checks.append(DQCheck("volume_non_negative", neg == 0, "FAIL" if neg > 0 else "INFO", f"negative_volume_rows={neg}"))

    returns = pd.Series(c).pct_change().dropna()
    if len(returns) > 30:
        z = (returns - returns.mean()) / (returns.std() + 1e-12)
        outliers = int((np.abs(z) > 6.0).sum())
    else:
        outliers = 0
    checks.append(DQCheck("return_outliers_z_gt_6", outliers == 0, "WARN" if outliers > 0 else "INFO", f"outlier_rows={outliers}"))

    return checks


def dq_summary_table(checks: List[DQCheck]) -> pd.DataFrame:
    return pd.DataFrame([c.__dict__ for c in checks])


def overall_status(checks: List[DQCheck]) -> str:
    if any(c.severity == "FAIL" and not c.passed for c in checks):
        return "FAIL"
    if any(c.severity == "WARN" and not c.passed for c in checks):
        return "WARN"
    return "PASS"
