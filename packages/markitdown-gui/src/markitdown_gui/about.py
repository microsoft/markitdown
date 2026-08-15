# SPDX-FileCopyrightText: 2026-present Ayush Chaugule
#
# SPDX-License-Identifier: MIT
"""The About dialog: a small modal Toplevel, styled to match the main window.

Implemented as a separate Toplevel rather than swapping out the main window's
content in place. Both are reasonable in Tkinter, but a Toplevel needs no
extra state machine (no "remember what to restore, then put it back"), gets
correct modal behavior and a native window-manager close button for free via
transient()/grab_set()/WM_DELETE_WINDOW, and is the conventional shape of an
"About" dialog in any desktop toolkit -- all of which makes it the one less
likely to grow subtle bugs later, which was the deciding factor over the
"cover the window" alternative.
"""

from __future__ import annotations

import tkinter as tk
import webbrowser

from . import theme
from .__about__ import APP_TITLE, __version__

# Repository URL, opened by the Source button below.
SOURCE_URL = "https://github.com/Ayush-Chaugule/gui-markitdown"

# Sized the same way as the main window: measured the packed layout's actual
# winfo_reqheight() and left a deliberate margin below it, rather than
# guessing a round number.
DIALOG_WIDTH = 360
DIALOG_HEIGHT = 330


def show_about_dialog(root: tk.Tk, *, font_title, font_body, font_small) -> None:
    """Open the About dialog as a modal child of `root`."""
    from .widgets import RoundedButton  # deferred, same reasoning as app.py

    dialog = tk.Toplevel(root)
    dialog.title("About")
    dialog.configure(bg=theme.BG_WINDOW)
    dialog.resizable(False, False)
    dialog.transient(root)  # stays on top of / minimizes with the main window

    root.update_idletasks()
    x = root.winfo_rootx() + (root.winfo_width() - DIALOG_WIDTH) // 2
    y = root.winfo_rooty() + (root.winfo_height() - DIALOG_HEIGHT) // 3
    dialog.geometry(f"{DIALOG_WIDTH}x{DIALOG_HEIGHT}+{max(0, x)}+{max(0, y)}")
    dialog.minsize(DIALOG_WIDTH, DIALOG_HEIGHT)
    dialog.maxsize(DIALOG_WIDTH, DIALOG_HEIGHT)

    outer = tk.Frame(dialog, bg=theme.BG_WINDOW)
    outer.pack(fill="both", expand=True, padx=20, pady=16)

    tk.Label(
        outer,
        text=APP_TITLE,
        font=font_title,
        bg=theme.BG_WINDOW,
        fg=theme.FG_PRIMARY,
        anchor="w",
    ).pack(fill="x")

    tk.Label(
        outer,
        text=f"Version {__version__}",
        font=font_body,
        bg=theme.BG_WINDOW,
        fg=theme.FG_SECONDARY,
        anchor="w",
    ).pack(fill="x", pady=(2, 14))

    tk.Label(
        outer,
        text=(
            "Visual theme inspired by Linux Mint Cinnamon (Mint-Y-Dark-Purple). "
            "This is an independent, personal-use project -- not affiliated with, "
            "endorsed by, or sponsored by Linux Mint or Microsoft."
        ),
        font=font_small,
        bg=theme.BG_WINDOW,
        fg=theme.FG_SECONDARY,
        justify="left",
        anchor="w",
        wraplength=DIALOG_WIDTH - 40,
    ).pack(fill="x", pady=(0, 16))

    def _open_source() -> None:
        webbrowser.open(SOURCE_URL)

    # Source gets the accent treatment (it's the notable action here, same
    # role Convert plays in the main window); Close is plain dismiss chrome
    # (same role Save Output plays -- present, but not the visual headline).
    RoundedButton(
        outer,
        text="Source",
        command=_open_source,
        bg=theme.ACCENT,
        hover_bg=theme.ACCENT_HOVER,
        active_bg=theme.ACCENT_PRESSED,
        fg=theme.FG_ON_ACCENT,
        font=font_body,
        stretch=True,
    ).pack(fill="x", pady=(0, 8))

    RoundedButton(
        outer,
        text="Close",
        command=dialog.destroy,
        bg=theme.BG_BUTTON,
        hover_bg=theme.BUTTON_HOVER,
        active_bg=theme.BUTTON_PRESSED,
        fg=theme.FG_PRIMARY,
        font=font_body,
        stretch=True,
    ).pack(fill="x")

    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
    dialog.focus_set()
    dialog.grab_set()  # modal: block interaction with the main window until closed
