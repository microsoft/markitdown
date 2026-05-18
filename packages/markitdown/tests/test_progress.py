"""Tests for the progress tracking module."""
import threading
import time
from typing import List

import pytest

from markitdown import _progress
from markitdown._progress import (
    ConversionPhase,
    ConversionProgress,
    ProgressTracker,
    ProgressCallback,
    create_progress_reporter,
)


def test_conversion_phase_has_all_phases():
    """Test that ConversionPhase has all expected phases."""
    phases = [phase.value for phase in ConversionPhase]
    assert "detecting" in phases
    assert "converting" in phases
    assert "extracting_images" in phases
    assert "ocr" in phases
    assert "finalizing" in phases


def test_conversion_progress_percentage_calculation():
    """Test that percentage is calculated correctly."""
    progress = ConversionProgress(
        phase=ConversionPhase.CONVERTING,
        current=50,
        total=100,
    )
    assert progress.percentage == 50.0

    progress.current = 100
    assert progress.percentage == 100.0

    progress.current = 150  # Over 100%
    assert progress.percentage == 100.0  # Capped at 100

    progress.total = 0
    progress.current = 50
    assert progress.percentage == 0.0  # Handle division by zero


def test_conversion_progress_with_message_and_path():
    """Test that progress can include message and file path."""
    progress = ConversionProgress(
        phase=ConversionPhase.OCR,
        current=1,
        total=3,
        message="Processing page 1",
        file_path="/path/to/file.pdf",
    )
    assert progress.message == "Processing page 1"
    assert progress.file_path == "/path/to/file.pdf"
    assert progress.phase == ConversionPhase.OCR


def test_progress_tracker_initialization():
    """Test that ProgressTracker initializes correctly."""
    tracker = ProgressTracker(callback=None)
    assert tracker._callback is None
    assert tracker._current_phase is None
    assert tracker._current == 0
    assert tracker._total == 0


def test_progress_tracker_set_phase():
    """Test that set_phase updates phase and resets progress."""
    callback_calls: List[ConversionProgress] = []

    def callback(progress: ConversionProgress) -> None:
        callback_calls.append(progress)

    tracker = ProgressTracker(callback=callback)

    # Set initial phase
    tracker.set_phase(ConversionPhase.DETECTING, total=1, message="Starting detection")

    assert len(callback_calls) == 1
    assert callback_calls[0].phase == ConversionPhase.DETECTING
    assert callback_calls[0].total == 1
    assert callback_calls[0].current == 0
    assert callback_calls[0].message == "Starting detection"

    # Change phase - should reset current to 0
    tracker.set_phase(ConversionPhase.CONVERTING, total=10, message="Now converting")

    assert len(callback_calls) == 2
    assert callback_calls[1].phase == ConversionPhase.CONVERTING
    assert callback_calls[1].current == 0
    assert callback_calls[1].total == 10


def test_progress_tracker_update():
    """Test that update updates current progress."""
    callback_calls: List[ConversionProgress] = []

    def callback(progress: ConversionProgress) -> None:
        callback_calls.append(progress)

    tracker = ProgressTracker(callback=callback)
    tracker.set_phase(ConversionPhase.CONVERTING, total=100)

    tracker.update(50, message="Halfway there")

    assert len(callback_calls) == 2  # 1 for set_phase + 1 for update
    assert callback_calls[1].current == 50
    assert callback_calls[1].message == "Halfway there"


def test_progress_tracker_increment():
    """Test that increment increases current progress."""
    callback_calls: List[ConversionProgress] = []

    def callback(progress: ConversionProgress) -> None:
        callback_calls.append(progress)

    tracker = ProgressTracker(callback=callback)
    tracker.set_phase(ConversionPhase.EXTRACTING_IMAGES, total=5)

    tracker.increment(by=1, message="First image done")
    assert callback_calls[-1].current == 1

    tracker.increment(by=2)  # Increment by 2
    assert callback_calls[-1].current == 3


def test_progress_tracker_no_callback():
    """Test that ProgressTracker works without a callback (no errors)."""
    tracker = ProgressTracker(callback=None)

    # Should not raise any exceptions
    tracker.set_phase(ConversionPhase.DETECTING, total=1)
    tracker.update(1)
    tracker.increment()


def test_progress_tracker_callback_exception():
    """Test that callback exceptions don't break conversion."""
    def bad_callback(_: ConversionProgress) -> None:
        raise RuntimeError("Callback failed!")

    tracker = ProgressTracker(callback=bad_callback)

    # Should NOT raise - callback exceptions are swallowed
    tracker.set_phase(ConversionPhase.CONVERTING, total=10)
    tracker.update(5)
    tracker.increment()


def test_create_progress_reporter():
    """Test that create_progress_reporter returns a ProgressTracker."""
    tracker = create_progress_reporter(callback=None)
    assert isinstance(tracker, ProgressTracker)


def test_callback_receives_correct_data():
    """Test that callback receives complete and correct progress data."""
    callback_data: List[ConversionProgress] = []

    def callback(progress: ConversionProgress) -> None:
        callback_data.append(progress)

    tracker = ProgressTracker(callback=callback)
    tracker.set_phase(
        ConversionPhase.OCR,
        total=10,
        message="Starting OCR",
        file_path="test.pdf",
    )

    assert len(callback_data) == 1
    data = callback_data[0]
    assert data.phase == ConversionPhase.OCR
    assert data.total == 10
    assert data.current == 0
    assert data.message == "Starting OCR"
    assert data.file_path == "test.pdf"
    assert data.percentage == 0.0


def test_thread_safety_basic():
    """Basic test that ProgressTracker with Lock doesn't crash under concurrent access."""
    callback_calls: List[ConversionProgress] = []

    def callback(progress: ConversionProgress) -> None:
        callback_calls.append(progress)

    tracker = ProgressTracker(callback=callback)
    tracker.set_phase(ConversionPhase.CONVERTING, total=1000)

    def worker(start: int, count: int):
        for i in range(count):
            tracker.update(start + i)

    threads = [
        threading.Thread(target=worker, args=(0, 100)),
        threading.Thread(target=worker, args=(100, 100)),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # At least all the updates should have been processed (some may overwrite)
    # We can't guarantee order due to concurrency, but we can verify no crashes
    assert len(callback_calls) > 0  # Some updates got through


def test_phase_enum_is_string_subclass():
    """Test that ConversionPhase is a str enum (can be used as string)."""
    phase = ConversionPhase.DETECTING
    # The enum can be compared directly to strings
    assert phase == "detecting"
    # And the value is a string
    assert isinstance(phase.value, str)
    assert phase.value == "detecting"


def test_progress_callback_type():
    """Test that ProgressCallback is properly typed."""
    # Just verify the type exists and is callable
    def my_callback(_: ConversionProgress) -> None:
        pass

    # This should type-check
    callback: ProgressCallback = my_callback
    assert callable(callback)
