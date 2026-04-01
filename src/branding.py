"""Branding helpers for subtle attribution across visual outputs."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import matplotlib.image as mpimg

DEFAULT_BRAND_LABEL = "kobeanderson-png"


def branding_enabled(default: bool = False) -> bool:
    """Return whether branding is enabled via environment configuration."""
    raw = os.getenv("BRANDING_ENABLED")
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _resolve_logo_path(explicit_path: Optional[str] = None) -> Optional[Path]:
    """Find the first existing logo path from explicit/env/common candidates."""
    candidates = []

    if explicit_path:
        candidates.append(explicit_path)

    env_logo = os.getenv("BRAND_LOGO_PATH")
    if env_logo:
        candidates.append(env_logo)

    candidates.extend(
        [
            "kobeanderson-png",
            "kobeanderson.png",
            "assets/kobeanderson-png",
            "assets/kobeanderson.png",
        ]
    )

    for item in candidates:
        path = Path(item)
        if path.exists() and path.is_file():
            return path

    return None


def brand_label(default: str = DEFAULT_BRAND_LABEL) -> str:
    return os.getenv("BRAND_LABEL", default).strip() or default


def apply_subtle_branding(
    fig,
    label: Optional[str] = None,
    logo_path: Optional[str] = None,
    text_alpha: float = 0.025,
    logo_alpha: float = 0.035,
    enabled: Optional[bool] = None,
) -> None:
    """Apply subtle text branding and optional logo overlay to a matplotlib figure."""
    if enabled is None:
        enabled = branding_enabled(default=False)
    if not enabled:
        return

    mark = label or brand_label()

    # Keep this low-contrast so it remains non-intrusive in academic figures.
    fig.text(
        0.995,
        0.005,
        mark,
        ha="right",
        va="bottom",
        fontsize=8,
        color="#333333",
        alpha=text_alpha,
    )

    logo = _resolve_logo_path(logo_path)
    if not logo:
        return

    try:
        img = mpimg.imread(str(logo))
        dpi = fig.dpi
        width_px = int(fig.get_figwidth() * dpi)
        height_px = int(fig.get_figheight() * dpi)

        img_h, img_w = img.shape[:2]
        target_w = max(80, int(width_px * 0.12))
        scale = target_w / max(1, img_w)
        target_h = max(24, int(img_h * scale))

        # Position image in the lower-right corner with small padding.
        xo = max(0, width_px - target_w - 10)
        yo = 10

        fig.figimage(img, xo=xo, yo=yo, alpha=logo_alpha, zorder=10)
    except Exception:
        # Fall back to text-only branding if logo parsing fails.
        return
