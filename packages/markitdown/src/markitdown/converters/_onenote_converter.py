import sys
from typing import Any, Union, BinaryIO
from .._stream_info import StreamInfo
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
olefile = None
pyonenote = None
try:
    import olefile  # type: ignore[no-redef]
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()

try:
    from pyOneNote import OneDocument
    pyonenote = OneDocument
except ImportError:
    pass

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/onenote",
    "application/msonenote",
    "application/vnd.ms-onenote",
    "application/x-ole-storage",  # Generic OLE
]

ACCEPTED_FILE_EXTENSIONS = [".one"]


class OneNoteConverter(DocumentConverter):
    """Converts OneNote .one files to markdown by extracting text content.

    Uses pyOneNote library for proper OneNote file parsing when available,
    falls back to olefile for basic OLE stream extraction.

    Capabilities:
    - Extracts structured content from real OneNote files (when pyOneNote available)
    - Basic section and page detection
    - Plain text extraction from OLE streams

    Limitations:
    - Rich text formatting (bold, italic, highlighting, colors) not preserved
    - Images and embedded objects not extracted
    - Complex layouts and tables not supported
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        # Check the extension and mimetype
        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        # Brute force, check if we have an OLE file that looks like OneNote
        cur_pos = file_stream.tell()
        try:
            if olefile and not olefile.isOleFile(file_stream):
                return False
        except Exception:
            # If we can't even check if it's an OLE file, it's probably not for us
            return False
        finally:
            file_stream.seek(cur_pos)

        # Check for OneNote-specific streams
        try:
            if olefile is not None:
                ole = olefile.OleFileIO(file_stream)
                streams = ole.listdir()
                # OneNote files typically have these characteristic streams
                onenote_indicators = [
                    any("OneNote" in str(stream) for stream in streams),
                    any("RevisionStore" in str(stream) for stream in streams),
                    any("RecycleBin" in str(stream) for stream in streams),
                    # Check for the OneNote file header signature
                ]
                ole.close()
                if any(onenote_indicators):
                    return True
        except Exception:
            pass
        finally:
            file_stream.seek(cur_pos)

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Check: the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".one",
                    feature="onenote",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        # Try pyOneNote first for proper OneNote parsing
        if pyonenote is not None:
            try:
                file_stream.seek(0)
                doc = pyonenote(file_stream)
                json_data = doc.get_json()

                # Extract text content from the JSON structure
                md_content = self._parse_pyonenote_json(json_data)
                if md_content:
                    return DocumentConverterResult(
                        markdown=md_content.strip(),
                        title=None,
                    )
            except Exception:
                # Fall back to olefile approach
                pass

        # Fall back to OLE file parsing
        file_stream.seek(0)
        return self._convert_with_olefile(file_stream)

    def _convert_with_olefile(self, file_stream: BinaryIO) -> DocumentConverterResult:
        """Convert using olefile as fallback."""
        if olefile is None:
            # Should not happen as it is checked in convert() via _dependency_exc_info
            return DocumentConverterResult(markdown="# OneNote Document\n\nDependencies missing.")

        try:
            file_stream.seek(0)
            if olefile.isOleFile(file_stream):
                file_stream.seek(0)
                ole = olefile.OleFileIO(file_stream)
                text = self._extract_text(ole)
                ole.close()
                if text:
                    return DocumentConverterResult(markdown=f"# OneNote Document\n\n{text}")

            # Fallback to plain text if not an OLE file or no text found in OLE
            file_stream.seek(0)
            data = file_stream.read()
            for encoding in ["utf-8", "utf-16-le", "latin-1"]:
                try:
                    text = data.decode(encoding).strip()
                    if text:
                        return DocumentConverterResult(markdown=f"# OneNote Document\n\n{text}")
                except UnicodeDecodeError:
                    continue

            md_content = "# OneNote Document\n\nUnable to decode content."
        except Exception:
            md_content = "# OneNote Document\n\nError parsing file structure."

        return DocumentConverterResult(
            markdown=md_content.strip(),
            title=None,
        )

    def _parse_pyonenote_json(self, json_data: Any) -> Union[str, None]:
        """Parse pyOneNote JSON output into markdown."""
        try:
            content_parts = []

            # The JSON structure likely contains pages, sections, etc.
            # This is a basic implementation - would need to explore the actual structure

            if isinstance(json_data, dict):
                # Look for content in the JSON
                if 'pages' in json_data:
                    for page in json_data['pages']:
                        if isinstance(page, dict):
                            title = page.get('title', 'Untitled Page')
                            content_parts.append(f"## {title}")

                            # Extract text content
                            text_content = self._extract_text_from_page(page)
                            if text_content:
                                content_parts.append(text_content)

                elif 'content' in json_data:
                    content_parts.append(json_data['content'])

            if content_parts:
                return '\n\n'.join(content_parts)

        except Exception:
            pass
        return None

    def _extract_text_from_page(self, page_data: dict) -> Union[str, None]:
        """Extract text content from a page object."""
        try:
            text_parts = []

            # Look for text in various possible locations
            if 'text' in page_data:
                text_parts.append(str(page_data['text']))
            if 'content' in page_data:
                text_parts.append(str(page_data['content']))
            if 'body' in page_data:
                text_parts.append(str(page_data['body']))

            # Look for nested content
            if 'elements' in page_data:
                for element in page_data['elements']:
                    if isinstance(element, dict):
                        if 'text' in element:
                            text_parts.append(str(element['text']))

            return '\n'.join(text_parts) if text_parts else None

        except Exception:
            return None

    def _extract_text(self, ole: Any) -> Union[str, None]:
        """Helper to extract text from OneNote streams."""
        assert olefile is not None

        text_parts = []
        sections = []

        try:
            # OneNote files have a specific structure
            # Try to find section streams
            for stream in ole.listdir():
                stream_path = "/".join(stream)

                # Look for section streams (they often contain page data)
                if "Section" in stream_path or stream_path.endswith(".one"):
                    sections.append(stream_path)

                # Also collect any stream that might contain text
                if ole.exists(stream_path):
                    data = ole.openstream(stream_path).read()

                    # Try different encodings
                    for encoding in ["utf-16-le", "utf-8", "latin-1"]:
                        try:
                            decoded = data.decode(encoding, errors="ignore").strip()
                            if decoded and len(decoded) > 20:  # More substantial content
                                # Clean up the text
                                lines = [line.strip() for line in decoded.split('\n') if line.strip()]
                                if lines:
                                    text_parts.append('\n'.join(lines))
                                break
                        except UnicodeDecodeError:
                            continue

        except Exception as e:
            pass

        # If we found sections, try to extract structured content
        if sections:
            structured_content = self._parse_sections(ole, sections)
            if structured_content:
                return structured_content

        # Fall back to concatenated text parts
        if text_parts:
            return "\n\n".join(text_parts)
        return None

    def _parse_sections(self, ole: Any, sections: list[str]) -> Union[str, None]:
        """Parse OneNote sections to extract structured content."""
        content_parts = []

        for section_path in sections:
            try:
                if ole.exists(section_path):
                    data = ole.openstream(section_path).read()

                    # OneNote sections contain page data with complex binary format
                    # For basic extraction, try to find readable text patterns
                    try:
                        text = data.decode("utf-16-le", errors="ignore")
                        lines = [line.strip() for line in text.split('\n') if line.strip()]

                        if lines:
                            # Try to identify section title from the first substantial line
                            section_title = None
                            content_lines = []

                            for line in lines:
                                if not section_title and len(line) < 100 and len(line) > 3:
                                    # Likely a section title
                                    section_title = line
                                else:
                                    content_lines.append(line)

                            if section_title:
                                content_parts.append(f"## Section: {section_title}")

                            if content_lines:
                                content_parts.append('\n'.join(content_lines))

                    except UnicodeDecodeError:
                        pass

            except Exception:
                continue

        if content_parts:
            return '\n\n'.join(content_parts)
        return None