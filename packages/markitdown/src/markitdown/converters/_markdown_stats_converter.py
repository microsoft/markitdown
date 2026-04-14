"""
Utility module for computing statistics about a Markdown document.
This is a post-processing enhancer, not a file converter.
"""

import re
from typing import Dict


def get_document_stats(markdown_text: str) -> Dict[str, int]:
    """
    Compute statistics about a Markdown document.

    Parameters:
    - markdown_text: The Markdown text to analyze.

    Returns:
    - A dict with the following keys:
        - word_count: number of words
        - char_count: number of characters
        - line_count: number of lines
        - heading_count: number of ATX headings (# / ## / etc.)
        - code_block_count: number of fenced code blocks (``` ... ```)
        - link_count: number of Markdown links [text](url)
        - image_count: number of Markdown images ![alt](url)
    """
    word_count = len(markdown_text.split())
    char_count = len(markdown_text)
    line_count = len(markdown_text.splitlines())
    heading_count = len(re.findall(r"^#{1,6}\s", markdown_text, re.MULTILINE))
    # Count fenced code blocks — each opening ``` (with optional lang) starts one
    code_block_count = len(re.findall(r"^```", markdown_text, re.MULTILINE)) // 2
    # Images must come before links to avoid double-counting
    image_count = len(re.findall(r"!\[.*?\]\(.*?\)", markdown_text))
    # Links: [text](url) but NOT images (which start with !)
    link_count = len(re.findall(r"(?<!!)\[.*?\]\(.*?\)", markdown_text))

    return {
        "word_count": word_count,
        "char_count": char_count,
        "line_count": line_count,
        "heading_count": heading_count,
        "code_block_count": code_block_count,
        "link_count": link_count,
        "image_count": image_count,
    }
