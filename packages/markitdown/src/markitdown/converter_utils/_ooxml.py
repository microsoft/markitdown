"""Shared checks for Office Open XML (.docx, .xlsx, .pptx) packages."""

from typing import BinaryIO

# Office saves password-protected and rights-managed (IRM) documents as an OLE
# compound file whose "EncryptedPackage" stream holds the encrypted ZIP package
# ([MS-OFFCRYPTO]), so ZIP readers reject them with "File is not a zip file".
_OLE_SIGNATURE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
# Compound files store their stream names in UTF-16LE.
_ENCRYPTED_PACKAGE = "EncryptedPackage".encode("utf-16-le")


def _raise_if_encrypted(file_stream: BinaryIO, extension: str) -> None:
    position = file_stream.tell()
    try:
        encrypted = (
            file_stream.read(len(_OLE_SIGNATURE)) == _OLE_SIGNATURE
            and _ENCRYPTED_PACKAGE in file_stream.read()
        )
    finally:
        file_stream.seek(position)

    if encrypted:
        raise ValueError(
            f"This {extension} file is encrypted (password-protected or "
            "rights-managed), and MarkItDown cannot read encrypted documents. "
            "Convert an unprotected copy instead."
        )
