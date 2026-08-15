# SPDX-FileCopyrightText: 2026-present Ayush Chaugule
#
# SPDX-License-Identifier: MIT
"""A small Canvas-drawn rounded button.

`ttk.Button` can be recolored via styles, but it cannot be given real rounded
corners portably (that needs either platform theme engines we don't have, or
image assets). Drawing the button ourselves on a `tk.Canvas` -- a rounded
polygon plus centered text, redrawn on hover/press/resize -- gets genuine
rounded corners with zero extra assets and no ttk style fighting, matching
Cinnamon's small `border-radius: 3px` buttons closely enough to read as
"designed" rather than stock Tkinter.
"""

from __future__ import annotations

import tkinter as tk
import tkinter.font as tkfont
from typing import Callable, Optional

from . import theme


def _rounded_rect_points(x1: float, y1: float, x2: float, y2: float, radius: float):
    """Corner points for a rounded rectangle, meant to be drawn with
    `create_polygon(..., smooth=True)`. This is the standard Tk recipe:
    smoothing treats each pair of points around a corner as control points
    for a quadratic curve, so listing the two points flanking each corner is
    enough to round it.
    """
    radius = max(0, radius)
    return [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]


class RoundedButton(tk.Canvas):
    """A button-like widget with rounded corners and Mint-Y hover/press states.

    Usage mirrors a plain callback button:

        RoundedButton(parent, text="Convert", command=fn,
                       bg=theme.ACCENT, hover_bg=theme.ACCENT_HOVER,
                       active_bg=theme.ACCENT_PRESSED, fg=theme.FG_ON_ACCENT,
                       font=("Ubuntu", 10), stretch=True).pack(fill="x")
    """

    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        command: Optional[Callable[[], None]] = None,
        *,
        bg: str,
        hover_bg: str,
        active_bg: str,
        fg: str,
        font,
        radius: int = theme.BUTTON_RADIUS,
        padx: int = theme.BUTTON_PAD_X,
        pady: int = theme.BUTTON_PAD_Y,
        stretch: bool = False,
        disabled_bg: str = theme.DISABLED_BG,
        disabled_fg: str = theme.DISABLED_FG,
        border: str = theme.BORDER,
    ) -> None:
        parent_bg = parent["bg"]
        super().__init__(parent, bg=parent_bg, highlightthickness=0, bd=0, cursor="hand2")

        self._text = text
        self._command = command
        self._bg = bg
        self._hover_bg = hover_bg
        self._active_bg = active_bg
        self._fg = fg
        self._font = font
        self._radius = radius
        self._padx = padx
        self._pady = pady
        self._stretch = stretch
        self._disabled_bg = disabled_bg
        self._disabled_fg = disabled_fg
        self._border = border
        self._enabled = True
        self._state = "normal"  # normal | hover | pressed

        measured = tkfont.Font(font=font)
        text_width = measured.measure(text)
        line_height = measured.metrics("linespace")
        self._min_width = text_width + padx * 2
        self._min_height = line_height + pady * 2

        self.configure(width=self._min_width, height=self._min_height)

        self.bind("<Configure>", self._on_configure)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

        self._draw(self._min_width, self._min_height)

    # --- internal drawing -------------------------------------------------

    def _current_colors(self):
        if not self._enabled:
            return self._disabled_bg, self._disabled_fg
        if self._state == "pressed":
            return self._active_bg, self._fg
        if self._state == "hover":
            return self._hover_bg, self._fg
        return self._bg, self._fg

    def _draw(self, width: float, height: float) -> None:
        # Real Mint-Y-Dark-Purple buttons are drawn with `border: 1px solid
        # #202023` around the fill (see gtk-dark.css). We keep that outline on
        # every state -- including disabled -- so a disabled button still
        # reads as "a button" (its shape stays legible) even when its fill is
        # deliberately muted down toward the window background.
        self.delete("all")
        fill, text_fill = self._current_colors()
        radius = min(self._radius, height / 2, width / 2)
        points = _rounded_rect_points(1, 1, width - 1, height - 1, radius)
        self.create_polygon(points, smooth=True, fill=fill, outline=self._border, width=1)
        self.create_text(
            width / 2, height / 2, text=self._text, fill=text_fill, font=self._font
        )

    def _on_configure(self, event: tk.Event) -> None:
        self._draw(event.width, event.height)

    # --- interaction --------------------------------------------------

    def _on_enter(self, _event: tk.Event) -> None:
        if self._enabled:
            self._state = "hover"
            self._draw(self.winfo_width(), self.winfo_height())

    def _on_leave(self, _event: tk.Event) -> None:
        if self._enabled:
            self._state = "normal"
            self._draw(self.winfo_width(), self.winfo_height())

    def _on_press(self, _event: tk.Event) -> None:
        if self._enabled:
            self._state = "pressed"
            self._draw(self.winfo_width(), self.winfo_height())

    def _on_release(self, event: tk.Event) -> None:
        if not self._enabled:
            return
        self._state = "hover"
        self._draw(self.winfo_width(), self.winfo_height())
        # Only fire the command if the button was released back inside the widget
        # (standard button behavior: press-and-drag-away-then-release cancels the click).
        if 0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height():
            if self._command is not None:
                self._command()

    # --- public API ---------------------------------------------------

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled
        self._state = "normal"
        self.configure(cursor="hand2" if enabled else "arrow")
        self._draw(self.winfo_width() or self._min_width, self.winfo_height() or self._min_height)


def _left_rounded_rect_points(x1: float, y1: float, x2: float, y2: float, radius: float):
    """Like _rounded_rect_points, but only the left corners are rounded --
    the right edge is square. Used for the progress bar's fill: it starts at
    the trough's rounded left edge, but its right edge is a moving boundary
    that's almost never sitting exactly at the trough's rounded right corner,
    so rounding it there would look like a stray notch rather than a corner.
    """
    radius = max(0, radius)
    return [
        x1 + radius, y1,
        x2, y1,
        x2, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]


class ProgressBar(tk.Canvas):
    """A small determinate progress bar with centered percentage text,
    styled from theme.PROGRESS_* (pulled from the real GTK theme's own
    `progressbar`/`progressbar progress` rules -- see theme.py).

    This widget only draws whatever fraction it's told to; it has no opinion
    about *why* the fraction is what it is. MarkItDown's convert() has no
    progress callback to report real progress, so app.py is the one deciding
    what fraction to show and when, including driving a simulated animation
    while a conversion is in flight.
    """

    def __init__(
        self,
        parent: tk.Widget,
        *,
        font,
        width: int = 200,
        height: int = theme.PROGRESS_BAR_HEIGHT,
        trough: str = theme.PROGRESS_TROUGH,
        fill: str = theme.PROGRESS_FILL,
        text_fill: str = theme.PROGRESS_TEXT,
        border: str = theme.BORDER,
        radius: int = theme.PROGRESS_BAR_RADIUS,
    ) -> None:
        parent_bg = parent["bg"]
        super().__init__(parent, bg=parent_bg, highlightthickness=0, bd=0)

        self._font = font
        self._trough = trough
        self._fill = fill
        self._text_fill = text_fill
        self._border = border
        self._radius = radius
        self._fraction = 0.0
        self._show_text = False
        self._min_width = width
        self._min_height = height

        self.configure(width=width, height=height)
        self.bind("<Configure>", lambda event: self._draw(event.width, event.height))
        self._draw(width, height)

    def set_progress(self, fraction: float, *, show_text: bool = True) -> None:
        """Set the fill to `fraction` (clamped 0..1) and redraw immediately."""
        self._fraction = max(0.0, min(1.0, fraction))
        self._show_text = show_text
        self._draw(self.winfo_width() or self._min_width, self.winfo_height() or self._min_height)

    def _draw(self, width: float, height: float) -> None:
        self.delete("all")
        trough_radius = min(self._radius, height / 2, width / 2)
        self.create_polygon(
            _rounded_rect_points(1, 1, width - 1, height - 1, trough_radius),
            smooth=True,
            fill=self._trough,
            outline=self._border,
            width=1,
        )

        # Fill, inset slightly within the trough (matches the small margin
        # real GTK progress bars draw between the trough border and the fill).
        inset = 2
        fill_right = inset + (width - inset * 2) * self._fraction
        if fill_right > inset + 1:
            fill_radius = min(self._radius, (height - inset * 2) / 2)
            # Square right corners look right while the fill is genuinely
            # partial (it's a moving boundary, not meant to look rounded).
            # But once it's within a corner-radius of the actual right edge
            # (i.e. at/near 100%), a square corner pokes past the trough's
            # own rounded corner and reads as a stray notch -- round both
            # sides there instead, matching the trough exactly.
            if width - 1 - fill_right <= fill_radius:
                points = _rounded_rect_points(
                    inset, inset, width - inset, height - inset, fill_radius
                )
            else:
                points = _left_rounded_rect_points(
                    inset, inset, fill_right, height - inset, fill_radius
                )
            self.create_polygon(
                points,
                smooth=True,
                fill=self._fill,
                outline=self._fill,
            )

        if self._show_text:
            self.create_text(
                width / 2,
                height / 2,
                text=f"{round(self._fraction * 100)}%",
                fill=self._text_fill,
                font=self._font,
            )
