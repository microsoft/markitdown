import os
import threading
import time
from pathlib import Path
from typing import Callable, Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FolderWatchHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback

    def on_created(self, event):
        if event.is_directory:
            return
        self.callback(event.src_path)


class FolderWatcherService:
    def __init__(self, database):
        self.database = database
        self.observer: Optional[Observer] = None
        self.callback: Optional[Callable[[str], None]] = None

    def watch_folder(self, folder: str, callback: Callable[[str], None]) -> None:
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join(timeout=2)

        self.callback = callback
        path = Path(folder).expanduser().resolve()
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        event_handler = FolderWatchHandler(callback)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(path), recursive=True)
        self.observer.start()
