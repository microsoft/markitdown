# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import os
import sys
import codecs
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from importlib.metadata import entry_points
from typing import Any, Dict, List, Optional

from ._markitdown import MarkItDown, StreamInfo, DocumentConverterResult
from .converters import ContentUnderstandingFileType


class MarkItDownGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MarkItDown - Document Converter")
        self.geometry("950x700")
        self.minsize(800, 600)

        # Configure Tkinter ttk styles
        self.style = ttk.Style()
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self._create_widgets()

    def _create_widgets(self):
        # Notebook / Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Main Conversion
        self.tab_convert = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_convert, text=" Conversion ")

        # Tab 2: Azure Cloud Services
        self.tab_cloud = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_cloud, text=" Azure Cloud Services ")

        # Tab 3: Plugins
        self.tab_plugins = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_plugins, text=" Plugins ")

        # Tab 4: Help
        self.tab_help = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_help, text=" Help ")

        # Tab 5: About
        self.tab_about = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_about, text=" About ")

        self._setup_convert_tab()
        self._setup_cloud_tab()
        self._setup_plugins_tab()
        self._setup_help_tab()
        self._setup_about_tab()

    def _setup_convert_tab(self):
        # Input File Frame
        file_frame = ttk.LabelFrame(self.tab_convert, text=" Input File ", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        self.var_input_file = tk.StringVar()
        entry_input = ttk.Entry(file_frame, textvariable=self.var_input_file)
        entry_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        btn_browse_input = ttk.Button(file_frame, text="Browse...", command=self._browse_input_file)
        btn_browse_input.pack(side=tk.RIGHT)

        # General Options Frame
        opts_frame = ttk.LabelFrame(self.tab_convert, text=" Hints & Options ", padding=10)
        opts_frame.pack(fill=tk.X, padx=10, pady=5)

        # Options Row 1: Hints (Extension, MIME, Charset)
        row1 = ttk.Frame(opts_frame)
        row1.pack(fill=tk.X, pady=2)

        ttk.Label(row1, text="Extension Hint (-x):").pack(side=tk.LEFT, padx=(0, 2))
        self.var_extension = tk.StringVar()
        entry_ext = ttk.Entry(row1, textvariable=self.var_extension, width=10)
        entry_ext.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(row1, text="MIME Type Hint (-m):").pack(side=tk.LEFT, padx=(0, 2))
        self.var_mimetype = tk.StringVar()
        entry_mime = ttk.Entry(row1, textvariable=self.var_mimetype, width=20)
        entry_mime.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(row1, text="Charset Hint (-c):").pack(side=tk.LEFT, padx=(0, 2))
        self.var_charset = tk.StringVar()
        entry_charset = ttk.Entry(row1, textvariable=self.var_charset, width=12)
        entry_charset.pack(side=tk.LEFT)

        # Options Row 2: Checkboxes
        row2 = ttk.Frame(opts_frame)
        row2.pack(fill=tk.X, pady=(8, 2))

        self.var_use_plugins = tk.BooleanVar(value=True)
        chk_plugins = ttk.Checkbutton(row2, text="Enable 3rd-party Plugins (-p)", variable=self.var_use_plugins)
        chk_plugins.pack(side=tk.LEFT, padx=(0, 20))

        self.var_keep_data_uris = tk.BooleanVar(value=False)
        chk_data_uris = ttk.Checkbutton(row2, text="Keep Data URIs / Base64 images (--keep-data-uris)", variable=self.var_keep_data_uris)
        chk_data_uris.pack(side=tk.LEFT)

        # Output File Frame
        output_file_frame = ttk.LabelFrame(self.tab_convert, text=" Output File (Optional -o) ", padding=10)
        output_file_frame.pack(fill=tk.X, padx=10, pady=5)

        self.var_output_file = tk.StringVar()
        entry_output = ttk.Entry(output_file_frame, textvariable=self.var_output_file)
        entry_output.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        btn_browse_output = ttk.Button(output_file_frame, text="Save As...", command=self._browse_output_file)
        btn_browse_output.pack(side=tk.RIGHT)

        # Action Frame (Convert)
        action_frame = ttk.Frame(self.tab_convert)
        action_frame.pack(fill=tk.X, padx=10, pady=8)

        self.btn_convert = ttk.Button(action_frame, text="Convert to Markdown", command=self._start_conversion)
        self.btn_convert.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)

        self.lbl_status = ttk.Label(action_frame, text="Ready.", font=("Segoe UI", 9, "italic"))
        self.lbl_status.pack(side=tk.RIGHT, padx=10)

        # Output Result Viewer (Markdown Result)
        result_frame = ttk.LabelFrame(self.tab_convert, text=" Markdown Result ", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.txt_result = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.txt_result.pack(fill=tk.BOTH, expand=True)

    def _setup_cloud_tab(self):
        # Document Intelligence Frame
        docintel_frame = ttk.LabelFrame(self.tab_cloud, text=" Azure Document Intelligence (-d / --use-docintel) ", padding=10)
        docintel_frame.pack(fill=tk.X, padx=10, pady=10)

        self.var_use_docintel = tk.BooleanVar(value=False)
        chk_docintel = ttk.Checkbutton(docintel_frame, text="Use Document Intelligence instead of offline conversion", variable=self.var_use_docintel, command=self._on_cloud_toggle)
        chk_docintel.pack(anchor=tk.W, pady=(0, 5))

        row_di = ttk.Frame(docintel_frame)
        row_di.pack(fill=tk.X, pady=2)
        ttk.Label(row_di, text="Endpoint (-e / --endpoint):").pack(side=tk.LEFT, padx=(0, 5))
        self.var_docintel_endpoint = tk.StringVar()
        self.entry_di_ep = ttk.Entry(row_di, textvariable=self.var_docintel_endpoint)
        self.entry_di_ep.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Content Understanding Frame
        cu_frame = ttk.LabelFrame(self.tab_cloud, text=" Azure Content Understanding (--use-cu) ", padding=10)
        cu_frame.pack(fill=tk.X, padx=10, pady=10)

        self.var_use_cu = tk.BooleanVar(value=False)
        chk_cu = ttk.Checkbutton(cu_frame, text="Use Azure Content Understanding", variable=self.var_use_cu, command=self._on_cloud_toggle)
        chk_cu.pack(anchor=tk.W, pady=(0, 5))

        row_cu1 = ttk.Frame(cu_frame)
        row_cu1.pack(fill=tk.X, pady=2)
        ttk.Label(row_cu1, text="Endpoint (--cu-endpoint):").pack(side=tk.LEFT, padx=(0, 5))
        self.var_cu_endpoint = tk.StringVar()
        self.entry_cu_ep = ttk.Entry(row_cu1, textvariable=self.var_cu_endpoint)
        self.entry_cu_ep.pack(side=tk.LEFT, fill=tk.X, expand=True)

        row_cu2 = ttk.Frame(cu_frame)
        row_cu2.pack(fill=tk.X, pady=5)
        ttk.Label(row_cu2, text="Analyzer ID (--cu-analyzer):").pack(side=tk.LEFT, padx=(0, 5))
        self.var_cu_analyzer = tk.StringVar()
        self.entry_cu_anz = ttk.Entry(row_cu2, textvariable=self.var_cu_analyzer, width=25)
        self.entry_cu_anz.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(row_cu2, text="File Types (--cu-file-types):").pack(side=tk.LEFT, padx=(0, 5))
        self.var_cu_file_types = tk.StringVar()
        self.entry_cu_types = ttk.Entry(row_cu2, textvariable=self.var_cu_file_types, width=25)
        self.entry_cu_types.pack(side=tk.LEFT)
        ttk.Label(row_cu2, text="(e.g., pdf,jpeg,mp4)", font=("Segoe UI", 8, "italic")).pack(side=tk.LEFT, padx=5)

        self._on_cloud_toggle()

    def _setup_plugins_tab(self):
        frame = ttk.Frame(self.tab_plugins, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Section 1: Installed Plugins
        lbl_inst = ttk.Label(frame, text="Installed Environment Plugins:", font=("Segoe UI", 10, "bold"))
        lbl_inst.pack(anchor=tk.W, pady=(0, 5))

        top_bar = ttk.Frame(frame)
        top_bar.pack(fill=tk.X, pady=(0, 5))

        btn_refresh = ttk.Button(top_bar, text="Refresh List", command=self._refresh_plugins)
        btn_refresh.pack(side=tk.LEFT)

        self.lbl_plugin_status = ttk.Label(top_bar, text="", font=("Segoe UI", 9, "italic"))
        self.lbl_plugin_status.pack(side=tk.LEFT, padx=10)

        self.txt_plugins = scrolledtext.ScrolledText(frame, wrap=tk.NONE, font=("Consolas", 10), height=8)
        self.txt_plugins.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Section 2: Plugin Installer
        lbl_install = ttk.Label(frame, text="Install New Plugin:", font=("Segoe UI", 10, "bold"))
        lbl_install.pack(anchor=tk.W, pady=(5, 5))

        install_frame = ttk.LabelFrame(frame, text=" Install via PyPI Package or Local Path ", padding=10)
        install_frame.pack(fill=tk.X, pady=5)

        ttk.Label(install_frame, text="Package Name (PyPI) or Plugin Path:").pack(anchor=tk.W, pady=(0, 5))

        row_inst = ttk.Frame(install_frame)
        row_inst.pack(fill=tk.X)

        self.var_plugin_to_install = tk.StringVar()
        entry_pkg = ttk.Entry(row_inst, textvariable=self.var_plugin_to_install)
        entry_pkg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        btn_browse_pkg = ttk.Button(row_inst, text="Select Local Folder...", command=self._browse_plugin_dir)
        btn_browse_pkg.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_install_pkg = ttk.Button(row_inst, text="Install Plugin", command=self._install_plugin)
        self.btn_install_pkg.pack(side=tk.RIGHT)

        # Quick Shortcuts
        sug_frame = ttk.Frame(install_frame)
        sug_frame.pack(fill=tk.X, pady=(8, 0))
        ttk.Label(sug_frame, text="Quick Shortcuts:", font=("Segoe UI", 9, "italic")).pack(side=tk.LEFT, padx=(0, 5))

        btn_sug_ocr = ttk.Button(sug_frame, text="markitdown-ocr (Local)", command=lambda: self._select_local_package("packages/markitdown-ocr"))
        btn_sug_ocr.pack(side=tk.LEFT, padx=2)

        btn_sug_sample = ttk.Button(sug_frame, text="markitdown-sample-plugin (Local)", command=lambda: self._select_local_package("packages/markitdown-sample-plugin"))
        btn_sug_sample.pack(side=tk.LEFT, padx=2)

        self._refresh_plugins()

    def _browse_plugin_dir(self):
        folder = filedialog.askdirectory(title="Select Plugin Folder")
        if folder:
            self.var_plugin_to_install.set(folder)

    def _select_local_package(self, rel_path: str):
        abs_path = os.path.abspath(os.path.join(os.getcwd(), rel_path))
        if os.path.exists(abs_path):
            self.var_plugin_to_install.set(abs_path)
        else:
            self.var_plugin_to_install.set(rel_path)

    def _install_plugin(self):
        pkg = self.var_plugin_to_install.get().strip()
        if not pkg:
            messagebox.showwarning("Warning", "Please enter a PyPI package name or select a local plugin folder.")
            return

        self.btn_install_pkg.config(state=tk.DISABLED)
        self.lbl_plugin_status.config(text=f"Installing '{pkg}' via pip...")

        threading.Thread(target=self._run_pip_install, args=(pkg,), daemon=True).start()

    def _run_pip_install(self, pkg: str):
        import subprocess

        cmd = [sys.executable, "-m", "pip", "install"]
        if os.path.isdir(pkg):
            cmd.extend(["-e", pkg])
        else:
            cmd.append(pkg)

        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                self.after(0, self._on_install_success, pkg)
            else:
                self.after(0, self._on_install_error, pkg, res.stderr or res.stdout)
        except Exception as e:
            self.after(0, self._on_install_error, pkg, str(e))

    def _on_install_success(self, pkg: str):
        self.btn_install_pkg.config(state=tk.NORMAL)
        self.lbl_plugin_status.config(text=f"Plugin '{pkg}' installed successfully!")
        messagebox.showinfo("Success", f"Plugin '{pkg}' installed successfully!\n\nThe plugin list has been updated.")
        self._refresh_plugins()

    def _on_install_error(self, pkg: str, err: str):
        self.btn_install_pkg.config(state=tk.NORMAL)
        self.lbl_plugin_status.config(text="Plugin installation failed.")
        messagebox.showerror("Installation Error", f"Failed to install plugin '{pkg}':\n\n{err}")

    def _refresh_plugins(self):
        self.txt_plugins.config(state=tk.NORMAL)
        self.txt_plugins.delete("1.0", tk.END)

        try:
            plugin_entry_points = list(entry_points(group="markitdown.plugin"))
        except Exception:
            plugin_entry_points = []

        if not plugin_entry_points:
            self.txt_plugins.insert(tk.END, "No 3rd-party plugins installed in current environment.\n\n")
            self.txt_plugins.insert(tk.END, "Use the section below to install new plugins (local or via PyPI).")
        else:
            for ep in plugin_entry_points:
                self.txt_plugins.insert(tk.END, f"- {ep.name:<25} (package: {ep.value})\n")

        self.txt_plugins.config(state=tk.DISABLED)

    def _setup_help_tab(self):
        frame = ttk.Frame(self.tab_help, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)

        txt_help = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Segoe UI", 10))
        txt_help.pack(fill=tk.BOTH, expand=True)

        help_content = (
            "MARKITDOWN GUI QUICK GUIDE\n"
            "---------------------------\n\n"
            "1. SIMPLE CONVERSION:\n"
            "   - On the 'Conversion' tab, click 'Browse...' and select your file (PDF, DOCX, XLSX, PPTX, HTML, Audio, etc.).\n"
            "   - (Optional) Choose output path via 'Save As...'.\n"
            "   - Click 'Convert to Markdown'. Formatted text will display directly on screen.\n\n"
            "2. HINTS & ADVANCED OPTIONS:\n"
            "   - Extension Hint (-x): Force conversion assuming a specific file extension (e.g., '.pdf').\n"
            "   - MIME Type Hint (-m): Specify exact Content-Type (e.g., 'application/pdf').\n"
            "   - Charset Hint (-c): Text file encoding (e.g., 'utf-8', 'latin1').\n"
            "   - Enable 3rd-party Plugins (-p): Allow installed plugins to extend conversion capabilities.\n"
            "   - Keep Data URIs (--keep-data-uris): Preserve Base64 images/data URIs in Markdown output.\n\n"
            "3. AZURE CLOUD SERVICES:\n"
            "   - On the 'Azure Cloud Services' tab, enable Document Intelligence or Content Understanding.\n"
            "   - Enter Service Endpoints and Analyzer IDs for advanced cloud document extraction.\n\n"
            "4. PLUGIN MANAGEMENT:\n"
            "   - On the 'Plugins' tab, view installed extensions or install new plugins via PyPI / local folders.\n\n"
            "5. COMMAND LINE EQUIVALENT:\n"
            "   - markitdown example.pdf -o example.md\n"
            "   - markitdown --gui\n"
            "   - markitdown-gui\n"
        )
        txt_help.insert(tk.END, help_content)
        txt_help.config(state=tk.DISABLED)

    def _setup_about_tab(self):
        frame = ttk.Frame(self.tab_about, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        lbl_title = ttk.Label(frame, text="MarkItDown", font=("Segoe UI", 18, "bold"))
        lbl_title.pack(anchor=tk.W, pady=(0, 2))

        from .__about__ import __version__
        lbl_version = ttk.Label(frame, text=f"Version {__version__}", font=("Segoe UI", 10, "italic"))
        lbl_version.pack(anchor=tk.W, pady=(0, 15))

        lbl_desc = ttk.Label(
            frame,
            text=(
                "MarkItDown is a utility for converting various file formats "
                "(PDF, Word, Excel, PowerPoint, HTML, Audio, Images, ZIP, etc.) into Markdown.\n\n"
                "This Graphical User Interface (GUI) is designed to provide an easy and intuitive way "
                "to access all command-line features of MarkItDown."
            ),
            font=("Segoe UI", 10),
            wraplength=700,
            justify=tk.LEFT
        )
        lbl_desc.pack(anchor=tk.W, pady=(0, 20))

        info_frame = ttk.LabelFrame(frame, text=" Project Information ", padding=10)
        info_frame.pack(fill=tk.X, pady=10)

        info_text = (
            "• License: MIT\n"
            "• Official Repository: https://github.com/microsoft/markitdown\n"
            "• Plugin Support: Dynamically extensible module (#markitdown-plugin)\n"
            "• User Interface: Built with native Python Tkinter"
        )
        lbl_info = ttk.Label(info_frame, text=info_text, font=("Segoe UI", 9))
        lbl_info.pack(anchor=tk.W)

    def _on_cloud_toggle(self):
        if self.var_use_docintel.get():
            self.var_use_cu.set(False)
        elif self.var_use_cu.get():
            self.var_use_docintel.set(False)

        self.entry_di_ep.config(state=tk.NORMAL if self.var_use_docintel.get() else tk.DISABLED)
        self.entry_cu_ep.config(state=tk.NORMAL if self.var_use_cu.get() else tk.DISABLED)
        self.entry_cu_anz.config(state=tk.NORMAL if self.var_use_cu.get() else tk.DISABLED)
        self.entry_cu_types.config(state=tk.NORMAL if self.var_use_cu.get() else tk.DISABLED)

    def _browse_input_file(self):
        path = filedialog.askopenfilename(title="Select File to Convert")
        if path:
            self.var_input_file.set(path)

    def _browse_output_file(self):
        path = filedialog.asksaveasfilename(
            title="Save Markdown File",
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("All Files", "*.*")]
        )
        if path:
            self.var_output_file.set(path)

    def _start_conversion(self):
        input_path = self.var_input_file.get().strip()
        if not input_path:
            messagebox.showwarning("Warning", "Please select an input file.")
            return

        if not os.path.exists(input_path):
            messagebox.showerror("Error", f"File not found:\n{input_path}")
            return

        if self.var_use_docintel.get() and not self.var_docintel_endpoint.get().strip():
            messagebox.showerror("Error", "Document Intelligence Endpoint is required when option is active.")
            return

        if self.var_use_cu.get() and not self.var_cu_endpoint.get().strip():
            messagebox.showerror("Error", "Content Understanding Endpoint (--cu-endpoint) is required when option is active.")
            return

        self.btn_convert.config(state=tk.DISABLED)
        self.lbl_status.config(text="Converting...")
        self.txt_result.delete("1.0", tk.END)

        threading.Thread(target=self._run_conversion, args=(input_path,), daemon=True).start()

    def _run_conversion(self, input_path: str):
        try:
            ext_hint = self.var_extension.get().strip().lower() or None
            if ext_hint and not ext_hint.startswith("."):
                ext_hint = "." + ext_hint

            mime_hint = self.var_mimetype.get().strip() or None
            if mime_hint and mime_hint.count("/") != 1:
                raise ValueError(f"Invalid MIME type: {mime_hint}")

            charset_hint = self.var_charset.get().strip() or None
            if charset_hint:
                try:
                    charset_hint = codecs.lookup(charset_hint).name
                except LookupError:
                    raise ValueError(f"Invalid charset: {charset_hint}")

            stream_info = None
            if ext_hint or mime_hint or charset_hint:
                stream_info = StreamInfo(extension=ext_hint, mimetype=mime_hint, charset=charset_hint)

            enable_plugins = self.var_use_plugins.get()

            if self.var_use_docintel.get():
                markitdown = MarkItDown(
                    enable_plugins=enable_plugins,
                    docintel_endpoint=self.var_docintel_endpoint.get().strip()
                )
            elif self.var_use_cu.get():
                cu_kwargs: Dict[str, Any] = {
                    "cu_endpoint": self.var_cu_endpoint.get().strip()
                }
                analyzer = self.var_cu_analyzer.get().strip()
                if analyzer:
                    cu_kwargs["cu_analyzer_id"] = analyzer

                cu_types_str = self.var_cu_file_types.get().strip()
                if cu_types_str:
                    type_names = [t.strip().lower() for t in cu_types_str.split(",") if t.strip()]
                    cu_types = []
                    for name in type_names:
                        cu_types.append(ContentUnderstandingFileType(name))
                    cu_kwargs["cu_file_types"] = cu_types

                markitdown = MarkItDown(enable_plugins=enable_plugins, **cu_kwargs)
            else:
                markitdown = MarkItDown(enable_plugins=enable_plugins)

            result = markitdown.convert(
                input_path,
                stream_info=stream_info,
                keep_data_uris=self.var_keep_data_uris.get()
            )

            markdown_text = result.markdown

            output_path = self.var_output_file.get().strip()
            if output_path:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)

            self.after(0, self._on_conversion_success, markdown_text, output_path)

        except Exception as e:
            self.after(0, self._on_conversion_error, str(e))

    def _on_conversion_success(self, markdown_text: str, output_path: Optional[str]):
        self.txt_result.insert(tk.END, markdown_text)
        self.btn_convert.config(state=tk.NORMAL)
        self.lbl_status.config(text="Conversion completed successfully!")
        if output_path:
            messagebox.showinfo("Success", f"Conversion completed and saved to:\n{output_path}")

    def _on_conversion_error(self, error_msg: str):
        self.btn_convert.config(state=tk.NORMAL)
        self.lbl_status.config(text="Conversion error.")
        messagebox.showerror("Conversion Error", error_msg)


def main():
    app = MarkItDownGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
