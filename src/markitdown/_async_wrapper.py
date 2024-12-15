"""Async wrapper for MarkItDown."""
import asyncio
from functools import partial
from typing import Optional, Union

from ._markitdown import MarkItDown, DocumentConverterResult

class AsyncMarkItDown:
    """Async wrapper for MarkItDown that runs operations in a thread pool."""

    def __init__(self, markitdown: Optional[MarkItDown] = None):
        """Initialize the async wrapper.
        
        Args:
            markitdown: Optional MarkItDown instance to wrap. If not provided,
                       a new instance will be created.
        """
        self._markitdown = markitdown or MarkItDown()
        self._loop = asyncio.get_event_loop()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        pass

    async def convert(self, file_path: str, **kwargs) -> DocumentConverterResult:
        """Convert a file to markdown asynchronously.
        
        This runs the synchronous convert operation in a thread pool to avoid
        blocking the event loop.
        
        Args:
            file_path: Path to the file to convert
            **kwargs: Additional arguments to pass to the converter
            
        Returns:
            DocumentConverterResult containing the converted markdown
        """
        # Run the synchronous convert in a thread pool
        func = partial(self._markitdown.convert, file_path, **kwargs)
        return await self._loop.run_in_executor(None, func)
