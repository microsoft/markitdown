"""Word headings deeper than level 6 clamp to h6 rather than losing structure."""

import io
import zipfile

import pytest

from markitdown import MarkItDown, StreamInfo


WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
STYLES_RELATIONSHIP_TYPE = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
)
LEVELS = range(1, 10)


def _headings_docx(style_id_format: str, *, stylesheet: bool) -> io.BytesIO:
    """Build a minimal .docx holding one paragraph per Word heading level."""
    style_ids = {level: style_id_format.format(level=level) for level in LEVELS}
    body = "".join(
        f'<w:p><w:pPr><w:pStyle w:val="{style_id}"/></w:pPr>'
        f"<w:r><w:t>Level {level}</w:t></w:r></w:p>"
        for level, style_id in style_ids.items()
    )
    styles_relationship = (
        f'<Relationship Id="rId2" Type="{STYLES_RELATIONSHIP_TYPE}"'
        ' Target="styles.xml"/>'
        if stylesheet
        else ""
    )

    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "word/_rels/document.xml.rels",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {styles_relationship}
</Relationships>""",
        )
        archive.writestr(
            "word/document.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{WORD_NAMESPACE}">
  <w:body>{body}</w:body>
</w:document>""",
        )
        if stylesheet:
            styles = "".join(
                f'<w:style w:type="paragraph" w:styleId="{style_id}">'
                f'<w:name w:val="heading {level}"/></w:style>'
                for level, style_id in style_ids.items()
            )
            archive.writestr(
                "word/styles.xml",
                f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{WORD_NAMESPACE}">{styles}</w:styles>""",
            )

    stream.seek(0)
    return stream


@pytest.mark.parametrize(
    ("style_id_format", "stylesheet"),
    [
        # The style ids Word itself writes, matched without a stylesheet ...
        ("Heading{level}", False),
        # ... and the ids a localized Word writes, matched by their style name.
        ("Titre{level}", True),
    ],
)
def test_docx_headings_past_level_six_are_clamped(
    style_id_format: str, stylesheet: bool
) -> None:
    docx_stream = _headings_docx(style_id_format, stylesheet=stylesheet)

    result = MarkItDown().convert_stream(
        docx_stream, stream_info=StreamInfo(extension=".docx")
    )

    assert result.markdown.split("\n\n") == [
        f"{'#' * min(level, 6)} Level {level}" for level in LEVELS
    ]


def test_docx_caller_style_map_overrides_deep_heading_clamp() -> None:
    # A caller-supplied style map still outranks the Heading 7-9 clamp.
    docx_stream = _headings_docx("Heading{level}", stylesheet=False)

    result = MarkItDown(style_map="p.Heading7 => p:fresh").convert_stream(
        docx_stream, stream_info=StreamInfo(extension=".docx")
    )

    assert "\n\nLevel 7\n\n" in result.markdown
    assert "###### Level 7" not in result.markdown
