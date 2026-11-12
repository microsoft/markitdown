"""Password forwarding through each local PDF extraction path."""

import io
import sys
import warnings
from unittest.mock import MagicMock

import pytest

from markitdown import StreamInfo
from markitdown.converters import _pdf_converter


@pytest.mark.parametrize("mode", ["plain", "form", "fallback", "empty"])
def test_pdf_password_forwarded(monkeypatch, mode):
    open_pdf = MagicMock()
    page = MagicMock()
    page.extract_text.return_value = "plain text"
    open_pdf.return_value.__enter__.return_value.pages = [page]
    if mode == "fallback":
        open_pdf.side_effect = ValueError("extraction failed")
    monkeypatch.setattr(_pdf_converter.pdfplumber, "open", open_pdf)
    monkeypatch.setattr(
        _pdf_converter,
        "_extract_form_content_from_words",
        lambda page: "" if mode == "empty" else "form text" if mode == "form" else None,
    )
    extract = MagicMock(return_value="fallback text")
    monkeypatch.setattr(_pdf_converter.pdfminer.high_level, "extract_text", extract)

    result = _pdf_converter.PdfConverter().convert(
        io.BytesIO(b"pdf"), StreamInfo(extension=".pdf"), pdf_password="test-password"
    )

    assert open_pdf.call_args.kwargs["password"] == "test-password"
    if mode == "form":
        extract.assert_not_called()
        assert result.markdown == "form text"
    else:
        assert extract.call_args.kwargs["password"] == "test-password"
        assert result.markdown == "fallback text"


def test_pdf_password_error_is_actionable(monkeypatch):
    error = _pdf_converter.pdfminer.pdfdocument.PDFPasswordIncorrect
    monkeypatch.setattr(_pdf_converter.pdfplumber, "open", MagicMock(side_effect=error))
    monkeypatch.setattr(
        _pdf_converter.pdfminer.high_level,
        "extract_text",
        MagicMock(side_effect=error),
    )
    with pytest.raises(error, match="--pdf-password") as exc:
        _pdf_converter.PdfConverter().convert(
            io.BytesIO(b"pdf"),
            StreamInfo(extension=".pdf"),
            pdf_password="do-not-disclose",
        )
    assert "do-not-disclose" not in str(exc.value)


@pytest.mark.parametrize("stdin", [False, True])
def test_cli_pdf_password_prompt(monkeypatch, capsys, stdin):
    import markitdown.__main__ as cli

    instance = MagicMock()
    instance.convert.return_value.markdown = "converted"
    instance.convert_stream.return_value.markdown = "converted"
    prompt = MagicMock(return_value="test-password")
    monkeypatch.setattr(cli, "MarkItDown", MagicMock(return_value=instance))
    monkeypatch.setattr(cli.getpass, "getpass", prompt)
    monkeypatch.setattr(
        sys, "argv", ["markitdown", "--pdf-password"] + ([] if stdin else ["test.pdf"])
    )
    if stdin:
        monkeypatch.setattr(sys, "stdin", MagicMock(buffer=io.BytesIO(b"pdf")))
    cli.main()
    call = instance.convert_stream if stdin else instance.convert
    assert call.call_args.kwargs["pdf_password"] == "test-password"
    prompt.assert_called_once_with("PDF password: ")
    assert capsys.readouterr().out == "converted\n"


def test_cli_refuses_visible_password_input(monkeypatch):
    import markitdown.__main__ as cli

    def insecure_prompt(prompt):
        warnings.warn("Cannot hide input", cli.getpass.GetPassWarning)
        pytest.fail("Must not fall back to visible input")

    monkeypatch.setattr(sys, "argv", ["markitdown", "--pdf-password", "test.pdf"])
    monkeypatch.setattr(cli.getpass, "getpass", insecure_prompt)
    monkeypatch.setattr(cli, "MarkItDown", MagicMock())
    with pytest.raises(SystemExit) as exc:
        cli.main()
    assert exc.value.code == 2
