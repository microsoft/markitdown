"""Rebuild password-encrypted copies of small Office fixtures with msoffcrypto-tool.

Run from packages/markitdown with: python tests/test_files/generate_encrypted_office_fixtures.py
The source fixtures are opened read-only; only encrypted.{docx,xlsx,pptx} is written.
The password is "markitdown".
"""

from pathlib import Path

from msoffcrypto.format.ooxml import OOXMLFile

FIXTURES = Path(__file__).resolve().parent

SOURCES = {
    "encrypted.docx": "test_with_comment.docx",
    "encrypted.xlsx": "test.xlsx",
    "encrypted.pptx": "test_svg_no_fallback.pptx",
}


def main() -> None:
    for target, source in SOURCES.items():
        with open(FIXTURES / source, "rb") as plain, open(
            FIXTURES / target, "wb"
        ) as encrypted:
            OOXMLFile(plain).encrypt("markitdown", encrypted)


if __name__ == "__main__":
    main()
