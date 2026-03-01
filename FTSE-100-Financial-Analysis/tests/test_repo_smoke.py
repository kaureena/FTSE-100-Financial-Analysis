from __future__ import annotations

from pathlib import Path

import pandas as pd
from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_v1_forecast_contract_files_exist() -> None:
    p = REPO_ROOT / "v1_dissertation_baseline" / "outputs" / "forecasts"
    assert (p / "arima_forecast.csv").exists()
    assert (p / "lstm_forecast.csv").exists()


def test_v1_forecast_contract_schema() -> None:
    p = REPO_ROOT / "v1_dissertation_baseline" / "outputs" / "forecasts" / "arima_forecast.csv"
    df = pd.read_csv(p)

    expected = {
        "run_id",
        "model_name",
        "origin_timestamp",
        "target_timestamp",
        "horizon_step",
        "horizon_unit",
        "y_true",
        "yhat",
        "residual",
    }
    assert expected.issubset(set(df.columns))


def test_v2_marts_exist_for_all_spec_references() -> None:
    pages_dir = REPO_ROOT / "docs" / "dashboards" / "V2" / "pages"
    mart_dir = REPO_ROOT / "v2_modernisation_realtime" / "data" / "mart"

    assert pages_dir.exists()
    assert mart_dir.exists()

    import re

    referenced = set()
    for md in pages_dir.glob("*.md"):
        txt = md.read_text(encoding="utf-8")
        referenced |= set(re.findall(r"mart\.[A-Za-z0-9_]+", txt))

    # sanity: at least a handful
    assert len(referenced) >= 10

    for t in referenced:
        name = t.split(".", 1)[1]
        assert (mart_dir / f"{name}.parquet").exists()


def test_exports_are_4k() -> None:
    v1 = REPO_ROOT / "docs" / "dashboards" / "V1" / "exports"
    v2 = REPO_ROOT / "docs" / "dashboards" / "V2" / "exports"

    for folder in [v1, v2]:
        imgs = sorted(folder.glob("*.png"))
        assert imgs, f"no exports in {folder}"
        img = Image.open(imgs[0])
        assert img.size == (3840, 2160)
