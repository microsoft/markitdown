import re
from typing import BinaryIO, Any, Optional, Set, Union
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/x-latex",
    "application/x-tex",
    "text/x-tex",
    "text/x-latex",
]

ACCEPTED_FILE_EXTENSIONS = [".tex", ".latex", ".ltx"]

INLINE_MATH_PATTERN = re.compile(r"\$([^\$]+)\$")
COMMENT_PATTERN = re.compile(r"%.*$", re.MULTILINE)

LATEX_TEXT_COMMANDS = [
    (re.compile(r"\\textbf\{([^}]+)\}"), r"**\1**"),
    (re.compile(r"\\textit\{([^}]+)\}"), r"*\1*"),
    (re.compile(r"\\texttt\{([^}]+)\}"), r"`\1`"),
    (re.compile(r"\\textmd\{([^}]+)\}"), r"\1"),
    (re.compile(r"\\textsf\{([^}]+)\}"), r"\1"),
    (re.compile(r"\\rmfamily\{([^}]+)\}"), r"\1"),
    (re.compile(r"\\sffamily\{([^}]+)\}"), r"\1"),
    (re.compile(r"\\ttfamily\{([^}]+)\}"), r"`\1`"),
    (re.compile(r"\\bfseries\{([^}]+)\}"), r"**\1**"),
    (re.compile(r"\\itshape\{([^}]+)\}"), r"*\1*"),
    (re.compile(r"\\scshape\{([^}]+)\}"), r"\1"),
    (re.compile(r"\\upshape\{([^}]+)\}"), r"\1"),
    (re.compile(r"\\emph\{([^}]+)\}"), r"*\1*"),
    (re.compile(r"\\TeX\b"), "LaTeX"),
    (re.compile(r"\\LaTeX\b"), "LaTeX"),
    (re.compile(r"\\LaTeXe\b"), "LaTeX"),
]

LATEX_ACCENTS = [
    (re.compile(r"\\\"([a-zA-Z])"), r"\1"),
    (re.compile(r"\\`([a-zA-Z])"), r"\1"),
    (re.compile(r"\\'([a-zA-Z])"), r"\1"),
    (re.compile(r"\\^([a-zA-Z])"), r"\1"),
    (re.compile(r"\\~([a-zA-Z])"), r"\1"),
]

LATEX_SPECIAL_CHARS = [
    (re.compile(r"\\--"), "—"),
    (re.compile(r"\\---"), "—"),
    (re.compile(r"\\&"), "&"),
    (re.compile(r"\\\$"), "$"),
    (re.compile(r"\\%"), "%"),
    (re.compile(r"\\#"), "#"),
]

LATEX_SPACES = [
    (re.compile(r"\\,"), " "),
    (re.compile(r"\\:"), " "),
    (re.compile(r"\\;"), " "),
    (re.compile(r"\\ "), " "),
    (re.compile(r"\\quad"), "  "),
    (re.compile(r"\\qquad"), "    "),
]

LATEX_SYMBOLS = [
    (re.compile(r"\\ldots"), "..."),
    (re.compile(r"\\dots"), "..."),
    (re.compile(r"\\cdots"), "···"),
    (re.compile(r"\\vdots"), "⋮"),
    (re.compile(r"\\ddots"), "⋱"),
]

LATEX_REFS = [
    (re.compile(r"\\ref\{([^}]+)\}"), r"[@\1]"),
    (re.compile(r"\\eqref\{([^}]+)\}"), r"(@\1)"),
    (re.compile(r"\\pageref\{([^}]+)\}"), r"[page \1]"),
    (re.compile(r"\\cite(?:\[([^\]]*)\])?\{([^}]+)\}"), r"[@\2]"),
    (re.compile(r"\\citep(?:\[([^\]]*)\])?\{([^}]+)\}"), r"[@\2]"),
    (re.compile(r"\\citet(?:\[([^\]]*)\])?\{([^}]+)\}"), r"@\2"),
]

LATEX_URLS = [
    (re.compile(r"\\url\{([^}]+)\}"), r"<\1>"),
    (re.compile(r"\\href\{([^}]+)\}\{([^}]+)\}"), r"[\2](\1)"),
]

LATEX_NEWLINES = [
    (re.compile(r"\\newline\b"), "\n"),
    (re.compile(r"\\\\"), "\n"),
    (re.compile(r"\\par\b"), "\n\n"),
]

LATEX_QUOTES = [
    (re.compile(r"``"), '"'),
    (re.compile(r"''"), '"'),
    (re.compile(r"`([a-zA-Z])"), r"'\1"),
]

LATEX_SUBSUPERSCRIPT = [
    (re.compile(r"\^{([^}]+)}"), r"^\1"),
    (re.compile(r"\_{([^}]+)}"), r"_\1"),
    (re.compile(r"\\textsuperscript\{([^}]+)\}"), r"^\1"),
    (re.compile(r"\\textsubscript\{([^}]+)\}"), r"_\1"),
]

LATEX_OTHER = [
    (re.compile(r"\\em\b"), "*"),
    (re.compile(r"\{([^{}]*)\}"), r"\1"),
    (re.compile(r"~"), " "),
]


class LaTeXConverter(DocumentConverter):
    """
    Converts LaTeX files to Markdown.

    Handles:
    - Document structure (part, chapter, section, subsection, etc.)
    - Lists (itemize, enumerate, description)
    - Tables (tabular, table)
    - Figures (figure)
    - Mathematics (inline $...$ and display $$...$$)
    - Cross-references and citations
    - Basic text formatting
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        content = file_stream.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8", errors="replace")

        parser = LaTeXParser()
        markdown = parser.parse(content)

        return DocumentConverterResult(markdown=markdown)


class LaTeXParser:
    """
    Parser for LaTeX documents that converts them to Markdown.
    """

    def __init__(self):
        self.output: list[str] = []
        self.title: Optional[str] = None
        self.author: Optional[str] = None
        self.packages: Set[str] = set()
        self.footnotes: list[str] = []

    def parse(self, content: str) -> str:
        content = self._preprocess(content)
        lines = content.split("\n")
        self._parse_lines(lines)
        result = "\n".join(self.output)
        return self._postprocess(result)

    def _preprocess(self, content: str) -> str:
        content = COMMENT_PATTERN.sub("", content)
        content = content.replace("\r\n", "\n").replace("\r", "\n")
        return content

    def _postprocess(self, content: str) -> str:
        content = re.sub(r"\n{3,}", "\n\n", content)
        return content.strip()

    def _parse_lines(self, lines: list[str]) -> None:
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            if self._handle_command(line):
                i += 1
                continue

            env_result = self._handle_environment(line, lines, i)
            if isinstance(env_result, int) and not isinstance(env_result, bool):
                i = env_result
                continue

            if env_result:
                i += 1
                continue

            if self._handle_end_environment(line):
                i += 1
                continue

            self._handle_text_line(line)
            i += 1

    def _handle_end_environment(self, line: str) -> bool:
        env_match = re.match(r"\\end\{([a-zA-Z*]+)\}", line)
        if env_match:
            return True
        return False

    def _handle_command(self, line: str) -> bool:
        if line.startswith("\\"):
            if self._handle_document_class(line):
                return True
            if self._handle_package(line):
                return True
            if self._handle_title(line):
                return True
            if self._handle_author(line):
                return True
            if self._handle_maketitle(line):
                return True
            if self._handle_sectioning(line):
                return True
            if self._handle_list_item(line):
                return True
            if self._handle_footnote(line):
                return True
            if self._handle_display_math_brackets(line):
                return True
            if self._handle_hline(line):
                return True

        return False

    def _handle_environment(self, line: str, lines: list[str], i: int) -> Union[bool, int]:
        env_match = re.match(r"\\begin\{([a-zA-Z*]+)\}", line)
        if not env_match:
            return False

        env_name = env_match.group(1)

        if env_name == "document":
            return True

        if env_name in ("itemize", "enumerate", "description"):
            return True

        if env_name.startswith("end{"):
            return True

        if env_name in ("figure", "table", "center", "flushleft", "flushright"):
            return True

        if env_name in ("tabular", "array"):
            return self._handle_tabular(lines, i)

        if env_name in ("equation", "eqnarray", "align", "gather", "multline"):
            return self._handle_equation(lines, i, env_name)

        if env_name == "abstract":
            return self._handle_abstract(lines, i)

        if env_name in ("verbatim", "listing"):
            return self._handle_verbatim(lines, i)

        if env_name.startswith("end{"):
            return True

        return False

    def _find_end(self, lines: list[str], start_idx: int, env_name: str) -> int:
        i = start_idx + 1
        while i < len(lines):
            line = lines[i].strip()
            if re.match(rf"\\end\{{{env_name}\}}", line):
                break
            i += 1
        return i

    def _handle_document_class(self, line: str) -> bool:
        if re.match(r"\\documentclass(?:\[[^\]]*\])?\{[^}]+\}", line):
            return True
        return False

    def _handle_package(self, line: str) -> bool:
        match = re.match(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}", line)
        if match:
            self.packages.add(match.group(1))
            return True
        return False

    def _handle_title(self, line: str) -> bool:
        match = re.match(r"\\title\{([^}]+)\}", line)
        if match:
            self.title = self._clean_latex_text(match.group(1))
            return True
        return False

    def _handle_author(self, line: str) -> bool:
        match = re.match(r"\\author\{([^}]+)\}", line)
        if match:
            self.author = self._clean_latex_text(match.group(1))
            return True
        return False

    def _handle_maketitle(self, line: str) -> bool:
        if "\\maketitle" in line:
            if self.title:
                self.output.append(f"# {self.title}\n")
            if self.author:
                self.output.append(f"\n**Author:** {self.author}\n")
            return True
        return False

    def _handle_sectioning(self, line: str) -> bool:
        section_commands = {
            "part": 0,
            "chapter": 1,
            "section": 2,
            "subsection": 3,
            "subsubsection": 4,
            "paragraph": 5,
            "subparagraph": 6,
        }

        for cmd, level in section_commands.items():
            pattern = rf"\\{cmd}(?:\[[^\]]*\])?\{{([^}}]+)\}}"
            match = re.match(pattern, line)
            if match:
                title = self._clean_latex_text(match.group(1))
                self.output.append(f"\n{'#' * level} {title}\n")
                return True

        return False

    def _handle_list_item(self, line: str) -> bool:
        if re.match(r"\\item(?:\s|\[|$)", line):
            item_text = re.sub(r"\\item(?:\s*\[([^\]]*)\])?\s*", "", line).strip()
            if item_text:
                self.output.append(f"- {self._clean_latex_text(item_text)}\n")
            else:
                self.output.append("- \n")
            return True
        return False

    def _handle_footnote(self, line: str) -> bool:
        match = re.search(r"\\footnote(?:\[[^\]]*\])?\{([^}]+)\}", line)
        if match:
            footnote_text = self._clean_latex_text(match.group(1))
            footnote_num = len(self.footnotes) + 1
            self.footnotes.append(footnote_text)
            self.output.append(f"^{footnote_num}^")
            return True
        return False

    def _handle_display_math_brackets(self, line: str) -> bool:
        match = re.match(r"\\\[(.*)\\\]$", line)
        if match:
            content = self._clean_latex_text(match.group(1))
            self.output.append(f"\n$$\n{content}\n$$\n")
            return True
        return False

    def _handle_hline(self, line: str) -> bool:
        if re.match(r"\\hline\s*$", line) or re.match(r"\\hline$", line):
            return True
        return False

    def _handle_tabular(self, lines: list[str], start_idx: int) -> int:
        table_lines = []
        i = start_idx + 1

        while i < len(lines):
            line = lines[i].strip()

            if re.match(r"\\end\{(?:tabular|array)\}", line):
                break

            if line and not line.startswith("%"):
                if "\\hline" in line:
                    line = line.replace("\\hline", "").strip()

                if not line:
                    i += 1
                    continue

                line = re.sub(r"\s*&\s*", " | ", line)
                line = re.sub(r"\s*\\\\\s*$", "", line)
                line = re.sub(r"\s*\\\\\s*", "", line)

                if line:
                    table_lines.append(line)

            i += 1

        if table_lines:
            self._format_table(table_lines)

        return i

    def _format_table(self, table_lines: list[str]) -> None:
        if not table_lines:
            return

        self.output.append("\n")
        col_count = 0
        for idx, row in enumerate(table_lines):
            row = row.strip()
            if not row:
                continue

            if row.startswith("|") and row.endswith("|"):
                row = row[1:-1]

            cols = [c.strip() for c in row.split("|")]
            cols = [self._clean_latex_text(c) for c in cols]

            if idx == 0:
                col_count = len(cols)
                for col in cols:
                    self.output.append(f"| {col} ")
                self.output.append("|\n")

                separator = "| " + " | ".join(["---"] * col_count) + " |"
                self.output.append(f"{separator}\n")
            else:
                for col in cols:
                    col_text = col if col else ""
                    self.output.append(f"| {col_text} ")
                if len(cols) < col_count:
                    for _ in range(col_count - len(cols)):
                        self.output.append("| ")
                self.output.append("|\n")

    def _handle_equation(self, lines: list[str], start_idx: int, env_name: str) -> int:
        content_parts = []
        i = start_idx + 1

        while i < len(lines):
            line = lines[i].strip()

            if re.match(rf"\\end\{{{env_name}\}}", line):
                break

            if line:
                line = re.sub(r"\\\\\s*$", "", line)
                line = re.sub(r"\\\\\s*", " ", line)
                content_parts.append(line)

            i += 1

        if content_parts:
            content = " ".join(content_parts)
            content = self._clean_latex_text(content)
            self.output.append(f"\n$$\n{content}\n$$\n")

        return i

    def _handle_abstract(self, lines: list[str], start_idx: int) -> int:
        content_parts = []
        i = start_idx + 1

        while i < len(lines):
            line = lines[i].strip()

            if re.match(r"\\end\{abstract\}", line):
                i += 1
                break

            if line:
                content_parts.append(self._clean_latex_text(line))

            i += 1

        if content_parts:
            self.output.append("\n## Abstract\n\n")
            self.output.append(" ".join(content_parts))
            self.output.append("\n")

        return i

    def _handle_verbatim(self, lines: list[str], start_idx: int) -> int:
        env_name = self._get_env_name(lines[start_idx])
        content_parts = []
        i = start_idx + 1

        while i < len(lines):
            line = lines[i]

            if re.match(rf"\\end\{{{env_name}\}}", line):
                break

            content_parts.append(line.rstrip())
            i += 1

        if content_parts:
            self.output.append("\n```\n")
            self.output.extend(content_parts)
            self.output.append("\n```\n")

        return i

    def _get_env_name(self, line: str) -> str:
        match = re.match(r"\\begin\{([a-zA-Z*]+)\}", line)
        if match:
            return match.group(1)
        return ""

    def _handle_text_line(self, line: str) -> None:
        line = self._process_inline_math(line)
        line = self._clean_latex_text(line)

        if line.strip():
            self.output.append(f"{line}\n")

    def _process_inline_math(self, line: str) -> str:
        def math_replacer(match):
            content = match.group(1)
            return f"${content}$"

        return INLINE_MATH_PATTERN.sub(math_replacer, line)

    def _clean_latex_text(self, text: str) -> str:
        if not text:
            return ""

        result = text

        for pattern, replacement in LATEX_TEXT_COMMANDS:
            result = pattern.sub(replacement, result)

        for pattern, replacement in LATEX_ACCENTS:
            result = pattern.sub(replacement, result)

        for pattern, replacement in LATEX_SPECIAL_CHARS:
            result = pattern.sub(replacement, result)

        for pattern, replacement in LATEX_SPACES:
            result = pattern.sub(replacement, result)

        for pattern, replacement in LATEX_SYMBOLS:
            result = pattern.sub(replacement, result)

        for pattern, replacement in LATEX_REFS:
            result = pattern.sub(replacement, result)

        for pattern, replacement in LATEX_URLS:
            result = pattern.sub(replacement, result)

        for pattern, replacement in LATEX_NEWLINES:
            result = pattern.sub(replacement, result)

        for pattern, replacement in LATEX_SUBSUPERSCRIPT:
            result = pattern.sub(replacement, result)

        for pattern, replacement in LATEX_QUOTES:
            result = pattern.sub(replacement, result)

        for pattern, replacement in LATEX_OTHER:
            result = pattern.sub(replacement, result)

        result = re.sub(r"\s+", " ", result)

        return result.strip()
