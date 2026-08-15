# SPDX-FileCopyrightText: 2026-present Ayush Chaugule
#
# SPDX-License-Identifier: MIT
"""Mint-Y-Dark-Purple color palette and small styling helpers.

Tkinter has no access to the real GTK/Cinnamon theme engine (GTK themes don't
apply to Tk widgets on any platform), so "matching Mint Cinnamon" here means
hand-reproducing the palette, not hooking into the live theme. To make that
reproduction accurate rather than guessed, every hex value below was read
directly out of the actual installed Cinnamon theme this app targets:

    /usr/share/themes/Mint-Y-Dark-Purple/gtk-3.0/gtk-dark.css

(`@define-color` rules for theme_bg_color, accent_color, borders, button
background, semantic colors, etc.) Mint-Y-Dark-Purple was confirmed to be a
real, shipped Mint-Y variant by checking:

    gsettings get org.cinnamon.theme name            -> 'Mint-Y-Dark-Purple'
    gsettings get org.cinnamon.desktop.interface gtk-theme -> 'Mint-Y-Dark-Purple'

If you retheme this app to a different Mint-Y variant later (e.g. the default
green), pull the same @define-color values from that variant's gtk-dark.css
and update the constants below -- the rest of the app only ever imports names
from this module, never raw hex codes.
"""

from __future__ import annotations

# --- Core palette (straight from Mint-Y-Dark-Purple's gtk-dark.css) --------

BG_WINDOW = "#2e2e33"  # theme_bg_color / theme_base_color
BG_TITLEBAR = "#222226"  # wm_bg -- used for our in-window "header" strip
BG_BUTTON = "#333338"  # default (non-accent) button background
BG_SURFACE = "#333339"  # insensitive_bg_color -- used as a raised panel/card bg
BORDER = "#202023"  # borders

FG_PRIMARY = "#e4e4e4"  # theme_fg_color (rgba(255,255,255,.87) flattened over BG_WINDOW)
FG_SECONDARY = "#a8a8a8"  # placeholder_text_color -- muted/help text
FG_ON_ACCENT = "#ffffff"  # theme_selected_fg_color

ACCENT = "#8c5dd9"  # accent_color / theme_selected_bg_color (Mint-Y-Purple)

SUCCESS = "#73d216"  # success_color
WARNING = "#f27835"  # warning_color
ERROR = "#fc4138"  # error_color

DISABLED_BG = "#28282c"  # slightly darker than BG_SURFACE, for disabled buttons
DISABLED_FG = "#6f6f74"

# Cinnamon/GTK buttons in this theme use a small radius and compact padding
# (button { border-radius: 3px; padding: 5px 8px; min-height: 22px; }).
# We go slightly larger than the literal GTK values because Tk fonts render
# a bit taller than GTK's, and this is a *small* fixed window where a couple
# of extra px of breathing room reads as "designed" rather than "cramped".
BUTTON_RADIUS = 8
BUTTON_PAD_X = 16
BUTTON_PAD_Y = 6

# Cinnamon's own default UI font on this system (gsettings
# org.cinnamon.desktop.interface font-name -> 'Ubuntu 10'). Falls back
# gracefully via FONT_FALLBACKS if "Ubuntu" isn't installed (e.g. when this
# app runs on a non-Mint machine).
FONT_FAMILY_PRIMARY = "Ubuntu"
FONT_FALLBACKS = ("Noto Sans", "DejaVu Sans", "Helvetica")

FONT_SIZE_TITLE = 15
FONT_SIZE_BODY = 10
FONT_SIZE_SMALL = 9

# Progress bar -- values pulled from the real theme CSS the same way as the
# rest of this file, not reused/approximated from other widgets:
#   progressbar trough { border: 1px solid #202023; border-radius: 2px;
#                         background-color: #222226; }
#   progressbar progress { background-color: #8c5dd9; border-radius: 0px; }
# So the trough is literally BG_TITLEBAR (#222226 = wm_bg, already defined
# above) and the fill is literally ACCENT -- GTK's own progress bar uses the
# exact same accent purple as everything else in this theme. GTK's radius is
# a near-flat 2px; we go a little rounder (matching the same stylization
# ratio as BUTTON_RADIUS vs GTK's real 3px button radius) so it still reads
# as intentionally-rounded at this widget's small size, not just square.
PROGRESS_BAR_HEIGHT = 20
PROGRESS_BAR_RADIUS = 6
PROGRESS_TROUGH = BG_TITLEBAR
PROGRESS_FILL = ACCENT
PROGRESS_TEXT = FG_ON_ACCENT


def resolve_font_family(tk_root) -> str:
    """Return FONT_FAMILY_PRIMARY if it's actually installed on this system,
    otherwise the first available fallback. Keeps the app looking right on
    Mint (where Ubuntu is present) without breaking on other distros/CI.
    """
    import tkinter.font as tkfont

    available = set(tkfont.families(tk_root))
    for candidate in (FONT_FAMILY_PRIMARY,) + FONT_FALLBACKS:
        if candidate in available:
            return candidate
    return "TkDefaultFont"


def _clamp(value: int) -> int:
    return max(0, min(255, value))


def _hex_to_rgb(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*(_clamp(c) for c in rgb))


def lighten(color: str, amount: float) -> str:
    """Blend `color` toward white by `amount` (0..1). Used for hover states."""
    r, g, b = _hex_to_rgb(color)
    return _rgb_to_hex(
        (
            round(r + (255 - r) * amount),
            round(g + (255 - g) * amount),
            round(b + (255 - b) * amount),
        )
    )


def darken(color: str, amount: float) -> str:
    """Blend `color` toward black by `amount` (0..1). Used for pressed states."""
    r, g, b = _hex_to_rgb(color)
    return _rgb_to_hex(
        (
            round(r * (1 - amount)),
            round(g * (1 - amount)),
            round(b * (1 - amount)),
        )
    )


# Derived interaction states for the accent (primary) button.
ACCENT_HOVER = lighten(ACCENT, 0.12)
ACCENT_PRESSED = darken(ACCENT, 0.15)

# Derived interaction states for the plain (secondary) button.
BUTTON_HOVER = lighten(BG_BUTTON, 0.15)
BUTTON_PRESSED = darken(BG_BUTTON, 0.10)
