from __future__ import annotations

import threading
from pathlib import Path
from tkinter import Tk, StringVar, filedialog, ttk
from typing import Protocol

from ._base_converter import DocumentConverterResult
from ._markitdown import MarkItDown


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


class MarkItDownGUI:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("MarkItDown GUI")
        self.input_path = StringVar()
        self.output_path = StringVar()
        self.status = StringVar(value="Choose an input file and output path.")

        self._build()
        self._update_convert_state()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Input file").grid(row=0, column=0, sticky="w", pady=4)
        self.input_entry = ttk.Entry(
            frame, textvariable=self.input_path, state="readonly", width=56
        )
        self.input_entry.grid(row=0, column=1, sticky="ew", padx=8, pady=4)
        self.browse_button = ttk.Button(
            frame, text="Browse", command=self._browse_input
        )
        self.browse_button.grid(row=0, column=2, pady=4)

        ttk.Label(frame, text="Output file").grid(row=1, column=0, sticky="w", pady=4)
        self.output_entry = ttk.Entry(frame, textvariable=self.output_path, width=56)
        self.output_entry.grid(row=1, column=1, sticky="ew", padx=8, pady=4)
        self.choose_button = ttk.Button(
            frame, text="Choose", command=self._choose_output
        )
        self.choose_button.grid(row=1, column=2, pady=4)

        self.convert_button = ttk.Button(frame, text="Convert", command=self._convert)
        self.convert_button.grid(row=2, column=1, sticky="e", padx=8, pady=(12, 4))

        self.status_label = ttk.Label(frame, textvariable=self.status, wraplength=520)
        self.status_label.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(12, 0))

        self.input_path.trace_add("write", lambda *_: self._update_convert_state())
        self.output_path.trace_add("write", lambda *_: self._update_convert_state())

    def _browse_input(self) -> None:
        selected = filedialog.askopenfilename(title="Choose input file")
        if not selected:
            return

        path = Path(selected)
        self.input_path.set(str(path))
        self.output_path.set(str(path.with_suffix(".md")))
        self.status.set("Ready to convert.")

    def _choose_output(self) -> None:
        initial = Path(self.output_path.get()) if self.output_path.get() else None
        selected = filedialog.asksaveasfilename(
            title="Choose output Markdown file",
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialdir=str(initial.parent) if initial else None,
            initialfile=initial.name if initial else None,
        )
        if selected:
            self.output_path.set(selected)

    def _set_busy(self, busy: bool) -> None:
        state = "disabled" if busy else "normal"
        self.browse_button.configure(state=state)
        self.choose_button.configure(state=state)
        self.output_entry.configure(state=state)
        self.convert_button.configure(state="disabled" if busy else "normal")

    def _update_convert_state(self) -> None:
        state = "normal" if self.input_path.get() and self.output_path.get() else "disabled"
        self.convert_button.configure(state=state)

    def _convert(self) -> None:
        self._set_busy(True)
        self.status.set("Converting...")

        def worker() -> None:
            try:
                convert_file_to_markdown(self.input_path.get(), self.output_path.get())
            except Exception as exc:
                self.root.after(0, lambda: self._finish_with_error(exc))
            else:
                self.root.after(0, self._finish_success)

        threading.Thread(target=worker, daemon=True).start()

    def _finish_success(self) -> None:
        self._set_busy(False)
        self.status.set(f"Done: {self.output_path.get()}")
        self._update_convert_state()

    def _finish_with_error(self, exc: Exception) -> None:
        self._set_busy(False)
        self.status.set(f"Error: {exc}")
        self._update_convert_state()


def main() -> None:
    root = Tk()
    MarkItDownGUI(root)
    root.mainloop()
