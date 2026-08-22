import os
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PyQt6")

from PyQt6.QtCore import QEventLoop, QTimer
from PyQt6.QtWidgets import QApplication, QMessageBox

import markitdown._qt_gui as qt_gui


@pytest.fixture(scope="module")
def qt_app():
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def message_boxes(monkeypatch):
    messages = []

    def record_information(_parent, title, message):
        messages.append(("information", title, message))

    def record_warning(_parent, title, message):
        messages.append(("warning", title, message))

    monkeypatch.setattr(QMessageBox, "information", record_information)
    monkeypatch.setattr(QMessageBox, "warning", record_warning)
    return messages


def _wait_for_conversion(window, timeout_ms=5_000):
    thread = window._conversion_thread
    assert thread is not None

    loop = QEventLoop()
    finished = []
    thread.finished.connect(lambda: (finished.append(True), loop.quit()))
    QTimer.singleShot(timeout_ms, loop.quit)
    loop.exec()
    QApplication.processEvents()

    assert finished, "Conversion worker did not finish before the test timeout"


def _create_window():
    _app_class, window_class, _qt = qt_gui._MainWindowFactory.create()
    return window_class()


def test_conversion_runs_without_blocking_gui_thread(
    qt_app, monkeypatch, message_boxes, tmp_path
):
    class SlowConverter:
        def __init__(self, **_kwargs):
            pass

        def convert(self, _source_file):
            time.sleep(0.15)
            return SimpleNamespace(markdown="# Converted")

    monkeypatch.setattr(qt_gui, "MarkItDown", SlowConverter)
    source_file = tmp_path / "large.pdf"
    source_file.write_bytes(b"test")
    window = _create_window()
    window._selected_files = [source_file]

    events = []
    QTimer.singleShot(10, lambda: events.append("timer"))
    window._convert_files()
    thread = window._conversion_thread
    assert thread is not None
    thread.finished.connect(lambda: events.append("finished"))

    _wait_for_conversion(window)

    assert events == ["timer", "finished"]
    assert source_file.with_suffix(".md").read_text(encoding="utf-8") == "# Converted"
    window.close()


def test_batch_conversion_updates_progress_and_avoids_output_collisions(
    qt_app, monkeypatch, message_boxes, tmp_path
):
    class SuccessfulConverter:
        def __init__(self, **_kwargs):
            pass

        def convert(self, source_file):
            time.sleep(0.02)
            return SimpleNamespace(markdown=f"# {Path(source_file).parent.name}")

    monkeypatch.setattr(qt_gui, "MarkItDown", SuccessfulConverter)
    first_source = tmp_path / "first" / "report.pdf"
    second_source = tmp_path / "second" / "report.pdf"
    first_source.parent.mkdir()
    second_source.parent.mkdir()
    first_source.write_bytes(b"first")
    second_source.write_bytes(b"second")
    output_dir = tmp_path / "output"

    window = _create_window()
    window._selected_files = [first_source, second_source]
    window.write_next_to_source_checkbox.setChecked(False)
    window.output_dir_edit.setText(str(output_dir))
    window._convert_files()

    assert not window.convert_button.isEnabled()
    assert not window.select_files_button.isEnabled()
    _wait_for_conversion(window)

    assert (output_dir / "report.md").read_text(encoding="utf-8") == "# first"
    assert (output_dir / "report_1.md").read_text(encoding="utf-8") == "# second"
    assert window.progress_bar.maximum() == 2
    assert window.progress_bar.value() == 2
    assert window.convert_button.isEnabled()
    assert "Finished. Success: 2, Failed: 0." in window.log_box.toPlainText()
    assert message_boxes[-1] == (
        "information",
        "Conversion completed",
        "Converted 2 file(s) to Markdown.",
    )
    window.close()


def test_conversion_continues_after_one_file_fails(
    qt_app, monkeypatch, message_boxes, tmp_path
):
    class PartiallyFailingConverter:
        def __init__(self, **_kwargs):
            pass

        def convert(self, source_file):
            time.sleep(0.02)
            if Path(source_file).name == "bad.pdf":
                raise RuntimeError("conversion failed")
            return SimpleNamespace(markdown="# Good")

    monkeypatch.setattr(qt_gui, "MarkItDown", PartiallyFailingConverter)
    bad_source = tmp_path / "bad.pdf"
    good_source = tmp_path / "good.pdf"
    bad_source.write_bytes(b"bad")
    good_source.write_bytes(b"good")

    window = _create_window()
    window._selected_files = [bad_source, good_source]
    window._convert_files()
    _wait_for_conversion(window)

    log = window.log_box.toPlainText()
    assert "ERROR:" in log
    assert "conversion failed" in log
    assert "OK:" in log
    assert "Finished. Success: 1, Failed: 1." in log
    assert not bad_source.with_suffix(".md").exists()
    assert good_source.with_suffix(".md").read_text(encoding="utf-8") == "# Good"
    assert window.progress_bar.value() == 2
    assert message_boxes[-1] == (
        "warning",
        "Conversion completed with errors",
        "Converted 1 file(s), 1 failed.",
    )
    window.close()
