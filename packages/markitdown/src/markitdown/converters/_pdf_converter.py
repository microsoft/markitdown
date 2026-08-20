import sys
import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Pattern for MasterFormat-style partial numbering (e.g., ".1", ".2", ".10")
PARTIAL_NUMBERING_PATTERN = re.compile(r"^\.\d+$")


@dataclass(frozen=True)
class _PositionedMarkdownItem:
    top: float
    markdown: str
    order: int


@dataclass(frozen=True)
class _ExtractedPdfImage:
    top: float
    markdown: str


def _merge_partial_numbering_lines(text: str) -> str:
    """
    Post-process extracted text to merge MasterFormat-style partial numbering
    with the following text line.

    MasterFormat documents use partial numbering like:
        .1  The intent of this Request for Proposal...
        .2  Available information relative to...

    Some PDF extractors split these into separate lines:
        .1
        The intent of this Request for Proposal...

    This function merges them back together.
    """
    lines = text.split("\n")
    result_lines: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check if this line is ONLY a partial numbering
        if PARTIAL_NUMBERING_PATTERN.match(stripped):
            # Look for the next non-empty line to merge with
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1

            if j < len(lines):
                # Merge the partial numbering with the next line
                next_line = lines[j].strip()
                result_lines.append(f"{stripped} {next_line}")
                i = j + 1  # Skip past the merged line
            else:
                # No next line to merge with, keep as is
                result_lines.append(line)
                i += 1
        else:
            result_lines.append(line)
            i += 1

    return "\n".join(result_lines)


# Load dependencies
_dependency_exc_info = None
try:
    import pdfminer
    import pdfminer.high_level
    import pdfplumber
except ImportError:
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/pdf",
    "application/x-pdf",
]

ACCEPTED_FILE_EXTENSIONS = [".pdf"]


def _to_markdown_table(table: list[list[str]], include_separator: bool = True) -> str:
    """Convert a 2D list (rows/columns) into a nicely aligned Markdown table.

    Args:
        table: 2D list of cell values
        include_separator: If True, include header separator row (standard markdown).
                          If False, output simple pipe-separated rows.
    """
    if not table:
        return ""

    # Normalize None → ""
    table = [[cell if cell is not None else "" for cell in row] for row in table]

    # Filter out empty rows
    table = [row for row in table if any(cell.strip() for cell in row)]

    if not table:
        return ""

    # Column widths
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*table)]

    def fmt_row(row: list[str]) -> str:
        return (
            "|"
            + "|".join(str(cell).ljust(width) for cell, width in zip(row, col_widths))
            + "|"
        )

    if include_separator:
        header, *rows = table
        md = [fmt_row(header)]
        md.append("|" + "|".join("-" * w for w in col_widths) + "|")
        for row in rows:
            md.append(fmt_row(row))
    else:
        md = [fmt_row(row) for row in table]

    return "\n".join(md)


def _extract_form_content_from_words(page: Any) -> str | None:
    """
    Extract form-style content from a PDF page by analyzing word positions.
    This handles borderless forms/tables where words are aligned in columns.

    Returns markdown with proper table formatting:
    - Tables have pipe-separated columns with header separator rows
    - Non-table content is rendered as plain text

    Returns None if the page doesn't appear to be a form-style document,
    indicating that pdfminer should be used instead for better text spacing.
    """
    words = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3)
    if not words:
        return None

    # Group words by their Y position (rows)
    y_tolerance = 5
    rows_by_y: dict[float, list[dict]] = {}
    for word in words:
        y_key = round(word["top"] / y_tolerance) * y_tolerance
        if y_key not in rows_by_y:
            rows_by_y[y_key] = []
        rows_by_y[y_key].append(word)

    # Sort rows by Y position
    sorted_y_keys = sorted(rows_by_y.keys())
    page_width = page.width if hasattr(page, "width") else 612

    # First pass: analyze each row
    row_info: list[dict] = []
    for y_key in sorted_y_keys:
        row_words = sorted(rows_by_y[y_key], key=lambda w: w["x0"])
        if not row_words:
            continue

        first_x0 = row_words[0]["x0"]
        last_x1 = row_words[-1]["x1"]
        line_width = last_x1 - first_x0
        combined_text = " ".join(w["text"] for w in row_words)

        # Count distinct x-position groups (columns)
        x_positions = [w["x0"] for w in row_words]
        x_groups: list[float] = []
        for x in sorted(x_positions):
            if not x_groups or x - x_groups[-1] > 50:
                x_groups.append(x)

        # Determine row type
        is_paragraph = line_width > page_width * 0.55 and len(combined_text) > 60

        # Check for MasterFormat-style partial numbering (e.g., ".1", ".2")
        # These should be treated as list items, not table rows
        has_partial_numbering = False
        if row_words:
            first_word = row_words[0]["text"].strip()
            if PARTIAL_NUMBERING_PATTERN.match(first_word):
                has_partial_numbering = True

        row_info.append(
            {
                "y_key": y_key,
                "words": row_words,
                "text": combined_text,
                "x_groups": x_groups,
                "is_paragraph": is_paragraph,
                "num_columns": len(x_groups),
                "has_partial_numbering": has_partial_numbering,
            }
        )

    # Collect ALL x-positions from rows with 3+ columns (table-like rows)
    # This gives us the global column structure
    all_table_x_positions: list[float] = []
    for info in row_info:
        if info["num_columns"] >= 3 and not info["is_paragraph"]:
            all_table_x_positions.extend(info["x_groups"])

    if not all_table_x_positions:
        return None

    # Compute adaptive column clustering tolerance based on gap analysis
    all_table_x_positions.sort()

    # Calculate gaps between consecutive x-positions
    gaps = []
    for i in range(len(all_table_x_positions) - 1):
        gap = all_table_x_positions[i + 1] - all_table_x_positions[i]
        if gap > 5:  # Only significant gaps
            gaps.append(gap)

    # Determine optimal tolerance using statistical analysis
    if gaps and len(gaps) >= 3:
        # Use 70th percentile of gaps as threshold (balances precision/recall)
        sorted_gaps = sorted(gaps)
        percentile_70_idx = int(len(sorted_gaps) * 0.70)
        adaptive_tolerance = sorted_gaps[percentile_70_idx]

        # Clamp tolerance to reasonable range [25, 50]
        adaptive_tolerance = max(25, min(50, adaptive_tolerance))
    else:
        # Fallback to conservative value
        adaptive_tolerance = 35

    # Compute global column boundaries using adaptive tolerance
    global_columns: list[float] = []
    for x in all_table_x_positions:
        if not global_columns or x - global_columns[-1] > adaptive_tolerance:
            global_columns.append(x)

    # Adaptive max column check based on page characteristics
    # Calculate average column width
    if len(global_columns) > 1:
        content_width = global_columns[-1] - global_columns[0]
        avg_col_width = content_width / len(global_columns)

        # Forms with very narrow columns (< 30px) are likely dense text
        if avg_col_width < 30:
            return None

        # Compute adaptive max based on columns per inch
        # Typical forms have 3-8 columns per inch
        columns_per_inch = len(global_columns) / (content_width / 72)

        # If density is too high (> 10 cols/inch), likely not a form
        if columns_per_inch > 10:
            return None

        # Adaptive max: allow more columns for wider pages
        # Standard letter is 612pt wide, so scale accordingly
        adaptive_max_columns = int(20 * (page_width / 612))
        adaptive_max_columns = max(15, adaptive_max_columns)  # At least 15

        if len(global_columns) > adaptive_max_columns:
            return None
    else:
        # Single column, not a form
        return None

    # Now classify each row as table row or not
    # A row is a table row if it has words that align with 2+ of the global columns
    for info in row_info:
        if info["is_paragraph"]:
            info["is_table_row"] = False
            continue

        # Rows with partial numbering (e.g., ".1", ".2") are list items, not table rows
        if info["has_partial_numbering"]:
            info["is_table_row"] = False
            continue

        # Count how many global columns this row's words align with
        aligned_columns: set[int] = set()
        for word in info["words"]:
            word_x = word["x0"]
            for col_idx, col_x in enumerate(global_columns):
                if abs(word_x - col_x) < 40:
                    aligned_columns.add(col_idx)
                    break

        # If row uses 2+ of the established columns, it's a table row
        info["is_table_row"] = len(aligned_columns) >= 2

    # Find table regions (consecutive table rows)
    table_regions: list[tuple[int, int]] = []  # (start_idx, end_idx)
    i = 0
    while i < len(row_info):
        if row_info[i]["is_table_row"]:
            start_idx = i
            while i < len(row_info) and row_info[i]["is_table_row"]:
                i += 1
            end_idx = i
            table_regions.append((start_idx, end_idx))
        else:
            i += 1

    # Check if enough rows are table rows (at least 20%)
    total_table_rows = sum(end - start for start, end in table_regions)
    if len(row_info) > 0 and total_table_rows / len(row_info) < 0.2:
        return None

    # Build output - collect table data first, then format with proper column widths
    result_lines: list[str] = []
    num_cols = len(global_columns)

    # Helper function to extract cells from a row
    def extract_cells(info: dict) -> list[str]:
        cells: list[str] = ["" for _ in range(num_cols)]
        for word in info["words"]:
            word_x = word["x0"]
            # Find the correct column using boundary ranges
            assigned_col = num_cols - 1  # Default to last column
            for col_idx in range(num_cols - 1):
                col_end = global_columns[col_idx + 1]
                if word_x < col_end - 20:
                    assigned_col = col_idx
                    break
            if cells[assigned_col]:
                cells[assigned_col] += " " + word["text"]
            else:
                cells[assigned_col] = word["text"]
        return cells

    # Process rows, collecting table data for proper formatting
    idx = 0
    while idx < len(row_info):
        info = row_info[idx]

        # Check if this row starts a table region
        table_region = None
        for start, end in table_regions:
            if idx == start:
                table_region = (start, end)
                break

        if table_region:
            start, end = table_region
            # Collect all rows in this table
            table_data: list[list[str]] = []
            for table_idx in range(start, end):
                cells = extract_cells(row_info[table_idx])
                table_data.append(cells)

            # Calculate column widths for this table
            if table_data:
                col_widths = [
                    max(len(row[col]) for row in table_data) for col in range(num_cols)
                ]
                # Ensure minimum width of 3 for separator dashes
                col_widths = [max(w, 3) for w in col_widths]

                # Format header row
                header = table_data[0]
                header_str = (
                    "| "
                    + " | ".join(
                        cell.ljust(col_widths[i]) for i, cell in enumerate(header)
                    )
                    + " |"
                )
                result_lines.append(header_str)

                # Format separator row
                separator = (
                    "| "
                    + " | ".join("-" * col_widths[i] for i in range(num_cols))
                    + " |"
                )
                result_lines.append(separator)

                # Format data rows
                for row in table_data[1:]:
                    row_str = (
                        "| "
                        + " | ".join(
                            cell.ljust(col_widths[i]) for i, cell in enumerate(row)
                        )
                        + " |"
                    )
                    result_lines.append(row_str)

            idx = end  # Skip to end of table region
        else:
            # Check if we're inside a table region (not at start)
            in_table = False
            for start, end in table_regions:
                if start < idx < end:
                    in_table = True
                    break

            if not in_table:
                # Non-table content
                result_lines.append(info["text"])
            idx += 1

    return "\n".join(result_lines)


def _extract_tables_from_words(page: Any) -> list[list[list[str]]]:
    """
    Extract tables from a PDF page by analyzing word positions.
    This handles borderless tables where words are aligned in columns.

    This function is designed for structured tabular data (like invoices),
    not for multi-column text layouts in scientific documents.
    """
    words = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3)
    if not words:
        return []

    # Group words by their Y position (rows)
    y_tolerance = 5
    rows_by_y: dict[float, list[dict]] = {}
    for word in words:
        y_key = round(word["top"] / y_tolerance) * y_tolerance
        if y_key not in rows_by_y:
            rows_by_y[y_key] = []
        rows_by_y[y_key].append(word)

    # Sort rows by Y position
    sorted_y_keys = sorted(rows_by_y.keys())

    # Find potential column boundaries by analyzing x positions across all rows
    all_x_positions = []
    for words_in_row in rows_by_y.values():
        for word in words_in_row:
            all_x_positions.append(word["x0"])

    if not all_x_positions:
        return []

    # Cluster x positions to find column starts
    all_x_positions.sort()
    x_tolerance_col = 20
    column_starts: list[float] = []
    for x in all_x_positions:
        if not column_starts or x - column_starts[-1] > x_tolerance_col:
            column_starts.append(x)

    # Need at least 3 columns but not too many (likely text layout, not table)
    if len(column_starts) < 3 or len(column_starts) > 10:
        return []

    # Find rows that span multiple columns (potential table rows)
    table_rows = []
    for y_key in sorted_y_keys:
        words_in_row = sorted(rows_by_y[y_key], key=lambda w: w["x0"])

        # Assign words to columns
        row_data = [""] * len(column_starts)
        for word in words_in_row:
            # Find the closest column
            best_col = 0
            min_dist = float("inf")
            for i, col_x in enumerate(column_starts):
                dist = abs(word["x0"] - col_x)
                if dist < min_dist:
                    min_dist = dist
                    best_col = i

            if row_data[best_col]:
                row_data[best_col] += " " + word["text"]
            else:
                row_data[best_col] = word["text"]

        # Only include rows that have content in multiple columns
        non_empty = sum(1 for cell in row_data if cell.strip())
        if non_empty >= 2:
            table_rows.append(row_data)

    # Validate table quality - tables should have:
    # 1. Enough rows (at least 3 including header)
    # 2. Short cell content (tables have concise data, not paragraphs)
    # 3. Consistent structure across rows
    if len(table_rows) < 3:
        return []

    # Check if cells contain short, structured data (not long text)
    long_cell_count = 0
    total_cell_count = 0
    for row in table_rows:
        for cell in row:
            if cell.strip():
                total_cell_count += 1
                # If cell has more than 30 chars, it's likely prose text
                if len(cell.strip()) > 30:
                    long_cell_count += 1

    # If more than 30% of cells are long, this is probably not a table
    if total_cell_count > 0 and long_cell_count / total_cell_count > 0.3:
        return []

    return [table_rows]


def _image_extension_from_bytes(data: bytes) -> str | None:
    """Return a common image extension when bytes are already image-encoded."""
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return "gif"
    if data.startswith(b"II*\x00") or data.startswith(b"MM\x00*"):
        return "tiff"
    if data.startswith(b"\x00\x00\x00\x0cjP  \r\n\x87\n") or data.startswith(
        b"\xff\x4f\xff\x51"
    ):
        return "jp2"
    return None


def _safe_image_bbox(
    image: dict[str, Any], page: Any
) -> tuple[float, float, float, float] | None:
    x0 = float(image.get("x0", 0) or 0)
    x1 = float(image.get("x1", 0) or 0)
    top = float(image.get("top", image.get("y0", 0)) or 0)
    bottom = float(image.get("bottom", image.get("y1", 0)) or 0)

    width = float(getattr(page, "width", x1) or x1)
    height = float(getattr(page, "height", bottom) or bottom)

    x0 = max(0, min(x0, width))
    x1 = max(0, min(x1, width))
    top = max(0, min(top, height))
    bottom = max(0, min(bottom, height))

    if x1 <= x0 or bottom <= top:
        return None

    return (x0, top, x1, bottom)


def _write_rendered_image(
    page: Any, bbox: tuple[float, float, float, float], path: Path
) -> bool:
    try:
        cropped_page = page.crop(bbox)
        page_image = cropped_page.to_image(resolution=600)
        page_image.original.save(path, format="PNG")
        return path.exists() and path.stat().st_size > 0
    except Exception:
        return False


def _write_stream_image(
    image: dict[str, Any], path_without_suffix: Path
) -> Path | None:
    stream = image.get("stream")
    if stream is None or not hasattr(stream, "get_data"):
        return None

    try:
        data = stream.get_data()
    except Exception:
        return None

    if not data:
        return None

    extension = _image_extension_from_bytes(data)
    if extension is None:
        return None

    path = path_without_suffix.with_suffix(f".{extension}")
    try:
        path.write_bytes(data)
    except Exception:
        return None

    if path.exists() and path.stat().st_size > 0:
        return path
    return None


def _extract_pdf_images_from_page(
    page: Any,
    *,
    page_num: int,
    images_dir: Path,
) -> list[_ExtractedPdfImage]:
    images = list(getattr(page, "images", []) or [])
    if not images and hasattr(page, "objects"):
        images = list(getattr(page, "objects", {}).get("image", []) or [])

    extracted: list[_ExtractedPdfImage] = []
    for image_idx, image in enumerate(images, start=1):
        bbox = _safe_image_bbox(image, page)
        top = bbox[1] if bbox is not None else float(image.get("top", 0) or 0)
        path_without_suffix = images_dir / f"page{page_num}-image{image_idx}"

        image_path = _write_stream_image(image, path_without_suffix)
        if image_path is None and bbox is not None:
            rendered_path = path_without_suffix.with_suffix(".png")
            if _write_rendered_image(page, bbox, rendered_path):
                image_path = rendered_path

        if image_path is None:
            continue

        rel_path = Path("images") / image_path.name
        alt_text = f"Image {image_idx} on page {page_num}"
        extracted.append(
            _ExtractedPdfImage(
                top=top,
                markdown=f"![{alt_text}]({rel_path.as_posix()})",
            )
        )

    return extracted


def _extract_text_items_from_page(page: Any) -> list[_PositionedMarkdownItem]:
    form_content = _extract_form_content_from_words(page)
    if form_content is not None:
        return [_PositionedMarkdownItem(top=0, markdown=form_content, order=0)]

    try:
        lines = page.extract_text_lines()
        items = [
            _PositionedMarkdownItem(
                top=float(line.get("top", idx) or idx),
                markdown=str(line.get("text", "")).strip(),
                order=idx,
            )
            for idx, line in enumerate(lines)
            if str(line.get("text", "")).strip()
        ]
        if items:
            return items
    except Exception:
        pass

    try:
        words = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3)
        if words:
            rows_by_y: dict[float, list[dict]] = {}
            y_tolerance = 5.0
            for word in words:
                y_key = round(float(word["top"]) / y_tolerance) * y_tolerance
                rows_by_y.setdefault(y_key, []).append(word)

            items = []
            for order, y_key in enumerate(sorted(rows_by_y.keys())):
                row_words = sorted(rows_by_y[y_key], key=lambda w: w["x0"])
                text = " ".join(w["text"] for w in row_words).strip()
                if text:
                    items.append(
                        _PositionedMarkdownItem(top=y_key, markdown=text, order=order)
                    )
            if items:
                return items
    except Exception:
        pass

    text = page.extract_text() or ""
    return [
        _PositionedMarkdownItem(top=float(idx), markdown=line.strip(), order=idx)
        for idx, line in enumerate(text.splitlines())
        if line.strip()
    ]


def _convert_pdf_with_image_extraction(
    pdf_bytes: io.BytesIO,
    *,
    output_dir: str | Path,
) -> str:
    output_root = Path(output_dir)
    images_dir = output_root / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    chunks: list[str] = []
    with pdfplumber.open(pdf_bytes) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            page_num = page_idx + 1
            try:
                items: list[_PositionedMarkdownItem] = _extract_text_items_from_page(
                    page
                )
                image_items = _extract_pdf_images_from_page(
                    page,
                    page_num=page_num,
                    images_dir=images_dir,
                )

                for image_order, image in enumerate(image_items):
                    items.append(
                        _PositionedMarkdownItem(
                            top=image.top,
                            markdown=image.markdown,
                            order=10_000 + image_order,
                        )
                    )

                items.sort(key=lambda item: (item.top, item.order))
                page_markdown = "\n\n".join(item.markdown for item in items).strip()
                if page_markdown:
                    chunks.append(page_markdown)
            finally:
                page.close()

    return "\n\n".join(chunks).strip()


class PdfConverter(DocumentConverter):
    """
    Converts PDFs to Markdown.
    Supports extracting tables into aligned Markdown format (via pdfplumber).
    Falls back to pdfminer if pdfplumber is missing or fails.
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
        if _dependency_exc_info is not None:
            missing_dependency_exception = _dependency_exc_info[1]
            assert missing_dependency_exception is not None
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pdf",
                    feature="pdf",
                )
            ) from missing_dependency_exception.with_traceback(_dependency_exc_info[2])

        assert isinstance(file_stream, io.IOBase)

        # Read file stream into BytesIO for compatibility with pdfplumber
        pdf_bytes = io.BytesIO(file_stream.read())

        extract_images = bool(kwargs.get("extract_images", False))
        output_dir = kwargs.get("output_dir")

        if extract_images:
            if output_dir is None:
                raise ValueError("output_dir is required when extract_images=True")

            try:
                markdown = _convert_pdf_with_image_extraction(
                    pdf_bytes,
                    output_dir=output_dir,
                )
            except Exception:
                pdf_bytes.seek(0)
                markdown = pdfminer.high_level.extract_text(pdf_bytes)
        else:
            try:
                # Single pass: check every page for form-style content.
                # Pages with tables/forms get rich extraction; plain-text
                # pages are collected separately. page.close() is called
                # after each page to free pdfplumber's cached objects and
                # keep memory usage constant regardless of page count.
                markdown_chunks: list[str] = []
                form_page_count = 0
                plain_page_indices: list[int] = []

                with pdfplumber.open(pdf_bytes) as pdf:
                    for page_idx, page in enumerate(pdf.pages):
                        page_content = _extract_form_content_from_words(page)

                        if page_content is not None:
                            form_page_count += 1
                            if page_content.strip():
                                markdown_chunks.append(page_content)
                        else:
                            plain_page_indices.append(page_idx)
                            text = page.extract_text()
                            if text and text.strip():
                                markdown_chunks.append(text.strip())

                        page.close()  # Free cached page data immediately

                # If no pages had form-style content, use pdfminer for
                # the whole document (better text spacing for prose).
                if form_page_count == 0:
                    pdf_bytes.seek(0)
                    markdown = pdfminer.high_level.extract_text(pdf_bytes)
                else:
                    markdown = "\n\n".join(markdown_chunks).strip()

            except Exception:
                # Fallback if pdfplumber fails
                pdf_bytes.seek(0)
                markdown = pdfminer.high_level.extract_text(pdf_bytes)

        # Fallback if still empty
        if not markdown:
            pdf_bytes.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_bytes)

        # Post-process to merge MasterFormat-style partial numbering with following text
        markdown = _merge_partial_numbering_lines(markdown)

        return DocumentConverterResult(markdown=markdown)
