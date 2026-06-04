from __future__ import annotations

import threading
from pathlib import Path
from tkinter import filedialog
from typing import Protocol

import customtkinter as ctk

from ._base_converter import DocumentConverterResult
from ._markitdown import MarkItDown

APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"


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
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("MarkItDown GUI")
        self.root.geometry("760x430")
        self.root.minsize(680, 390)
        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.status = ctk.StringVar(value="Choose an input file and output path.")

        self._build()
        self._update_convert_state()

    def _build(self) -> None:
        self.root.configure(fg_color="#0f172a")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        frame = ctk.CTkFrame(self.root, fg_color="#111827", corner_radius=18)
        frame.grid(row=0, column=0, sticky="nsew", padx=28, pady=28)
        frame.columnconfigure(0, weight=1)

        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(28, 18))
        header.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="MarkItDown",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#f8fafc",
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            header,
            text="Convert one document into Markdown",
            font=ctk.CTkFont(size=14),
            text_color="#94a3b8",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        fields = ctk.CTkFrame(frame, fg_color="#0b1220", corner_radius=14)
        fields.grid(row=1, column=0, sticky="ew", padx=28, pady=(0, 18))
        fields.columnconfigure(1, weight=1)

        ctk.CTkLabel(
            fields,
            text="Input file",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#e5e7eb",
        ).grid(row=0, column=0, sticky="w", padx=(18, 12), pady=(18, 8))
        self.input_entry = ctk.CTkEntry(
            fields,
            textvariable=self.input_path,
            state="disabled",
            height=40,
            fg_color="#111827",
            border_color="#334155",
            text_color="#f8fafc",
        )
        self.input_entry.grid(row=0, column=1, sticky="ew", padx=0, pady=(18, 8))
        self.browse_button = ctk.CTkButton(
            fields,
            text="Browse",
            command=self._browse_input,
            width=108,
            height=40,
        )
        self.browse_button.grid(row=0, column=2, padx=(12, 18), pady=(18, 8))

        ctk.CTkLabel(
            fields,
            text="Output file",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#e5e7eb",
        ).grid(row=1, column=0, sticky="w", padx=(18, 12), pady=(8, 18))
        self.output_entry = ctk.CTkEntry(
            fields,
            textvariable=self.output_path,
            height=40,
            fg_color="#111827",
            border_color="#334155",
            text_color="#f8fafc",
        )
        self.output_entry.grid(row=1, column=1, sticky="ew", padx=0, pady=(8, 18))
        self.choose_button = ctk.CTkButton(
            fields,
            text="Choose",
            command=self._choose_output,
            width=108,
            height=40,
            fg_color="#334155",
            hover_color="#475569",
        )
        self.choose_button.grid(row=1, column=2, padx=(12, 18), pady=(8, 18))

        actions = ctk.CTkFrame(frame, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", padx=28, pady=(0, 18))
        actions.columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            actions,
            textvariable=self.status,
            font=ctk.CTkFont(size=13),
            text_color="#cbd5e1",
            anchor="w",
            justify="left",
            wraplength=480,
        )
        self.status_label.grid(row=0, column=0, sticky="ew", padx=(0, 18))

        self.convert_button = ctk.CTkButton(
            actions,
            text="Convert",
            command=self._convert,
            width=148,
            height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.convert_button.grid(row=0, column=1, sticky="e")

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
    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)
    root = ctk.CTk()
    MarkItDownGUI(root)
    root.mainloop()
