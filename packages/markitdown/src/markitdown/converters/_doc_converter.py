import sys
import struct
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import olefile
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
    "application/vnd.ms-word",
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]


class DocConverter(DocumentConverter):
    """
    Converts legacy DOC files to Markdown. This converter handles the older Microsoft Word binary format (.doc)
    as opposed to the newer XML-based format (.docx).
    
    This converter uses pure Python libraries to extract text from DOC files without requiring
    external system dependencies like LibreOffice or antiword.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
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
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Check the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".doc",
                    feature="doc",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        # Extract text from the DOC file
        try:
            # check if this is actually a DOC file using olefile
            if not olefile.isOleFile(file_stream):
                return DocumentConverterResult(
                    markdown="Error: Not a valid Microsoft Word DOC file"
                )
            
            text_content = self._extract_doc_text(file_stream)
            
            # Clean up the extracted text
            if text_content:
                markdown_content = self._clean_text(text_content)
            else:
                markdown_content = "Unable to extract readable text from this DOC file."

            return DocumentConverterResult(markdown=markdown_content)
            
        except Exception as e:
            return DocumentConverterResult(
                markdown=f"Error converting DOC file: {str(e)}"
            )

    def _extract_doc_text(self, file_stream: BinaryIO) -> str:
        """Extract text from DOC file using olefile to parse the OLE structure."""
        try:
            # Reset stream position
            file_stream.seek(0)
            
            ole = olefile.OleFileIO(file_stream)
            
            try:
                if ole.exists('WordDocument'):
                    word_stream = ole.openstream('WordDocument')
                    data = word_stream.read()
                    
                    text = self._extract_text_from_word_stream(data)
                    
                    return text
                else:
                    return self._extract_readable_strings(file_stream)
                    
            finally:
                ole.close()
                
        except Exception:
            # Fallback to basic string extraction
            return self._extract_readable_strings(file_stream)

    def _extract_text_from_word_stream(self, data: bytes) -> str:
        """Extract text from the WordDocument stream using pattern matching."""
        try:
            # Convert to string and filter out non-printable characters
            text_parts = []
            current_word = ""
            
            i = 0
            while i < len(data):
                byte = data[i]
                
                # Look for printable ASCII characters
                if 32 <= byte <= 126:  # Printable ASCII
                    current_word += chr(byte)
                elif byte == 0:  # Null terminator often separates words
                    if len(current_word) > 2:  # Only keep words longer than 2 chars
                        text_parts.append(current_word)
                    current_word = ""
                else:
                    # Check for Unicode characters (UTF-16)
                    if i + 1 < len(data) and data[i + 1] == 0:
                        # Potential UTF-16 little endian character
                        if 32 <= byte <= 126:
                            current_word += chr(byte)
                        i += 1  # Skip the null byte
                    else:
                        # End current word
                        if len(current_word) > 2:
                            text_parts.append(current_word)
                        current_word = ""
                
                i += 1
            
            # Add the last word
            if len(current_word) > 2:
                text_parts.append(current_word)
            
            return " ".join(text_parts)
            
        except Exception:
            return ""

    def _extract_readable_strings(self, file_stream: BinaryIO) -> str:
        """Fallback method to extract readable strings from the file."""
        try:
            file_stream.seek(0)
            data = file_stream.read()
            
            text_parts = []
            current_string = ""
            
            for byte in data:
                # Look for printable characters
                if 32 <= byte <= 126:
                    current_string += chr(byte)
                else:
                    if len(current_string) > 4:  # Only keep strings longer than 4 characters
                        # Filter out common binary patterns
                        if not self._is_likely_binary_string(current_string):
                            text_parts.append(current_string)
                    current_string = ""
            
            # Add the last string
            if len(current_string) > 4:
                if not self._is_likely_binary_string(current_string):
                    text_parts.append(current_string)
            
            return " ".join(text_parts)
            
        except Exception:
            return ""

    def _is_likely_binary_string(self, s: str) -> bool:
        """Check if a string is likely binary data rather than readable text."""
        # Filter out strings that are likely binary data
        binary_indicators = [
            # Common file format signatures
            'Microsoft', 'Word', 'MSWordDoc',
            # Common binary patterns
            'Root Entry', 'SummaryInformation', 'DocumentSummaryInformation',
            # Strings with too many special characters
        ]
        
        # Skip strings that are mostly special characters
        special_char_count = sum(1 for c in s if not c.isalnum() and c != ' ')
        if len(s) > 0 and special_char_count / len(s) > 0.7:
            return True
        
        # Skip known binary indicators
        for indicator in binary_indicators:
            if indicator in s:
                return True
        
        return False

    def _clean_text(self, text: str) -> str:
        """Clean and format the extracted text."""
        if not text:
            return ""
        
        # Split into words and reconstruct sentences
        words = text.split()
        if not words:
            return ""
        
        # Basic sentence reconstruction
        sentences = []
        current_sentence = []
        
        for word in words:
            current_sentence.append(word)
            
            # Simple sentence boundary detection
            if word.endswith(('.', '!', '?')) or len(current_sentence) > 20:
                if current_sentence:
                    sentences.append(' '.join(current_sentence))
                current_sentence = []
        
        # Add remaining words as a sentence
        if current_sentence:
            sentences.append(' '.join(current_sentence))
        
        # Join sentences with proper spacing
        return '\n\n'.join(sentences) if sentences else text.strip()