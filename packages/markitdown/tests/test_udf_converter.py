#!/usr/bin/env python3 -m pytest
import io
import zipfile

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import UdfConverter


def build_udf(content_xml: str) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("content.xml", content_xml)
    return buffer.getvalue()


def build_zip(filename: str, content: str) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(filename, content)
    return buffer.getvalue()


def wrap_template(cdata: str, elements: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" ?>\n'
        '<template format_id="1.8">\n'
        f"<content><![CDATA[{cdata}]]></content>\n"
        "<properties></properties>\n"
        f'<elements resolver="hvl-default">{elements}</elements>\n'
        "</template>"
    )


def test_accepts_udf_zip_without_extension() -> None:
    converter = UdfConverter()
    udf_bytes = build_udf(
        wrap_template(
            "Merhaba\n",
            '<paragraph Alignment="0"><content startOffset="0" length="7" /></paragraph>',
        )
    )

    accepts = converter.accepts(
        io.BytesIO(udf_bytes),
        StreamInfo(mimetype="application/zip"),
    )

    assert accepts is True

    result = MarkItDown().convert_stream(
        io.BytesIO(udf_bytes),
        stream_info=StreamInfo(mimetype="application/zip"),
    )
    assert result.markdown == "Merhaba"


def test_rejects_regular_zip_stream() -> None:
    converter = UdfConverter()
    zip_bytes = build_zip("notes.txt", "not a udf archive")

    accepts = converter.accepts(
        io.BytesIO(zip_bytes),
        StreamInfo(mimetype="application/zip"),
    )

    assert accepts is False


def test_rune_offsets_handle_turkish_and_emoji() -> None:
    udf_bytes = build_udf(
        wrap_template(
            "Türkçe 👋 deneme\n",
            (
                '<paragraph Alignment="0">'
                '<content startOffset="0" length="8" />'
                '<content startOffset="8" length="7" bold="true" />'
                "</paragraph>"
            ),
        )
    )

    result = MarkItDown().convert_stream(
        io.BytesIO(udf_bytes),
        stream_info=StreamInfo(extension=".udf"),
    )

    assert result.markdown == "Türkçe 👋 **deneme**"


def test_numbered_lists_reset_across_groups() -> None:
    udf_bytes = build_udf(
        wrap_template(
            "Bir\nIki\nAra\nUc\n",
            (
                '<paragraph Alignment="0" Numbered="true" ListLevel="0" ListId="1">'
                '<content startOffset="0" length="3" />'
                "</paragraph>"
                '<paragraph Alignment="0" Numbered="true" ListLevel="0" ListId="1">'
                '<content startOffset="4" length="3" />'
                "</paragraph>"
                '<paragraph Alignment="0"><content startOffset="8" length="3" /></paragraph>'
                '<paragraph Alignment="0" Numbered="true" ListLevel="0" ListId="1">'
                '<content startOffset="12" length="2" />'
                "</paragraph>"
            ),
        )
    )

    result = MarkItDown().convert_stream(
        io.BytesIO(udf_bytes),
        stream_info=StreamInfo(extension=".udf"),
    )

    assert result.markdown == "1. Bir\n2. Iki\n\nAra\n\n1. Uc"


def test_numbered_lists_reset_when_list_id_changes() -> None:
    udf_bytes = build_udf(
        wrap_template(
            "Bir\nIki\nUc\n",
            (
                '<paragraph Alignment="0" Numbered="true" ListLevel="0" ListId="1">'
                '<content startOffset="0" length="3" />'
                "</paragraph>"
                '<paragraph Alignment="0" Numbered="true" ListLevel="0" ListId="1">'
                '<content startOffset="4" length="3" />'
                "</paragraph>"
                '<paragraph Alignment="0" Numbered="true" ListLevel="0" ListId="2">'
                '<content startOffset="8" length="2" />'
                "</paragraph>"
            ),
        )
    )

    result = MarkItDown().convert_stream(
        io.BytesIO(udf_bytes),
        stream_info=StreamInfo(extension=".udf"),
    )

    assert result.markdown == "1. Bir\n2. Iki\n1. Uc"


def test_zero_width_space_is_removed_from_empty_paragraphs() -> None:
    udf_bytes = build_udf(
        wrap_template(
            "Ilk\n\u200b\nSon\n",
            (
                '<paragraph Alignment="0"><content startOffset="0" length="3" /></paragraph>'
                '<paragraph Alignment="0"></paragraph>'
                '<paragraph Alignment="0"><content startOffset="6" length="3" /></paragraph>'
            ),
        )
    )

    result = MarkItDown().convert_stream(
        io.BytesIO(udf_bytes),
        stream_info=StreamInfo(extension=".udf"),
    )

    assert "\u200b" not in result.markdown
    assert result.markdown == "Ilk\n\nSon"


def test_nested_table_content_is_flattened_inside_cells() -> None:
    udf_bytes = build_udf(
        wrap_template(
            "Baslik\nDetay\nSatir\nIc A\nIc B\nBitis\n",
            (
                '<table tableName="Sabit" columnCount="2" columnSpans="100,100">'
                '<row rowName="row1" rowType="dataRow">'
                '<cell><paragraph Alignment="0"><content startOffset="0" length="6" /></paragraph></cell>'
                '<cell><paragraph Alignment="0"><content startOffset="7" length="5" /></paragraph></cell>'
                "</row>"
                '<row rowName="row2" rowType="dataRow">'
                "<cell>"
                '<paragraph Alignment="0"><content startOffset="13" length="5" /></paragraph>'
                '<table tableName="Ic" columnCount="2" columnSpans="50,50">'
                '<row rowName="row1" rowType="dataRow">'
                '<cell><paragraph Alignment="0"><content startOffset="19" length="4" /></paragraph></cell>'
                '<cell><paragraph Alignment="0"><content startOffset="24" length="4" /></paragraph></cell>'
                "</row>"
                "</table>"
                "</cell>"
                '<cell><paragraph Alignment="0"><content startOffset="29" length="5" /></paragraph></cell>'
                "</row>"
                "</table>"
            ),
        )
    )

    result = MarkItDown().convert_stream(
        io.BytesIO(udf_bytes),
        stream_info=StreamInfo(extension=".udf"),
    )

    assert result.markdown == (
        "| Baslik | Detay |\n"
        "| --- | --- |\n"
        "| Satir Ic A / Ic B | Bitis |"
    )


def test_image_placeholder_is_separated_from_adjacent_text() -> None:
    udf_bytes = build_udf(
        wrap_template(
            "Once\nSonra\n",
            (
                '<paragraph Alignment="0">'
                '<content startOffset="0" length="4" />'
                '<image imageData="abc" width="10" height="10" />'
                '<content startOffset="5" length="5" bold="true" />'
                "</paragraph>"
            ),
        )
    )

    result = MarkItDown().convert_stream(
        io.BytesIO(udf_bytes),
        stream_info=StreamInfo(extension=".udf"),
    )

    assert result.markdown == "Once [embedded image omitted] **Sonra**"
