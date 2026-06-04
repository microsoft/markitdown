from __future__ import annotations

import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal, Protocol

import customtkinter as ctk

from ._base_converter import DocumentConverterResult
from ._markitdown import MarkItDown

APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"


@dataclass(frozen=True)
class DirectoryEntry:
    path: Path
    name: str
    is_dir: bool


def list_directory_entries(directory: str | Path) -> list[DirectoryEntry]:
    path = Path(directory).expanduser().resolve()
    entries = [
        DirectoryEntry(child, child.name, child.is_dir())
        for child in path.iterdir()
        if not child.name.startswith("__pycache__")
    ]
    return sorted(entries, key=lambda entry: (not entry.is_dir, entry.name.lower()))


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
        ModernFilePicker(
            self.root,
            mode="open",
            title="Choose input file",
            initial_path=Path(self.input_path.get()).parent
            if self.input_path.get()
            else Path.cwd(),
            on_select=self._set_input_file,
        )

    def _choose_output(self) -> None:
        initial = Path(self.output_path.get()) if self.output_path.get() else None
        ModernFilePicker(
            self.root,
            mode="save",
            title="Choose output Markdown file",
            initial_path=initial.parent if initial else Path.cwd(),
            initial_name=initial.name if initial else "output.md",
            on_select=lambda path: self.output_path.set(str(path)),
        )

    def _set_input_file(self, path: Path) -> None:
        self.input_path.set(str(path))
        self.output_path.set(str(path.with_suffix(".md")))
        self.status.set("Ready to convert.")

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


class ModernFilePicker(ctk.CTkToplevel):
    def __init__(
        self,
        parent: ctk.CTk,
        *,
        mode: Literal["open", "save"],
        title: str,
        initial_path: str | Path,
        on_select: Callable[[Path], None],
        initial_name: str = "",
    ):
        super().__init__(parent)
        self.mode = mode
        self.current_dir = Path(initial_path).expanduser().resolve()
        self.on_select = on_select
        self.filename = ctk.StringVar(value=initial_name)
        self.path_label = ctk.StringVar(value=str(self.current_dir))

        self.title(title)
        self.geometry("760x520")
        self.minsize(640, 440)
        self.configure(fg_color="#0f172a")
        self.transient(parent)
        self.grab_set()

        self._build(title)
        self._refresh()

    def _build(self, title: str) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=22, pady=(22, 12))
        header.columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#f8fafc",
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(
            header,
            text="Up",
            width=74,
            fg_color="#334155",
            hover_color="#475569",
            command=self._go_up,
        ).grid(row=0, column=2, sticky="e")

        path_bar = ctk.CTkEntry(
            header,
            textvariable=self.path_label,
            state="disabled",
            height=36,
            fg_color="#111827",
            border_color="#334155",
            text_color="#cbd5e1",
        )
        path_bar.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(12, 0))

        self.list_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#111827",
            corner_radius=14,
            scrollbar_button_color="#334155",
            scrollbar_button_hover_color="#475569",
        )
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=22, pady=(0, 14))
        self.list_frame.columnconfigure(0, weight=1)

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=22, pady=(0, 22))
        footer.columnconfigure(0, weight=1)

        self.name_entry = ctk.CTkEntry(
            footer,
            textvariable=self.filename,
            placeholder_text="File name",
            height=40,
            fg_color="#111827",
            border_color="#334155",
            text_color="#f8fafc",
        )
        self.name_entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        ctk.CTkButton(
            footer,
            text="Cancel",
            width=100,
            height=40,
            fg_color="#334155",
            hover_color="#475569",
            command=self.destroy,
        ).grid(row=0, column=1, padx=(0, 10))
        ctk.CTkButton(
            footer,
            text="Open" if self.mode == "open" else "Save",
            width=100,
            height=40,
            command=self._confirm,
        ).grid(row=0, column=2)

    def _refresh(self) -> None:
        self.path_label.set(str(self.current_dir))
        for child in self.list_frame.winfo_children():
            child.destroy()

        for row, entry in enumerate(list_directory_entries(self.current_dir)):
            label = f"{'Folder' if entry.is_dir else 'File'}  {entry.name}"
            button = ctk.CTkButton(
                self.list_frame,
                text=label,
                anchor="w",
                height=38,
                fg_color="transparent",
                hover_color="#1e293b",
                text_color="#e5e7eb",
                command=lambda item=entry: self._choose_entry(item),
            )
            button.grid(row=row, column=0, sticky="ew", padx=8, pady=3)

    def _go_up(self) -> None:
        parent = self.current_dir.parent
        if parent != self.current_dir:
            self.current_dir = parent
            self._refresh()

    def _choose_entry(self, entry: DirectoryEntry) -> None:
        if entry.is_dir:
            self.current_dir = entry.path
            self._refresh()
            return
        self.filename.set(entry.name)
        if self.mode == "open":
            self._confirm()

    def _confirm(self) -> None:
        name = self.filename.get().strip()
        if not name:
            return
        selected = self.current_dir / name
        if self.mode == "open" and not selected.is_file():
            return
        if self.mode == "save" and selected.suffix == "":
            selected = selected.with_suffix(".md")
        self.on_select(selected)
        self.destroy()


def main() -> None:
    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)
    root = ctk.CTk()
    MarkItDownGUI(root)
    root.mainloop()
