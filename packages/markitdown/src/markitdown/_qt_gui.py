# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, List

from ._markitdown import MarkItDown


class _MainWindowFactory:
    @staticmethod
    def create():
        try:
            from PyQt6.QtCore import QObject, QThread, Qt, pyqtSignal, pyqtSlot
            from PyQt6.QtWidgets import (
                QApplication,
                QCheckBox,
                QFileDialog,
                QGridLayout,
                QGroupBox,
                QHBoxLayout,
                QLabel,
                QLineEdit,
                QListWidget,
                QMainWindow,
                QMessageBox,
                QPushButton,
                QPlainTextEdit,
                QProgressBar,
                QVBoxLayout,
                QWidget,
            )
        except ImportError as exc:
            raise RuntimeError(
                "PyQt6 is not installed. Install with: pip install 'markitdown[gui]'"
            ) from exc

        class ConversionWorker(QObject):
            progress = pyqtSignal(int, int)
            log = pyqtSignal(str)
            finished = pyqtSignal(int, int)

            def __init__(
                self,
                source_files: List[Path],
                target_directory: Path | None,
                enable_plugins: bool,
            ):
                super().__init__()
                self._source_files = source_files
                self._target_directory = target_directory
                self._enable_plugins = enable_plugins

            @pyqtSlot()
            def run(self):
                converter = MarkItDown(enable_plugins=self._enable_plugins)
                success_count = 0
                failure_count = 0
                seen_outputs: set[Path] = set()

                for index, source_file in enumerate(self._source_files, start=1):
                    try:
                        output_file = self._resolve_output_path(
                            source_file=source_file,
                            target_directory=self._target_directory,
                            seen_outputs=seen_outputs,
                        )
                        result = converter.convert(str(source_file))
                        output_file.write_text(result.markdown, encoding="utf-8")
                        success_count += 1
                        self.log.emit(f"OK: {source_file} -> {output_file}")
                    except Exception as exc:
                        failure_count += 1
                        self.log.emit(f"ERROR: {source_file} ({exc})")
                    finally:
                        self.progress.emit(index, len(self._source_files))

                self.finished.emit(success_count, failure_count)

            @staticmethod
            def _resolve_output_path(
                source_file: Path,
                target_directory: Path | None,
                seen_outputs: set[Path],
            ) -> Path:
                if target_directory is None:
                    candidate = source_file.with_suffix(".md")
                else:
                    candidate = target_directory / f"{source_file.stem}.md"

                if candidate not in seen_outputs:
                    seen_outputs.add(candidate)
                    return candidate

                index = 1
                while True:
                    if target_directory is None:
                        next_candidate = source_file.with_name(
                            f"{source_file.stem}_{index}.md"
                        )
                    else:
                        next_candidate = (
                            target_directory / f"{source_file.stem}_{index}.md"
                        )
                    if next_candidate not in seen_outputs:
                        seen_outputs.add(next_candidate)
                        return next_candidate
                    index += 1

        class MarkItDownWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("MarkItDown - Multi File to Markdown")
                self.resize(920, 620)

                self._selected_files: List[Path] = []
                self._conversion_thread: QThread | None = None
                self._conversion_worker: ConversionWorker | None = None

                central = QWidget(self)
                self.setCentralWidget(central)
                root_layout = QVBoxLayout(central)

                # File selection area
                files_group = QGroupBox("Input Files")
                files_layout = QVBoxLayout(files_group)
                root_layout.addWidget(files_group)

                actions_layout = QHBoxLayout()
                self.select_files_button = QPushButton("Select Files")
                self.clear_files_button = QPushButton("Clear")
                actions_layout.addWidget(self.select_files_button)
                actions_layout.addWidget(self.clear_files_button)
                actions_layout.addStretch(1)
                files_layout.addLayout(actions_layout)

                self.files_list = QListWidget()
                files_layout.addWidget(self.files_list)

                # Output settings area
                output_group = QGroupBox("Output Settings")
                output_layout = QGridLayout(output_group)
                root_layout.addWidget(output_group)

                self.write_next_to_source_checkbox = QCheckBox(
                    "Save next to each source file"
                )
                self.write_next_to_source_checkbox.setChecked(True)
                output_layout.addWidget(self.write_next_to_source_checkbox, 0, 0, 1, 3)

                output_layout.addWidget(QLabel("Output folder:"), 1, 0)
                self.output_dir_edit = QLineEdit()
                self.output_dir_edit.setPlaceholderText(
                    "Choose a folder when not saving next to source"
                )
                self.output_dir_edit.setEnabled(False)
                output_layout.addWidget(self.output_dir_edit, 1, 1)

                self.select_output_button = QPushButton("Browse")
                self.select_output_button.setEnabled(False)
                output_layout.addWidget(self.select_output_button, 1, 2)

                self.use_plugins_checkbox = QCheckBox("Enable 3rd-party plugins")
                output_layout.addWidget(self.use_plugins_checkbox, 2, 0, 1, 3)

                # Run area
                run_layout = QHBoxLayout()
                self.convert_button = QPushButton("Convert to Markdown")
                self.convert_button.setEnabled(False)
                run_layout.addWidget(self.convert_button)
                self.progress_bar = QProgressBar()
                self.progress_bar.setRange(0, 1)
                self.progress_bar.setValue(0)
                self.progress_bar.setFormat("Ready")
                run_layout.addWidget(self.progress_bar, 1)
                run_layout.addStretch(1)
                root_layout.addLayout(run_layout)

                # Log area
                root_layout.addWidget(QLabel("Conversion Log"))
                self.log_box = QPlainTextEdit()
                self.log_box.setReadOnly(True)
                self.log_box.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
                root_layout.addWidget(self.log_box, 1)

                self.select_files_button.clicked.connect(self._select_files)
                self.clear_files_button.clicked.connect(self._clear_files)
                self.select_output_button.clicked.connect(self._select_output_dir)
                self.convert_button.clicked.connect(self._convert_files)
                self.write_next_to_source_checkbox.toggled.connect(
                    self._on_output_mode_changed
                )

            def _on_output_mode_changed(self, checked: bool):
                self.output_dir_edit.setEnabled(not checked)
                self.select_output_button.setEnabled(not checked)

            def _select_files(self):
                selected, _ = QFileDialog.getOpenFileNames(
                    self,
                    "Select files to convert",
                    "",
                    "All files (*.*)",
                )
                if not selected:
                    return

                self._selected_files = [Path(item) for item in selected]
                self.files_list.clear()
                for file_path in self._selected_files:
                    self.files_list.addItem(str(file_path))

                self.convert_button.setEnabled(len(self._selected_files) > 0)
                self._append_log(
                    f"Selected {len(self._selected_files)} file(s) for conversion."
                )

            def _clear_files(self):
                self._selected_files = []
                self.files_list.clear()
                self.convert_button.setEnabled(False)
                self._append_log("Cleared selected files.")

            def _select_output_dir(self):
                directory = QFileDialog.getExistingDirectory(
                    self,
                    "Select output directory",
                )
                if directory:
                    self.output_dir_edit.setText(directory)

            def _convert_files(self):
                if not self._selected_files:
                    QMessageBox.information(self, "No files", "Select files first.")
                    return

                target_directory: Path | None
                if self.write_next_to_source_checkbox.isChecked():
                    target_directory = None
                else:
                    raw_output_dir = self.output_dir_edit.text().strip()
                    if not raw_output_dir:
                        QMessageBox.warning(
                            self,
                            "Missing output folder",
                            "Choose an output folder or enable saving next to source files.",
                        )
                        return
                    target_directory = Path(raw_output_dir)
                    target_directory.mkdir(parents=True, exist_ok=True)

                self._set_conversion_controls_enabled(False)
                self.progress_bar.setRange(0, len(self._selected_files))
                self.progress_bar.setValue(0)
                self.progress_bar.setFormat("Converting %v of %m files")
                self._append_log("Starting conversion...")

                self._conversion_thread = QThread(self)
                self._conversion_worker = ConversionWorker(
                    source_files=list(self._selected_files),
                    target_directory=target_directory,
                    enable_plugins=self.use_plugins_checkbox.isChecked(),
                )
                self._conversion_worker.moveToThread(self._conversion_thread)
                self._conversion_thread.started.connect(self._conversion_worker.run)
                self._conversion_worker.log.connect(self._append_log)
                self._conversion_worker.progress.connect(self._update_progress)
                self._conversion_worker.finished.connect(self._conversion_finished)
                self._conversion_worker.finished.connect(self._conversion_thread.quit)
                self._conversion_worker.finished.connect(
                    self._conversion_worker.deleteLater
                )
                self._conversion_thread.finished.connect(
                    self._conversion_thread.deleteLater
                )
                self._conversion_thread.finished.connect(self._clear_conversion_thread)
                self._conversion_thread.start()

            @pyqtSlot(int, int)
            def _update_progress(self, completed: int, total: int):
                self.progress_bar.setMaximum(total)
                self.progress_bar.setValue(completed)

            @pyqtSlot(int, int)
            def _conversion_finished(self, success_count: int, failure_count: int):
                self._append_log(
                    f"Finished. Success: {success_count}, Failed: {failure_count}."
                )
                self.progress_bar.setFormat("Finished: %v of %m files")
                self._set_conversion_controls_enabled(True)

                if failure_count > 0:
                    QMessageBox.warning(
                        self,
                        "Conversion completed with errors",
                        f"Converted {success_count} file(s), {failure_count} failed.",
                    )
                else:
                    QMessageBox.information(
                        self,
                        "Conversion completed",
                        f"Converted {success_count} file(s) to Markdown.",
                    )

            @pyqtSlot()
            def _clear_conversion_thread(self):
                self._conversion_worker = None
                self._conversion_thread = None

            def _set_conversion_controls_enabled(self, enabled: bool):
                self.select_files_button.setEnabled(enabled)
                self.clear_files_button.setEnabled(enabled)
                self.write_next_to_source_checkbox.setEnabled(enabled)
                self.output_dir_edit.setEnabled(
                    enabled and not self.write_next_to_source_checkbox.isChecked()
                )
                self.select_output_button.setEnabled(
                    enabled and not self.write_next_to_source_checkbox.isChecked()
                )
                self.use_plugins_checkbox.setEnabled(enabled)
                self.convert_button.setEnabled(enabled and bool(self._selected_files))

            def _append_log(self, message: str):
                self.log_box.appendPlainText(message)

        return QApplication, MarkItDownWindow, Qt


def main(argv: Iterable[str] | None = None) -> int:
    _ = argv  # Kept for parity with CLI-style entry points.
    app_class, window_class, _qt = _MainWindowFactory.create()
    app = app_class(sys.argv)
    window = window_class()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
