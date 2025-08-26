import json
import time
import re
import bs4
from typing import Any, BinaryIO, Dict, List, Union
from urllib.parse import parse_qs, urlparse, unquote

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

# Optional YouTube transcription support
try:
    # Suppress some warnings on library import
    import warnings

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=SyntaxWarning)
        # Patch submitted upstream to fix the SyntaxWarning
        from youtube_transcript_api import YouTubeTranscriptApi

    IS_YOUTUBE_TRANSCRIPT_CAPABLE = True
except ModuleNotFoundError:
    IS_YOUTUBE_TRANSCRIPT_CAPABLE = False


ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/html",
    "application/xhtml",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".html",
    ".htm",
]


class YouTubeConverter(DocumentConverter):
    """Handle YouTube specially, focusing on the video title, description, and transcript."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        """
        Make sure we're dealing with HTML content *from* YouTube.
        """
        url = stream_info.url or ""
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        url = unquote(url)
        url = url.replace(r"\?", "?").replace(r"\=", "=")

        if not url.startswith("https://www.youtube.com/watch?"):
            # Not a YouTube URL
            return False

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        # Not HTML content
        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Parse the stream
        encoding = "utf-8" if stream_info.charset is None else stream_info.charset
        soup = bs4.BeautifulSoup(file_stream, "html.parser", from_encoding=encoding)

        # Read the meta tags
        metadata: Dict[str, str] = {}

        if soup.title and soup.title.string:
            metadata["title"] = soup.title.string

        for meta in soup(["meta"]):
            if not isinstance(meta, bs4.Tag):
                continue

            for a in meta.attrs:
                if a in ["itemprop", "property", "name"]:
                    key = str(meta.get(a, ""))
                    content = str(meta.get("content", ""))
                    if key and content:  # Only add non-empty content
                        metadata[key] = content
                    break

        # Try reading the description
        try:
            for script in soup(["script"]):
                if not isinstance(script, bs4.Tag):
                    continue
                if not script.string:  # Skip empty scripts
                    continue
                content = script.string
                if "ytInitialData" in content:
                    match = re.search(r"var ytInitialData = ({.*?});", content)
                    if match:
                        data = json.loads(match.group(1))
                        attrdesc = self._findKey(data, "attributedDescriptionBodyText")
                        if attrdesc and isinstance(attrdesc, dict):
                            metadata["description"] = str(attrdesc.get("content", ""))
                    break
        except Exception as e:
            print(f"Error extracting description: {e}")
            pass

        # Start preparing the page
        webpage_text = "# YouTube\n"

        title = self._get(metadata, ["title", "og:title", "name"])  # type: ignore
        assert isinstance(title, str)

        if title:
            webpage_text += f"\n## {title}\n"

        stats = ""
        views = self._get(metadata, ["interactionCount"])  # type: ignore
        if views:
            stats += f"- **Views:** {views}\n"

        keywords = self._get(metadata, ["keywords"])  # type: ignore
        if keywords:
            stats += f"- **Keywords:** {keywords}\n"

        runtime = self._get(metadata, ["duration"])  # type: ignore
        if runtime:
            stats += f"- **Runtime:** {runtime}\n"

        if len(stats) > 0:
            webpage_text += f"\n### Video Metadata\n{stats}\n"

        description = self._get(metadata, ["description", "og:description"])  # type: ignore
        if description:
            webpage_text += f"\n### Description\n{description}\n"

        if IS_YOUTUBE_TRANSCRIPT_CAPABLE:
            ytt_api = YouTubeTranscriptApi()
            transcript_text = ""
            parsed_url = urlparse(stream_info.url)  # type: ignore
            params = parse_qs(parsed_url.query)  # type: ignore
            if "v" in params and params["v"][0]:
                video_id = str(params["v"][0])
                transcript_list = ytt_api.list(video_id)
                languages = ["en"]
                for transcript in transcript_list:
                    languages.append(transcript.language_code)
                    break
                try:
                    youtube_transcript_languages = kwargs.get(
                        "youtube_transcript_languages", languages
                    )
                    # Retry the transcript fetching operation
                    transcript = self._retry_operation(
                        lambda: ytt_api.fetch(
                            video_id, languages=youtube_transcript_languages
                        ),
                        retries=3,  # Retry 3 times
                        delay=2,  # 2 seconds delay between retries
                    )

                    if transcript:
                        transcript_text = " ".join(
                            [part.text for part in transcript]
                        )  # type: ignore
                except Exception as e:
                    # No transcript available
                    if len(languages) == 1:
                        print(f"Error fetching transcript: {e}")
                    else:
                        # Translate transcript into first kwarg
                        transcript = (
                            transcript_list.find_transcript(languages)
                            .translate(youtube_transcript_languages[0])
                            .fetch()
                        )
                        transcript_text = " ".join([part.text for part in transcript])
            if transcript_text:
                webpage_text += f"\n### Transcript\n{transcript_text}\n"

        title = title if title else (soup.title.string if soup.title else "")
        assert isinstance(title, str)

        return DocumentConverterResult(
            markdown=webpage_text,
            title=title,
        )

    def _get(
        self,
        metadata: Dict[str, str],
        keys: List[str],
        default: Union[str, None] = None,
    ) -> Union[str, None]:
        """Get first non-empty value from metadata matching given keys."""
        for k in keys:
            if k in metadata:
                return metadata[k]
        return default

    def _findKey(self, json: Any, key: str) -> Union[str, None]:  # TODO: Fix json type
        """Recursively search for a key in nested dictionary/list structures."""
        if isinstance(json, list):
            for elm in json:
                ret = self._findKey(elm, key)
                if ret is not None:
                    return ret
        elif isinstance(json, dict):
            for k, v in json.items():
                if k == key:
                    return json[k]
                if result := self._findKey(v, key):
                    return result
        return None

    def _retry_operation(self, operation, retries=3, delay=2):
        """Retries the operation if it fails."""
        attempt = 0
        while attempt < retries:
            try:
                return operation()  # Attempt the operation
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)  # Wait before retrying
                attempt += 1
        # If all attempts fail, raise the last exception
        raise Exception(f"Operation failed after {retries} attempts.")
