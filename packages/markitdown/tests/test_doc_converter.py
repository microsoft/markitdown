import io
import struct

from markitdown.converters._doc_converter import _WordDocTextExtractor


class _FakeOle:
    def __init__(self, streams):
        self._streams = streams

    def exists(self, name):
        return name in self._streams

    def openstream(self, name):
        return io.BytesIO(self._streams[name])


def _legacy_doc_stream(text):
    word = bytearray(0x300)
    struct.pack_into("<H", word, 0, 0xA5EC)
    struct.pack_into("<H", word, 0x0A, 0)
    struct.pack_into("<I", word, 0x01A2, 0)

    encoded = text.encode("cp1252")
    text_offset = 0x200
    word[text_offset : text_offset + len(encoded)] = encoded

    plc = bytearray()
    plc += struct.pack("<II", 0, len(text))
    plc += b"\x00\x00"
    plc += struct.pack("<I", (text_offset * 2) | 0x40000000)
    plc += b"\x00\x00"
    clx = b"\x02" + struct.pack("<I", len(plc)) + plc
    struct.pack_into("<I", word, 0x01A6, len(clx))
    return bytes(word), clx


def test_word_doc_text_extractor_reads_piece_table_text():
    word, table = _legacy_doc_stream("Hello from old Word\rSecond line")
    text = _WordDocTextExtractor(
        _FakeOle({"WordDocument": word, "0Table": table})
    ).extract()

    assert "Hello from old Word" in text
    assert "Second line" in text
