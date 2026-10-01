"""DOCX subclasses customize image HTML without replacing document conversion."""

import base64
import inspect
import io
from pathlib import Path
from typing import Any, BinaryIO, Callable, Optional
from unittest.mock import Mock
import zipfile

from bs4 import BeautifulSoup
import mammoth
from mammoth.docx.files import InvalidFileReferenceError
import pytest

from markitdown import (
    FileConversionException,
    MarkItDown,
    MissingDependencyException,
    StreamInfo,
)
from markitdown.converters import DocxConverter, HtmlConverter
from markitdown.converters import _docx_converter


_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAM"
    "BAQDJ/pLvAAAAAElFTkSuQmCC"
)
_GIF = base64.b64decode("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBTAA7")
_INFO = StreamInfo(extension=".docx")
_FILES = Path(__file__).parent / "test_files"


def _image(rid: str = "rIdPng", number: int = 1) -> str:
    return f"""<w:r><w:drawing><wp:inline>
  <wp:extent cx="9525" cy="9525"/>
  <wp:docPr id="{number}" name="Image {number}" descr="Image {number}"/>
  <a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
    <pic:pic>
      <pic:nvPicPr><pic:cNvPr id="{number}" name="Image {number}"/><pic:cNvPicPr/></pic:nvPicPr>
      <pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
      <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="9525" cy="9525"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
      </pic:spPr>
    </pic:pic>
  </a:graphicData></a:graphic>
</wp:inline></w:drawing></w:r>"""


def _text(text: str) -> str:
    return f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r>'


def _paragraph(content: str) -> str:
    return f"<w:p>{content}</w:p>"


_BODY = _paragraph(_text("Before") + _image() + _text("After"))


def _docx(body: str = _BODY, *, embedded_style_map: Optional[str] = None) -> io.BytesIO:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Default Extension="gif" ContentType="image/gif"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdDocument" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "word/_rels/document.xml.rels",
            """<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdPng" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image.png"/>
  <Relationship Id="rIdGif" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image.gif"/>
</Relationships>""",
        )
        archive.writestr(
            "word/document.xml",
            f"""<w:document
  xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
  xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>{body}</w:body>
</w:document>""",
        )
        archive.writestr("word/media/image.png", _PNG)
        archive.writestr("word/media/image.gif", _GIF)
    if embedded_style_map is not None:
        stream.seek(0)
        mammoth.embed_style_map(stream, embedded_style_map)
    stream.seek(0)
    return stream


class _ImageConverter(DocxConverter):
    def __init__(self, render: Callable[..., Optional[str]]):
        super().__init__()
        self.render = render

    def _image_to_html(
        self, image_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any
    ) -> Optional[str]:
        return self.render(image_stream, stream_info, **kwargs)


def test_image_hook_does_not_change_public_conversion_signature() -> None:
    assert list(inspect.signature(DocxConverter.convert).parameters) == [
        "self",
        "file_stream",
        "stream_info",
        "kwargs",
    ]
    assert _ImageConverter.convert is DocxConverter.convert
    assert list(inspect.signature(DocxConverter.__init__).parameters) == ["self"]


@pytest.mark.parametrize("via_dispatcher", [False, True])
def test_inherited_hook_receives_images_and_options_in_order(
    via_dispatcher: bool,
) -> None:
    seen = []
    streams = []
    service = object()
    options: dict[str, Any] = {
        "ocr_service": service,
        "heading_style": "underlined",
    }

    def render(stream: BinaryIO, info: StreamInfo, **kwargs: Any) -> str:
        assert stream.tell() == 0
        data = stream.read()
        stream.seek(0)
        assert stream.read() == data
        seen.append((data, info, kwargs))
        streams.append(stream)
        return f"<strong>image{len(seen)}</strong>"

    class InheritedImages(_ImageConverter):
        pass

    converter = InheritedImages(render)
    source = _docx(
        _paragraph(
            _image("rIdGif", 1)
            + _text(" ")
            + _image("rIdPng", 2)
            + _text(" ")
            + _image("rIdGif", 3)
        )
    )
    original = source.getvalue()
    info = StreamInfo(
        extension=".docx",
        filename="document.docx",
        url="https://example.test/document.docx",
        local_path="/document.docx",
    )
    if via_dispatcher:
        markitdown = MarkItDown()
        markitdown.register_converter(converter, priority=-1)
        result = markitdown.convert_stream(source, stream_info=info, **options)
    else:
        source.seek(7)
        result = converter.convert(source, info, **options)

    assert [entry[:2] for entry in seen] == [
        (_GIF, StreamInfo(mimetype="image/gif", extension=".gif")),
        (_PNG, StreamInfo(mimetype="image/png", extension=".png")),
        (_GIF, StreamInfo(mimetype="image/gif", extension=".gif")),
    ]
    assert all(entry[2]["ocr_service"] is service for entry in seen)
    assert all(entry[2]["heading_style"] == "underlined" for entry in seen)
    assert result.markdown == "**image1** **image2** **image3**"
    assert all(stream.closed for stream in streams)
    assert not source.closed and source.getvalue() == original


@pytest.mark.parametrize("keep_data_uris", [False, True])
@pytest.mark.parametrize("fallback", [None, "", " \n\t"])
def test_declining_hook_preserves_native_output(
    monkeypatch: pytest.MonkeyPatch, fallback: Optional[str], keep_data_uris: bool
) -> None:
    expected_converter = DocxConverter()
    expected_html = Mock(wraps=expected_converter._html_converter.convert_string)
    monkeypatch.setattr(
        expected_converter._html_converter, "convert_string", expected_html
    )
    expected = expected_converter.convert(_docx(), _INFO, keep_data_uris=keep_data_uris)
    converter = _ImageConverter(Mock(return_value=fallback))
    actual_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", actual_html)

    actual = converter.convert(_docx(), _INFO, keep_data_uris=keep_data_uris)

    assert actual_html.call_args == expected_html.call_args
    assert actual.markdown == expected.markdown
    assert actual.title == expected.title


def test_native_converter_does_not_add_image_processing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    convert_html = Mock(wraps=mammoth.convert_to_html)
    monkeypatch.setattr(mammoth, "convert_to_html", convert_html)

    class UnmodifiedSubclass(DocxConverter):
        pass

    for converter in (DocxConverter(), UnmodifiedSubclass()):
        result = converter.convert(_docx(), _INFO)
        assert "![Image 1](data:image/png;base64...)" in result.markdown
        assert "convert_image" not in convert_html.call_args.kwargs


def test_override_can_delegate_to_super() -> None:
    class NativeImages(DocxConverter):
        def _image_to_html(self, image_stream, stream_info, **kwargs):
            return super()._image_to_html(image_stream, stream_info, **kwargs)

    actual = NativeImages().convert(_docx(), _INFO)
    assert actual.markdown == DocxConverter().convert(_docx(), _INFO).markdown


@pytest.mark.parametrize(
    ("fragment", "expected"),
    [
        ("<strong>text</strong>", "<p>Before<strong>text</strong>After</p>"),
        ("one<br>two", "<p>Beforeone<br/>twoAfter</p>"),
        ("A &amp; B &lt; C", "<p>BeforeA &amp; B &lt; CAfter</p>"),
        (
            "<p>one</p><p>two</p>",
            "<p>Before</p><p>one</p><p>two</p><p>After</p>",
        ),
        (
            "<div><p>one</p><p>two</p></div>",
            "<p>Before</p><div><p>one</p><p>two</p></div><p>After</p>",
        ),
        (
            "<ul><li>one</li><li>two</li></ul>",
            "<p>Before</p><ul><li>one</li><li>two</li></ul><p>After</p>",
        ),
        (
            "<table><tr><th>Key</th></tr><tr><td>Value</td></tr></table>",
            "<p>Before</p><table><tr><th>Key</th></tr><tr><td>Value</td></tr>"
            "</table><p>After</p>",
        ),
        (
            "<details><summary>Title</summary><p>Body</p></details>",
            "<p>Before</p><details><summary>Title</summary><p>Body</p>"
            "</details><p>After</p>",
        ),
        (
            "lead<p>block</p>tail",
            "<p>Beforelead</p><p>block</p><p>tailAfter</p>",
        ),
        (
            "<pre><code>a &lt; b\n  *literal*</code></pre>",
            "<p>Before</p><pre><code>a &lt; b\n  *literal*</code></pre><p>After</p>",
        ),
    ],
)
def test_fragment_placement_precedes_shared_html_conversion(
    monkeypatch: pytest.MonkeyPatch, fragment: str, expected: str
) -> None:
    converter = _ImageConverter(Mock(return_value=fragment))
    convert_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", convert_html)
    options = {"escape_asterisks": False, "custom_option": "forwarded"}

    result = converter.convert(_docx(), _INFO, **options)

    assert convert_html.call_args.args == (expected,)
    assert convert_html.call_args.kwargs == options
    assert (
        result.markdown
        == HtmlConverter().convert_string(expected, escape_asterisks=False).markdown
    )
    assert "data-markitdown-image" not in expected


@pytest.mark.parametrize(
    ("style_map", "expected"),
    [
        (None, "<p>one</p><p>two</p>"),
        ("p => ul > li:fresh", "<ul><li><p>one</p><p>two</p></li></ul>"),
        ("p => blockquote > p:fresh", "<blockquote><p>one</p><p>two</p></blockquote>"),
        ("p => h2:fresh > strong", "<p>one</p><p>two</p>"),
    ],
)
def test_standalone_block_image_does_not_leave_empty_wrappers(
    monkeypatch: pytest.MonkeyPatch, style_map: Optional[str], expected: str
) -> None:
    converter = _ImageConverter(Mock(return_value="<p>one</p><p>two</p>"))
    convert_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", convert_html)

    converter.convert(_docx(_paragraph(_image())), _INFO, style_map=style_map)

    assert convert_html.call_args.args == (expected,)


def test_block_image_keeps_its_table_cell(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = (
        "<w:tbl><w:tblPr/><w:tblGrid><w:gridCol/><w:gridCol/></w:tblGrid>"
        "<w:tr><w:tc>"
        + _paragraph(_text("Item"))
        + "</w:tc><w:tc>"
        + _paragraph(_text("Details"))
        + "</w:tc></w:tr><w:tr><w:tc>"
        + _paragraph(_text("A"))
        + "</w:tc><w:tc>"
        + _paragraph(_image())
        + "</w:tc></w:tr></w:tbl>"
    )
    converter = _ImageConverter(
        Mock(return_value="<p>Serial: 12345</p><p>Status: active</p>")
    )
    convert_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", convert_html)

    result = converter.convert(_docx(body), _INFO)

    soup = BeautifulSoup(convert_html.call_args.args[0], "html.parser")
    assert len(soup.find_all("tr")) == 2
    assert len(soup.find_all("td")) == 4
    assert (
        str(soup.find_all("td")[-1])
        == "<td><p>Serial: 12345</p><p>Status: active</p></td>"
    )
    assert not soup.select("p p")
    assert "| A | Serial: 12345  Status: active |" in result.markdown


def test_nested_run_formatting_is_preserved_around_blocks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    converter = _ImageConverter(Mock(return_value="<p>block</p>"))
    convert_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", convert_html)

    converter.convert(_docx(), _INFO, style_map="p => p:fresh > em > strong")

    assert convert_html.call_args.args == (
        "<p><em><strong>Before</strong></em></p><p>block</p>"
        "<p><em><strong>After</strong></em></p>",
    )


def test_hook_inherits_preprocessing_and_style_precedence() -> None:
    body = (
        _BODY
        + _paragraph(
            '<w:r><w:rPr><w:u w:val="single"/></w:rPr><w:t>underlined</w:t></w:r>'
        )
        + _paragraph("<w:r><w:rPr><w:dstrike/></w:rPr><w:t>deleted</w:t></w:r>")
        + _paragraph("<m:oMath><m:r><m:t>x</m:t></m:r></m:oMath>")
    )

    result = _ImageConverter(Mock(return_value="image")).convert(
        _docx(body, embedded_style_map="u => em"),
        _INFO,
        style_map="u => strong",
    )

    assert result.markdown == "BeforeimageAfter\n\n**underlined**\n\n~~deleted~~\n\n$x$"


def test_multiple_images_and_native_fallback_keep_their_own_positions() -> None:
    converter = _ImageConverter(Mock(side_effect=[None, "<em>recognized</em>", ""]))
    body = _paragraph(
        _image(number=1) + _text(" ") + _image(number=2) + _text(" ") + _image(number=3)
    )

    result = converter.convert(_docx(body), _INFO)

    assert result.markdown == (
        "![Image 1](data:image/png;base64...) *recognized* "
        "![Image 3](data:image/png;base64...)"
    )


def test_many_images_have_independent_replacements() -> None:
    converter = _ImageConverter(
        Mock(side_effect=[f"<p>Image {number}</p>" for number in range(12)])
    )
    body = _paragraph("".join(_image(number=number) for number in range(12)))

    result = converter.convert(_docx(body), _INFO)

    assert result.markdown == "\n\n".join(f"Image {number}" for number in range(12))


def test_returned_image_and_literal_text_use_normal_html_rendering() -> None:
    render = Mock(
        return_value=(
            "<p>&lt;literal&gt; *not emphasis* &amp; text</p>"
            '<img alt="generated" src="image.png"><script>discard</script>'
        )
    )
    result = _ImageConverter(render).convert(_docx(_paragraph(_image())), _INFO)

    assert (
        result.markdown
        == r"<literal> \*not emphasis\* & text" + "\n\n![generated](image.png)"
    )
    render.assert_called_once()


@pytest.mark.parametrize("result", [False, 123, b"<p>not a string</p>"])
def test_invalid_return_is_not_silent_native_fallback(result: Any) -> None:
    with pytest.raises(TypeError, match="HTML string or None"):
        _ImageConverter(Mock(return_value=result)).convert(_docx(), _INFO)


@pytest.mark.parametrize(
    "fragment",
    [
        "<html><body>document</body></html>",
        "<head><title>title</title></head>",
        "<body>content</body>",
        "<!DOCTYPE html><p>content</p>",
    ],
)
def test_full_document_is_not_a_valid_fragment(fragment: str) -> None:
    with pytest.raises(ValueError, match="fragment, not a document"):
        _ImageConverter(Mock(return_value=fragment)).convert(_docx(), _INFO)


@pytest.mark.parametrize("via_dispatcher", [False, True])
def test_hook_errors_propagate_and_close_the_image_stream(via_dispatcher: bool) -> None:
    streams = []
    error = RuntimeError("Image service failed")

    def render(stream, info, **kwargs):
        streams.append(stream)
        raise error

    converter = _ImageConverter(render)
    if via_dispatcher:
        markitdown = MarkItDown(enable_builtins=False)
        markitdown.register_converter(converter, priority=-1)
        with pytest.raises(FileConversionException) as caught:
            markitdown.convert_stream(_docx(), stream_info=_INFO)
        assert caught.value.attempts is not None
        assert any(
            attempt.exc_info and attempt.exc_info[1] is error
            for attempt in caught.value.attempts
        )
    else:
        with pytest.raises(RuntimeError) as caught_direct:
            converter.convert(_docx(), _INFO)
        assert caught_direct.value is error
    assert streams and all(stream.closed for stream in streams)


def test_dispatcher_can_fall_back_to_native_docx_after_hook_error() -> None:
    render = Mock(side_effect=RuntimeError("Image service failed"))
    markitdown = MarkItDown()
    markitdown.register_converter(_ImageConverter(render), priority=-1)

    result = markitdown.convert_stream(_docx(), stream_info=_INFO)

    assert result.markdown == DocxConverter().convert(_docx(), _INFO).markdown
    render.assert_called()


def test_mammoth_does_not_swallow_hook_file_reference_errors() -> None:
    error = InvalidFileReferenceError("hook failed")
    render = Mock(side_effect=error)

    with pytest.raises(RuntimeError, match="_image_to_html failed") as caught:
        _ImageConverter(render).convert(_docx(), _INFO)

    assert caught.value.__cause__ is error
    render.assert_called_once()


def test_per_call_options_and_fragments_do_not_leak_between_conversions() -> None:
    converter = _ImageConverter(lambda stream, info, **kwargs: kwargs.get("image_text"))
    first = converter.convert(_docx(), _INFO, image_text="<p>first</p>")
    second = converter.convert(_docx(), _INFO, image_text="<p>second</p>")
    third = converter.convert(_docx(), _INFO)

    assert first.markdown == "Before\n\nfirst\n\nAfter"
    assert second.markdown == "Before\n\nsecond\n\nAfter"
    assert third.markdown == DocxConverter().convert(_docx(), _INFO).markdown


def test_unreferenced_media_does_not_invoke_the_hook() -> None:
    render = Mock(side_effect=AssertionError("unexpected image"))

    result = _ImageConverter(render).convert(
        _docx(_paragraph(_text("Only text"))), _INFO
    )

    assert result.markdown == "Only text"
    render.assert_not_called()


@pytest.mark.parametrize(
    "fragment",
    [
        '<a href="https://example.test/new">new</a>',
        '<p><a href="https://example.test/new">new</a></p>',
    ],
)
def test_image_html_does_not_create_nested_links(
    monkeypatch: pytest.MonkeyPatch, fragment: str
) -> None:
    body = _paragraph(
        '<w:hyperlink w:anchor="target">'
        + _text("Before")
        + _image()
        + _text("After")
        + "</w:hyperlink>"
    )
    converter = _ImageConverter(Mock(return_value=fragment))
    convert_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", convert_html)

    result = converter.convert(_docx(body), _INFO)

    soup = BeautifulSoup(convert_html.call_args.args[0], "html.parser")
    assert not soup.select("a a")
    assert [link.get("href") for link in soup.find_all("a")] == [
        "#target",
        "https://example.test/new",
        "#target",
    ]
    assert "[Before](#target)" in result.markdown
    assert "[new](https://example.test/new)" in result.markdown
    assert "[After](#target)" in result.markdown


@pytest.mark.parametrize("keep_data_uris", [False, True])
def test_declining_hook_preserves_a_real_document(keep_data_uris: bool) -> None:
    content = (_FILES / "test.docx").read_bytes()
    expected = DocxConverter().convert(
        io.BytesIO(content), _INFO, keep_data_uris=keep_data_uris
    )
    render = Mock(return_value=None)

    actual = _ImageConverter(render).convert(
        io.BytesIO(content), _INFO, keep_data_uris=keep_data_uris
    )

    assert actual.markdown == expected.markdown
    assert actual.title == expected.title
    render.assert_called()


def test_hook_reads_images_from_the_preprocessed_archive() -> None:
    import struct

    stream = _docx()
    data = bytearray(stream.getvalue())
    with zipfile.ZipFile(stream) as archive:
        offset = archive.getinfo("word/media/image.png").header_offset
    length = struct.unpack_from("<H", data, offset + 26)[0]
    data[offset + 30 : offset + 30 + length] = b"WORD/MEDIA/IMAGE.PNG"
    with pytest.raises(zipfile.BadZipFile), zipfile.ZipFile(
        io.BytesIO(data)
    ) as archive:
        archive.read("word/media/image.png")
    observed = []

    def render(image_stream, stream_info, **kwargs):
        observed.append(image_stream.read())
        return "<span>image</span>"

    result = _ImageConverter(render).convert(io.BytesIO(data), _INFO)

    assert observed == [_PNG]
    assert result.markdown == "BeforeimageAfter"


def test_missing_dependencies_fail_before_invoking_hook(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    error = ModuleNotFoundError("No module named 'mammoth'")
    monkeypatch.setattr(
        _docx_converter, "_dependency_exc_info", (ModuleNotFoundError, error, None)
    )
    render = Mock()

    with pytest.raises(MissingDependencyException) as caught:
        _ImageConverter(render).convert(_docx(), _INFO)

    assert caught.value.__cause__ is error
    render.assert_not_called()
