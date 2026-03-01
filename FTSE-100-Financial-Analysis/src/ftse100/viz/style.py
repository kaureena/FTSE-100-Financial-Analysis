from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt


@dataclass(frozen=True)
class NeonTheme:
    # Background / surfaces
    bg: str = "#0B0F14"
    panel: str = "#111827"
    grid: str = "#1F2937"
    text: str = "#E5E7EB"
    muted: str = "#9CA3AF"

    # UK-neon accents
    neon_cyan: str = "#22D3EE"
    neon_pink: str = "#F472B6"
    neon_green: str = "#34D399"
    neon_yellow: str = "#FBBF24"
    neon_purple: str = "#A78BFA"
    neon_red: str = "#FB7185"


THEME = NeonTheme()


def apply_theme() -> None:
    """Apply a reusable matplotlib style."""
    plt.rcParams.update(
        {
            "figure.facecolor": THEME.bg,
            "axes.facecolor": THEME.panel,
            "savefig.facecolor": THEME.bg,
            "axes.edgecolor": THEME.grid,
            "axes.labelcolor": THEME.text,
            "text.color": THEME.text,
            "xtick.color": THEME.muted,
            "ytick.color": THEME.muted,
            "grid.color": THEME.grid,
            "grid.linestyle": "-",
            "grid.alpha": 0.4,
            "font.size": 12,
            "axes.titleweight": "bold",
        }
    )
