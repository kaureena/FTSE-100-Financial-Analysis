from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def make_run_id(prefix: str = "run") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    short = uuid.uuid4().hex[:8]
    return f"{prefix}_{ts}_{short}"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, obj: Any) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)


def now_london_iso() -> str:
    # (We print the timezone explicitly on dashboards.)
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class SimpleLogger:
    """Tiny file logger to make the repo feel operational."""

    log_path: Path

    def __post_init__(self) -> None:
        ensure_dir(self.log_path.parent)

    def info(self, msg: str, **kv: Any) -> None:
        self._write("INFO", msg, **kv)

    def warn(self, msg: str, **kv: Any) -> None:
        self._write("WARN", msg, **kv)

    def error(self, msg: str, **kv: Any) -> None:
        self._write("ERROR", msg, **kv)

    def _write(self, level: str, msg: str, **kv: Any) -> None:
        payload = {
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "level": level,
            "msg": msg,
            **kv,
        }
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, default=str) + "\n")
