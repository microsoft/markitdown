import os
import sys
import time
from pathlib import Path
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from core.conversion import ConversionService
from core.database import StudioDatabase
from core.watcher import FolderWatcherService
from plugins import PlaceholderPluginManager


class DropZone(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setObjectName("drop-zone")
        self.setMinimumHeight(180)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.icon = QLabel("📄")
        self.icon.setObjectName("drop-zone-icon")
        self.icon.setAlignment(Qt.AlignCenter)
        self.label = QLabel("Drag and drop files here\nor browse to convert them")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.button = QPushButton("Browse Files")
        self.button.clicked.connect(self._browse_files)
        layout.addWidget(self.icon)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.file_drop_callback = None

    def _browse_files(self):
        if self.file_drop_callback:
            self.file_drop_callback([])

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        paths = [url.toLocalFile() for url in event.mimeData().urls() if url.isLocalFile()]
        if self.file_drop_callback:
            self.file_drop_callback(paths)
        event.acceptProposedAction()


class StudioMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = StudioDatabase()
        self.conversion_service = ConversionService(self.database)
        self.watcher_service = FolderWatcherService(self.database)
        self.plugin_manager = PlaceholderPluginManager()
        self.current_page = "home"
        self.queue_items: List[dict] = []
        self._build_ui()
        self._connect_signals()
        self.refresh_dashboard()

    def _build_ui(self):
        self.setWindowTitle("MarkItDown Studio")
        self.resize(1400, 900)
        self.setMinimumSize(1100, 750)

        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        nav = QWidget(self)
        nav.setObjectName("nav-pane")
        nav.setFixedWidth(240)
        nav_layout = QVBoxLayout(nav)
        nav_layout.setContentsMargins(16, 16, 16, 16)
        nav_layout.setSpacing(10)

        title = QLabel("MarkItDown Studio")
        title.setObjectName("app-title")
        nav_layout.addWidget(title)
        nav_layout.addSpacing(10)

        self.nav_buttons = {}
        for key, label in [
            ("home", "Home"),
            ("single", "Single File"),
            ("batch", "Batch Convert"),
            ("watcher", "Folder Watcher"),
            ("history", "History"),
            ("obsidian", "Obsidian"),
            ("ai", "AI Tools"),
            ("ocr", "OCR"),
            ("settings", "Settings"),
            ("about", "About"),
        ]:
            button = QPushButton(label)
            button.setCheckable(True)
            button.setObjectName("nav-button")
            button.clicked.connect(lambda checked=False, value=key: self.show_page(value))
            nav_layout.addWidget(button)
            self.nav_buttons[key] = button

        nav_layout.addStretch()
        footer = QLabel("Built for the AI Factory")
        footer.setObjectName("footer-label")
        nav_layout.addWidget(footer)

        self.content_stack = QStackedWidget(self)
        self.content_stack.setObjectName("content-stack")
        self._build_pages()

        splitter = QSplitter(self)
        splitter.setHandleWidth(1)
        splitter.addWidget(nav)
        splitter.addWidget(self.content_stack)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)

        self.setStyleSheet(self._load_stylesheet())
        self._set_status_bar()

    def _set_status_bar(self):
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def _build_pages(self):
        self.home_page = self._create_home_page()
        self.single_page = self._create_single_file_page()
        self.batch_page = self._create_batch_page()
        self.watcher_page = self._create_watcher_page()
        self.history_page = self._create_history_page()
        self.obsidian_page = self._create_obsidian_page()
        self.ai_page = self._create_ai_page()
        self.ocr_page = self._create_ocr_page()
        self.settings_page = self._create_settings_page()
        self.about_page = self._create_about_page()

        self.content_stack.addWidget(self.home_page)
        self.content_stack.addWidget(self.single_page)
        self.content_stack.addWidget(self.batch_page)
        self.content_stack.addWidget(self.watcher_page)
        self.content_stack.addWidget(self.history_page)
        self.content_stack.addWidget(self.obsidian_page)
        self.content_stack.addWidget(self.ai_page)
        self.content_stack.addWidget(self.ocr_page)
        self.content_stack.addWidget(self.settings_page)
        self.content_stack.addWidget(self.about_page)

    def _connect_signals(self):
        self.single_browse_button.clicked.connect(self._browse_single_file)
        self.single_convert_button.clicked.connect(self._convert_single_file)
        self.batch_add_button.clicked.connect(self._add_batch_file)
        self.batch_start_button.clicked.connect(self._start_batch_queue)
        self.batch_clear_button.clicked.connect(self._clear_batch_queue)
        self.batch_remove_button.clicked.connect(self._remove_selected_batch_item)
        self.watch_toggle_button.clicked.connect(self._toggle_watcher)
        self.export_obsidian_button.clicked.connect(self._export_obsidian)
        self.ai_suggest_button.clicked.connect(self._run_placeholder_ai)
        self.ocr_start_button.clicked.connect(self._run_placeholder_ocr)
        self.settings_save_button.clicked.connect(self._save_settings)

    def show_page(self, page_key: str):
        mapping = {
            "home": 0,
            "single": 1,
            "batch": 2,
            "watcher": 3,
            "history": 4,
            "obsidian": 5,
            "ai": 6,
            "ocr": 7,
            "settings": 8,
            "about": 9,
        }
        self.content_stack.setCurrentIndex(mapping[page_key])
        self.current_page = page_key
        for key, button in self.nav_buttons.items():
            button.setChecked(key == page_key)

    def refresh_dashboard(self):
        stats = self.database.get_statistics()
        self.home_total_label.setText(str(stats["total"]))
        self.home_errors_label.setText(str(stats["errors"]))
        self.home_queue_label.setText(str(stats["queue"]))
        self.home_average_label.setText(f"{stats['avg_seconds']:.1f}s")
        self._refresh_recent_files()
        self._refresh_history_table()
        self._refresh_watcher_state()

    def _refresh_recent_files(self):
        records = self.database.get_recent_history(limit=6)
        self.recent_files_list.clear()
        for record in records:
            item = QListWidgetItem(record.filename)
            self.recent_files_list.addItem(item)

    def _refresh_history_table(self):
        records = self.database.get_recent_history(limit=20)
        self.history_table.setRowCount(len(records))
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["File", "Status", "Output", "Created"])
        for row, record in enumerate(records):
            self.history_table.setItem(row, 0, QTableWidgetItem(record.filename))
            self.history_table.setItem(row, 1, QTableWidgetItem(record.status))
            self.history_table.setItem(row, 2, QTableWidgetItem(record.output_path or ""))
            self.history_table.setItem(row, 3, QTableWidgetItem(record.created_at))

    def _refresh_watcher_state(self):
        folder = self.database.get_setting("watch_folder")
        if folder:
            self.watch_folder_edit.setText(folder)
            self.watch_status_label.setText("Watching")
        else:
            self.watch_status_label.setText("Idle")

    def _create_home_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        drop = DropZone(self)
        drop.file_drop_callback = self._handle_dropped_files
        layout.addWidget(drop)

        cards = QHBoxLayout()
        cards.setSpacing(16)
        self.home_total_label = QLabel("0")
        self.home_errors_label = QLabel("0")
        self.home_queue_label = QLabel("0")
        self.home_average_label = QLabel("0.0s")
        for label, value in [
            ("Total Converted", self.home_total_label),
            ("Errors", self.home_errors_label),
            ("Queue", self.home_queue_label),
            ("Average Time", self.home_average_label),
        ]:
            card = QFrame(self)
            card.setObjectName("stat-card")
            card_layout = QVBoxLayout(card)
            card_layout.addWidget(QLabel(label))
            card_layout.addWidget(value)
            cards.addWidget(card)
        layout.addLayout(cards)

        bottom = QHBoxLayout()
        bottom.setSpacing(16)
        left = QGroupBox("Recent Files")
        left_layout = QVBoxLayout(left)
        self.recent_files_list = QListWidget(self)
        left_layout.addWidget(self.recent_files_list)
        bottom.addWidget(left, 1)

        right = QGroupBox("Recent Activity")
        right_layout = QVBoxLayout(right)
        self.activity_browser = QTextBrowser(self)
        self.activity_browser.setMaximumHeight(220)
        right_layout.addWidget(self.activity_browser)
        bottom.addWidget(right, 1)
        layout.addLayout(bottom)

        self.activity_browser.setPlainText("Start converting documents to see recent activity here.")
        return page

    def _create_single_file_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        top = QHBoxLayout()
        self.single_input = QLineEdit(self)
        self.single_input.setPlaceholderText("Select a document to convert")
        self.single_browse_button = QPushButton("Browse")
        top.addWidget(self.single_input, 1)
        top.addWidget(self.single_browse_button)
        layout.addLayout(top)

        body = QHBoxLayout()
        body.setSpacing(16)
        preview_group = QGroupBox("Document Preview")
        preview_layout = QVBoxLayout(preview_group)
        self.single_preview = QTextBrowser(self)
        preview_layout.addWidget(self.single_preview)
        body.addWidget(preview_group, 1)

        markdown_group = QGroupBox("Markdown Preview")
        markdown_layout = QVBoxLayout(markdown_group)
        self.single_markdown = QPlainTextEdit(self)
        self.single_markdown.setReadOnly(True)
        markdown_layout.addWidget(self.single_markdown)
        body.addWidget(markdown_group, 1)
        layout.addLayout(body)

        buttons = QHBoxLayout()
        self.single_convert_button = QPushButton("Convert")
        buttons.addWidget(self.single_convert_button)
        buttons.addStretch()
        layout.addLayout(buttons)
        return page

    def _create_batch_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        toolbar = QHBoxLayout()
        self.batch_add_button = QPushButton("Add Files")
        self.batch_remove_button = QPushButton("Remove")
        self.batch_start_button = QPushButton("Start")
        self.batch_clear_button = QPushButton("Clear")
        toolbar.addWidget(self.batch_add_button)
        toolbar.addWidget(self.batch_remove_button)
        toolbar.addWidget(self.batch_start_button)
        toolbar.addWidget(self.batch_clear_button)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.batch_table = QTableWidget(self)
        self.batch_table.setColumnCount(5)
        self.batch_table.setHorizontalHeaderLabels(["File", "Type", "Progress", "Status", "Output"])
        self.batch_table.setAlternatingRowColors(True)
        layout.addWidget(self.batch_table)
        return page

    def _create_watcher_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        folder_row = QHBoxLayout()
        self.watch_folder_edit = QLineEdit(self)
        self.watch_folder_edit.setPlaceholderText("Choose a folder to monitor")
        self.watch_toggle_button = QPushButton("Start Watching")
        folder_row.addWidget(self.watch_folder_edit, 1)
        folder_row.addWidget(self.watch_toggle_button)
        layout.addLayout(folder_row)

        self.watch_status_label = QLabel("Idle")
        layout.addWidget(self.watch_status_label)
        info = QLabel("The watcher will automatically queue new documents for conversion and preserve the folder structure.")
        info.setWordWrap(True)
        layout.addWidget(info)
        layout.addStretch()
        return page

    def _create_history_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.history_table = QTableWidget(self)
        layout.addWidget(self.history_table)
        return page

    def _create_obsidian_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        label = QLabel("Export converted Markdown into an Obsidian-friendly vault structure. This is a placeholder integration for now.")
        label.setWordWrap(True)
        layout.addWidget(label)
        self.export_obsidian_button = QPushButton("Export to Obsidian")
        layout.addWidget(self.export_obsidian_button)
        layout.addStretch()
        return page

    def _create_ai_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        label = QLabel("AI tools such as summarization, prompt-based extraction, and smart tagging are planned. A placeholder workflow is available now.")
        label.setWordWrap(True)
        layout.addWidget(label)
        self.ai_suggest_button = QPushButton("Run Placeholder AI Suggestions")
        layout.addWidget(self.ai_suggest_button)
        layout.addStretch()
        return page

    def _create_ocr_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        label = QLabel("OCR support is available through the MarkItDown ecosystem and the add-in plugin path. This page uses a placeholder workflow for now.")
        label.setWordWrap(True)
        layout.addWidget(label)
        self.ocr_start_button = QPushButton("Run Placeholder OCR")
        layout.addWidget(self.ocr_start_button)
        layout.addStretch()
        return page

    def _create_settings_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        group = QGroupBox("Preferences")
        group_layout = QVBoxLayout(group)
        self.output_dir_edit = QLineEdit(self)
        self.output_dir_edit.setPlaceholderText("Output folder")
        group_layout.addWidget(QLabel("Output folder"))
        group_layout.addWidget(self.output_dir_edit)

        self.open_output_checkbox = QFrame(self)
        self.open_output_checkbox = QPushButton("Save settings")
        self.settings_save_button = QPushButton("Save Settings")
        group_layout.addWidget(self.settings_save_button)
        layout.addWidget(group)
        layout.addStretch()
        return page

    def _create_about_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.addWidget(QLabel("MarkItDown Studio\nVersion 1.0.0\nA polished Windows desktop front end for Microsoft MarkItDown."))
        layout.addStretch()
        return page

    def _load_stylesheet(self) -> str:
        stylesheet_path = Path(__file__).resolve().parent.parent / "themes" / "dark.qss"
        if stylesheet_path.exists():
            return stylesheet_path.read_text(encoding="utf-8")
        return ""

    def _browse_single_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select a document", str(Path.home()))
        if path:
            self.single_input.setText(path)
            self.single_preview.setPlainText(Path(path).read_text(encoding="utf-8", errors="ignore")[:4000])

    def _convert_single_file(self):
        source = self.single_input.text().strip()
        if not source:
            QMessageBox.warning(self, "Missing file", "Please select a source file first.")
            return
        output_dir = self.database.get_setting("output_dir") or str(Path.home() / "markitdown-output")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        try:
            result = self.conversion_service.convert_file(source, output_dir)
            self.single_markdown.setPlainText(result["markdown"])
            self.status_bar.showMessage(f"Converted {Path(source).name} -> {result['output_path']}")
            self.refresh_dashboard()
        except Exception as exc:  # pragma: no cover - runtime feedback
            QMessageBox.critical(self, "Conversion failed", str(exc))
            self.status_bar.showMessage("Conversion failed")

    def _handle_dropped_files(self, paths: List[str]):
        if not paths:
            paths = [self._browse_for_files()]
        if not paths:
            return
        self.queue_items = [{"path": path, "status": "Queued"} for path in paths if path]
        self._refresh_batch_table()
        self.show_page("batch")

    def _browse_for_files(self) -> List[str]:
        paths, _ = QFileDialog.getOpenFileNames(self, "Select documents", str(Path.home()))
        return paths

    def _add_batch_file(self):
        paths = self._browse_for_files()
        self.queue_items.extend({"path": path, "status": "Queued"} for path in paths)
        self._refresh_batch_table()

    def _refresh_batch_table(self):
        self.batch_table.setRowCount(len(self.queue_items))
        for row, item in enumerate(self.queue_items):
            self.batch_table.setItem(row, 0, QTableWidgetItem(Path(item["path"]).name))
            self.batch_table.setItem(row, 1, QTableWidgetItem("Document"))
            self.batch_table.setItem(row, 2, QTableWidgetItem("0%"))
            self.batch_table.setItem(row, 3, QTableWidgetItem(item.get("status", "Queued")))
            self.batch_table.setItem(row, 4, QTableWidgetItem("Pending"))

    def _start_batch_queue(self):
        output_dir = self.database.get_setting("output_dir") or str(Path.home() / "markitdown-output")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        for row, item in enumerate(self.queue_items):
            path = item["path"]
            self.batch_table.setItem(row, 3, QTableWidgetItem("Working"))
            QApplication.processEvents()
            try:
                result = self.conversion_service.convert_file(path, output_dir)
                self.batch_table.setItem(row, 2, QTableWidgetItem("100%"))
                self.batch_table.setItem(row, 3, QTableWidgetItem("Completed"))
                self.batch_table.setItem(row, 4, QTableWidgetItem(result["output_path"]))
            except Exception as exc:
                self.batch_table.setItem(row, 3, QTableWidgetItem("Error"))
                self.batch_table.setItem(row, 4, QTableWidgetItem(str(exc)))
            QApplication.processEvents()
        self.refresh_dashboard()

    def _clear_batch_queue(self):
        self.queue_items.clear()
        self._refresh_batch_table()

    def _remove_selected_batch_item(self):
        selected = self.batch_table.selectedItems()
        if not selected:
            return
        row = selected[0].row()
        if 0 <= row < len(self.queue_items):
            self.queue_items.pop(row)
            self._refresh_batch_table()

    def _toggle_watcher(self):
        folder = self.watch_folder_edit.text().strip()
        if not folder:
            QMessageBox.warning(self, "Missing folder", "Please choose a folder to watch.")
            return
        self.database.set_setting("watch_folder", folder)
        self.watcher_service.watch_folder(folder, self._watcher_callback)
        self.watch_status_label.setText("Watching")
        self.status_bar.showMessage(f"Watcher active for {folder}")

    def _watcher_callback(self, path: str):
        self.activity_browser.append(f"Queued {Path(path).name} from watcher")
        output_dir = self.database.get_setting("output_dir") or str(Path.home() / "markitdown-output")
        self.conversion_service.convert_file(path, output_dir)
        self.refresh_dashboard()

    def _export_obsidian(self):
        self.status_bar.showMessage("Obsidian export placeholder executed")
        QMessageBox.information(self, "Obsidian export", "The export workflow is prepared and ready for a future vault integration.")

    def _run_placeholder_ai(self):
        self.status_bar.showMessage("AI placeholder executed")
        QMessageBox.information(self, "AI tools", "Placeholder suggestions are ready for future summarization and extraction workflows.")

    def _run_placeholder_ocr(self):
        self.status_bar.showMessage("OCR placeholder executed")
        QMessageBox.information(self, "OCR", "OCR is routed through the plugin path and is ready for further integration.")

    def _save_settings(self):
        self.database.set_setting("output_dir", self.output_dir_edit.text().strip() or str(Path.home() / "markitdown-output"))
        self.status_bar.showMessage("Settings saved")
