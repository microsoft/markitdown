"""Password forwarding through each local PDF extraction path."""

import io
import sys
import warnings
from unittest.mock import MagicMock

import pytest

from markitdown import StreamInfo
from markitdown.converters import _pdf_converter


@pytest.mark.parametrize("mode", ["plain", "form", "fallback", "empty"])
@pytest.mark.parametrize(
    "password", ["test-password", " spaced password ", "caf\u00e9"]
)
def test_pdf_password_forwarded(monkeypatch, mode, password):
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
        io.BytesIO(b"pdf"), StreamInfo(extension=".pdf"), pdf_password=password
    )

    assert open_pdf.call_args.kwargs["password"] == password
    if mode == "form":
        extract.assert_not_called()
        assert result.markdown == "form text"
    else:
        assert extract.call_args.kwargs["password"] == password
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


@pytest.mark.parametrize(
    "password",
    [
        "do-not-disclose\r",
        "do-not-disclose\t",
        "\x1b[200~do-not-disclose\x1b[201~",
        "do-not-disclose\ue000",
        "do-not-disclose\u0627",
    ],
)
def test_pdf_saslprep_error_is_actionable(monkeypatch, password):
    # Exercise pdfminer's actual revision-6 normalization, not a mocked error.
    handler = _pdf_converter.pdfminer.pdfdocument.PDFStandardSecurityHandlerV5.__new__(
        _pdf_converter.pdfminer.pdfdocument.PDFStandardSecurityHandlerV5
    )
    handler.r = 6

    def reject_password(stream, *, password):
        handler._normalize_password(password)
        pytest.fail("Expected SASLprep to reject the synthetic password")

    open_pdf = MagicMock(side_effect=reject_password)
    extract = MagicMock(side_effect=reject_password)
    monkeypatch.setattr(_pdf_converter.pdfplumber, "open", open_pdf)
    monkeypatch.setattr(_pdf_converter.pdfminer.high_level, "extract_text", extract)

    with pytest.raises(
        _pdf_converter.PDFValueError, match="type the password manually"
    ) as exc:
        _pdf_converter.PdfConverter().convert(
            io.BytesIO(b"pdf"), StreamInfo(extension=".pdf"), pdf_password=password
        )

    assert "do-not-disclose" not in str(exc.value)
    assert "SASLprep:" in str(exc.value.__cause__)
    assert open_pdf.call_args.kwargs["password"] == password
    assert extract.call_args.kwargs["password"] == password


def test_pdf_unrelated_value_error_is_preserved(monkeypatch):
    error = _pdf_converter.PDFValueError("Invalid PDF structure")
    monkeypatch.setattr(_pdf_converter.pdfplumber, "open", MagicMock(side_effect=error))
    monkeypatch.setattr(
        _pdf_converter.pdfminer.high_level, "extract_text", MagicMock(side_effect=error)
    )

    with pytest.raises(type(error)) as exc:
        _pdf_converter.PdfConverter().convert(
            io.BytesIO(b"pdf"), StreamInfo(extension=".pdf")
        )
    assert exc.value is error


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
