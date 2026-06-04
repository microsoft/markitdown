from __future__ import annotations

import sys
from pathlib import Path
from typing import Protocol

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ._base_converter import DocumentConverterResult
from ._markitdown import MarkItDown

APPEARANCE_MODE = "dark"
GUI_BACKEND = "pyside6"


class Converter(Protocol):
    def convert(self, path: Path) -> DocumentConverterResult:
        ...


def convert_file_to_markdown(
    input_path: str | Path,
    output_path: str | Path,
    *,
    converter: Converter | None = None,
) -> None:
    source = Path(input_path) if input_path else None
    destination = Path(output_path) if output_path else None

    if source is None or not source.exists():
        raise ValueError("Input file does not exist.")
    if not source.is_file():
        raise ValueError("Input path is not a file.")
    if destination is None:
        raise ValueError("Output path is required.")
    if not destination.parent.exists():
        raise ValueError("Output directory does not exist.")

    active_converter = converter or MarkItDown(enable_plugins=False)
    result = active_converter.convert(source)
    destination.write_text(result.markdown, encoding="utf-8")


class ConversionSignals(QObject):
    finished = Signal()
    failed = Signal(str)


class ConversionWorker(QRunnable):
    def __init__(self, input_path: str, output_path: str):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.signals = ConversionSignals()

    @Slot()
    def run(self) -> None:
        try:
            convert_file_to_markdown(self.input_path, self.output_path)
        except Exception as exc:
            self.signals.failed.emit(str(exc))
        else:
            self.signals.finished.emit()


class MarkItDownGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread_pool = QThreadPool.globalInstance()
        self.setWindowTitle("MarkItDown GUI")
        self.setMinimumSize(760, 430)
        self.resize(820, 460)

        self.input_entry = QLineEdit()
        self.output_entry = QLineEdit()
        self.status_label = QLabel("Choose an input file and output path.")
        self.browse_button = QPushButton("Browse")
        self.choose_button = QPushButton("Choose")
        self.convert_button = QPushButton("Convert")

        self._build()
        self._connect()
        self._update_convert_state()

    def _build(self) -> None:
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        page = QVBoxLayout(root)
        page.setContentsMargins(28, 28, 28, 28)

        card = QFrame()
        card.setObjectName("card")
        page.addWidget(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(30, 30, 30, 26)
        layout.setSpacing(22)

        title = QLabel("MarkItDown")
        title.setObjectName("title")
        subtitle = QLabel("Convert one document into Markdown")
        subtitle.setObjectName("subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        fields = QFrame()
        fields.setObjectName("fields")
        grid = QGridLayout(fields)
        grid.setContentsMargins(18, 18, 18, 18)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(14)
        grid.setColumnStretch(1, 1)

        self.input_entry.setReadOnly(True)
        self.input_entry.setPlaceholderText("Select source file")
        self.output_entry.setPlaceholderText("Choose markdown output path")
        self.browse_button.setFixedWidth(110)
        self.choose_button.setFixedWidth(110)

        grid.addWidget(QLabel("Input file"), 0, 0)
        grid.addWidget(self.input_entry, 0, 1)
        grid.addWidget(self.browse_button, 0, 2)
        grid.addWidget(QLabel("Output file"), 1, 0)
        grid.addWidget(self.output_entry, 1, 1)
        grid.addWidget(self.choose_button, 1, 2)
        layout.addWidget(fields)

        actions = QHBoxLayout()
        self.status_label.setObjectName("status")
        self.status_label.setWordWrap(True)
        self.status_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.convert_button.setObjectName("primary")
        self.convert_button.setFixedSize(148, 44)
        actions.addWidget(self.status_label)
        actions.addWidget(self.convert_button)
        layout.addLayout(actions)

        self.setStyleSheet(DARK_STYLESHEET)

    def _connect(self) -> None:
        self.browse_button.clicked.connect(self._browse_input)
        self.choose_button.clicked.connect(self._choose_output)
        self.convert_button.clicked.connect(self._convert)
        self.input_entry.textChanged.connect(self._update_convert_state)
        self.output_entry.textChanged.connect(self._update_convert_state)

    def _browse_input(self) -> None:
        selected, _ = QFileDialog.getOpenFileName(self, "Choose input file")
        if not selected:
            return
        path = Path(selected)
        self.input_entry.setText(str(path))
        self.output_entry.setText(str(path.with_suffix(".md")))
        self.status_label.setText("Ready to convert.")

    def _choose_output(self) -> None:
        current = self.output_entry.text().strip()
        initial = current or str(Path.cwd() / "output.md")
        selected, _ = QFileDialog.getSaveFileName(
            self,
            "Choose output Markdown file",
            initial,
            "Markdown files (*.md);;All files (*)",
        )
        if selected:
            path = Path(selected)
            if path.suffix == "":
                path = path.with_suffix(".md")
            self.output_entry.setText(str(path))

    def _set_busy(self, busy: bool) -> None:
        for widget in (
            self.input_entry,
            self.output_entry,
            self.browse_button,
            self.choose_button,
            self.convert_button,
        ):
            widget.setEnabled(not busy)

    def _update_convert_state(self) -> None:
        has_paths = bool(self.input_entry.text().strip() and self.output_entry.text().strip())
        self.convert_button.setEnabled(has_paths)

    def _convert(self) -> None:
        self._set_busy(True)
        self.status_label.setText("Converting...")

        worker = ConversionWorker(self.input_entry.text(), self.output_entry.text())
        worker.signals.finished.connect(self._finish_success)
        worker.signals.failed.connect(self._finish_with_error)
        self.thread_pool.start(worker)

    def _finish_success(self) -> None:
        self._set_busy(False)
        self.status_label.setText(f"Done: {self.output_entry.text()}")
        self._update_convert_state()

    def _finish_with_error(self, message: str) -> None:
        self._set_busy(False)
        self.status_label.setText(f"Error: {message}")
        self._update_convert_state()


DARK_STYLESHEET = """
QWidget#root {
    background: #0f172a;
    color: #e5e7eb;
    font-family: Inter, Segoe UI, Arial, sans-serif;
    font-size: 13px;
}
QFrame#card {
    background: #111827;
    border-radius: 18px;
}
QFrame#fields {
    background: #0b1220;
    border-radius: 14px;
}
QLabel {
    color: #e5e7eb;
}
QLabel#title {
    color: #f8fafc;
    font-size: 28px;
    font-weight: 700;
}
QLabel#subtitle, QLabel#status {
    color: #94a3b8;
}
QLineEdit {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #f8fafc;
    min-height: 38px;
    padding: 0 12px;
}
QLineEdit:focus {
    border-color: #3b82f6;
}
QPushButton {
    background: #334155;
    border: 0;
    border-radius: 8px;
    color: #f8fafc;
    min-height: 38px;
    padding: 0 16px;
}
QPushButton:hover {
    background: #475569;
}
QPushButton:disabled {
    background: #1e293b;
    color: #64748b;
}
QPushButton#primary {
    background: #2563eb;
    font-weight: 700;
}
QPushButton#primary:hover {
    background: #1d4ed8;
}
"""


def main() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    window = MarkItDownGUI()
    window.show()
    raise SystemExit(app.exec())
