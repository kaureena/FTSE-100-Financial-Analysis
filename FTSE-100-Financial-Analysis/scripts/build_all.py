"""Convenience runner: build V1 then V2."""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    subprocess.check_call(["python", str(REPO_ROOT / "scripts" / "v1_build_all.py")])
    subprocess.check_call(["python", str(REPO_ROOT / "scripts" / "v2_build_all.py")])


if __name__ == "__main__":
    main()
