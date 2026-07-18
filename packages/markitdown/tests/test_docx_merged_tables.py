import io
from types import SimpleNamespace

import pytest

import markitdown.converters._docx_converter as docx_converter_module
from markitdown import StreamInfo
from markitdown.converters import DocxConverter, HtmlConverter


@pytest.fixture
def mock_docx_html(monkeypatch: pytest.MonkeyPatch):
    def _convert(html: str):
        monkeypatch.setattr(
            docx_converter_module,
            "pre_process_docx",
            lambda file_stream: file_stream,
        )
        monkeypatch.setattr(
            docx_converter_module.mammoth,
            "convert_to_html",
            lambda *args, **kwargs: SimpleNamespace(value=html),
        )
        return (
            DocxConverter()
            .convert(
                io.BytesIO(b"mock docx"),
                StreamInfo(extension=".docx"),
            )
            .markdown
        )

    return _convert


@pytest.mark.parametrize("attribute", ["rowspan", "colspan"])
def test_docx_preserves_tables_with_merged_cells_as_html(
    mock_docx_html,
    attribute: str,
) -> None:
    html = f"""
    <p>Before table</p>
    <table>
      <tr><th {attribute}="2">Merged heading</th><th>Second heading</th></tr>
      <tr><td>First value</td><td>Second value</td></tr>
    </table>
    <p>After table</p>
    """

    result = mock_docx_html(html)

    assert "Before table" in result
    assert "After table" in result
    assert "<table>" in result
    assert f'{attribute}="2"' in result
    assert "Merged heading" in result


def test_docx_keeps_simple_tables_as_markdown(mock_docx_html) -> None:
    html = """
    <table>
      <tr><th>First heading</th><th>Second heading</th></tr>
      <tr><td>First value</td><td>Second value</td></tr>
    </table>
    """

    result = mock_docx_html(html)

    assert "<table>" not in result
    assert "| First heading | Second heading |" in result
    assert "| First value | Second value |" in result


def test_html_converter_does_not_preserve_complex_tables_by_default() -> None:
    html = """
    <table>
      <tr><th rowspan="2">Merged heading</th><th>Second heading</th></tr>
      <tr><td>First value</td></tr>
    </table>
    """

    result = HtmlConverter().convert_string(html).markdown

    assert "<table>" not in result
    assert "Merged heading" in result
