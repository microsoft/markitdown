#!/usr/bin/env python3 -m pytest
import locale
import subprocess
import zipfile
from pathlib import Path

import pytest

from markitdown import MarkItDown


def _write_docx_with_complex_tables(path: Path) -> None:
    document_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p>
      <w:r><w:t>Quarterly research note</w:t></w:r>
    </w:p>
    <w:p>
      <w:r>
        <w:rPr><w:b/></w:rPr>
        <w:t>Audited</w:t>
      </w:r>
    </w:p>
    <w:tbl>
      <w:tr>
        <w:tc>
          <w:tcPr><w:gridSpan w:val="2"/></w:tcPr>
          <w:p><w:r><w:t>Segment Revenue</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:p><w:r><w:t>Q1</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:t>1200</w:t></w:r></w:p></w:tc>
      </w:tr>
    </w:tbl>
    <w:tbl>
      <w:tr>
        <w:tc>
          <w:p><w:r><w:t>Outer Cell</w:t></w:r></w:p>
          <w:tbl>
            <w:tr>
              <w:tc><w:p><w:r><w:t>Nested KPI</w:t></w:r></w:p></w:tc>
            </w:tr>
          </w:tbl>
        </w:tc>
      </w:tr>
    </w:tbl>
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>
"""
    with zipfile.ZipFile(path, "w") as docx:
        docx.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>
""",
        )
        docx.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
""",
        )
        docx.writestr("word/document.xml", document_xml)


@pytest.fixture()
def complex_tables_docx(tmp_path: Path) -> Path:
    docx_path = tmp_path / "complex-tables.docx"
    _write_docx_with_complex_tables(docx_path)
    return docx_path


def test_docx_tables_default_to_markdown(complex_tables_docx: Path) -> None:
    result = MarkItDown().convert(complex_tables_docx)

    assert "Segment Revenue" in result.markdown
    assert "Nested KPI" in result.markdown
    assert "<table" not in result.markdown


def test_docx_html_table_format_preserves_complex_table_structure(
    complex_tables_docx: Path,
) -> None:
    result = MarkItDown(docx_table_format="html").convert(complex_tables_docx)

    assert "<table" in result.markdown
    assert 'colspan="2"' in result.markdown
    assert "Segment Revenue" in result.markdown
    assert "Nested KPI" in result.markdown


def test_docx_table_format_can_be_overridden_per_conversion(
    complex_tables_docx: Path,
) -> None:
    markitdown = MarkItDown(docx_table_format="markdown")

    result = markitdown.convert(complex_tables_docx, docx_table_format="html")

    assert "<table" in result.markdown
    assert 'colspan="2"' in result.markdown


def test_docx_table_format_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match="docx_table_format"):
        MarkItDown(docx_table_format="invalid")


def test_docx_markdownify_options_are_forwarded(complex_tables_docx: Path) -> None:
    result = MarkItDown(docx_markdownify_options={"strong_em_symbol": "_"}).convert(
        complex_tables_docx
    )

    assert "__Audited__" in result.markdown


def test_cli_docx_table_format_html(complex_tables_docx: Path) -> None:
    result = subprocess.run(
        [
            "python",
            "-m",
            "markitdown",
            "--docx-table-format",
            "html",
            str(complex_tables_docx),
        ],
        capture_output=True,
        text=False,
    )
    stdout = result.stdout.decode(locale.getpreferredencoding())

    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert "<table" in stdout
    assert 'colspan="2"' in stdout
