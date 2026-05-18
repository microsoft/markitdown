"""Progress tracking for MarkItDown conversions.

This module provides progress callback capabilities for long-running conversions.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional, List
from threading import Lock


class ConversionPhase(str, Enum):
    """Phase of the conversion process."""

    DETECTING = "detecting"  # Detecting file type
    CONVERTING = "converting"  # Converting content
    EXTRACTING_IMAGES = "extracting_images"  # Extracting embedded images
    OCR = "ocr"  # OCR processing
    FINALIZING = "finalizing"  # Finalizing markdown output


@dataclass
class ConversionProgress:
    """Progress information for a conversion."""

    phase: ConversionPhase
    current: int
    total: int
    message: str = ""
    file_path: Optional[str] = None

    @property
    def percentage(self) -> float:
        """Get progress percentage (0-100)."""
        if self.total <= 0:
            return 0.0
        return min(100.0, (self.current / self.total) * 100)


# Type for progress callback
ProgressCallback = Callable[[ConversionProgress], None]


class ProgressTracker:
    """Tracks progress of a conversion and notifies callbacks."""

    def __init__(self, callback: Optional[ProgressCallback] = None):
        self._callback = callback
        self._lock = Lock()
        self._current_phase: Optional[ConversionPhase] = None
        self._current = 0
        self._total = 0

    def set_phase(
        self,
        phase: ConversionPhase,
        total: int = 0,
        message: str = "",
        file_path: Optional[str] = None,
    ) -> None:
        """Set the current phase of conversion."""
        with self._lock:
            self._current_phase = phase
            self._current = 0
            self._total = total
            self._notify(message, file_path)

    def update(self, current: int, message: str = "") -> None:
        """Update current progress within a phase."""
        with self._lock:
            self._current = current
            self._notify(message)

    def increment(self, by: int = 1, message: str = "") -> None:
        """Increment current progress."""
        with self._lock:
            self._current += by
            self._notify(message)

    def _notify(self, message: str = "", file_path: Optional[str] = None) -> None:
        """Notify callback if set."""
        if self._callback is None:
            return

        progress = ConversionProgress(
            phase=self._current_phase or ConversionPhase.DETECTING,
            current=self._current,
            total=self._total,
            message=message,
            file_path=file_path,
        )
        try:
            self._callback(progress)
        except Exception:  # Callback error guard — must never break conversion
            pass


def create_progress_reporter(
    callback: Optional[ProgressCallback] = None,
) -> ProgressTracker:
    """Create a progress tracker with optional callback.

    Args:
        callback: Function called with progress updates

    Returns:
        ProgressTracker instance
    """
    return ProgressTracker(callback)
