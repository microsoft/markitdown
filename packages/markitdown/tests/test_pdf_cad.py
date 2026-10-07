"""CAD rejection policy, exercised with real, synthetic vector PDFs."""

import io
import subprocess
import sys

import pytest
from pdfplumber.utils.exceptions import PdfminerException

from markitdown import MarkItDown, StreamInfo, DocumentConverter
from markitdown._exceptions import (
    UnsupportedFormatException,
    MissingDependencyException,
)
from markitdown.converters import _pdf_converter


def drawing_pdf(creator="AutoCAD 2026", producer="PDF plotter", labels=True):
    # A minimal PDF with a vector floor plan and optional embedded text. Build
    # real cross-reference offsets so detection does not depend on parser repair.
    content = b"50 50 400 300 re S 250 50 m 250 350 l S"
    if labels:
        content += b" BT /F1 12 Tf 80 200 Td (ROOM A) Tj 220 0 Td (ROOM B) Tj ET"
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 500 400] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length "
        + str(len(content)).encode()
        + b" >>\nstream\n"
        + content
        + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        f"<< /Creator ({creator}) /Producer ({producer}) >>".encode(),
    ]
    data = b"%PDF-1.4\n"
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data += f"{number} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref = len(data)
    data += b"xref\n0 7\n0000000000 65535 f \n"
    data += b"".join(f"{offset:010} 00000 n \n".encode() for offset in offsets[1:])
    data += f"trailer\n<< /Size 7 /Root 1 0 R /Info 6 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return data


@pytest.mark.parametrize("labels", [True, False])
@pytest.mark.parametrize("plugins", [True, False])
def test_cad_rejected_before_conversion(labels, plugins):
    with pytest.raises(UnsupportedFormatException, match="CAD-generated PDF"):
        MarkItDown(enable_plugins=plugins).convert_stream(
            io.BytesIO(drawing_pdf(labels=labels)), reject_cad_pdfs=True
        )


@pytest.mark.parametrize("field", ["creator", "producer"])
@pytest.mark.parametrize(
    "exporter",
    ["AutoCAD 2026", "Autodesk Revit", "SOLIDWORKS 2025", "Bentley MicroStation"],
)
def test_known_exporter_metadata(field, exporter):
    metadata = {"creator": "", "producer": "", field: exporter}
    with pytest.raises(UnsupportedFormatException, match="CAD-generated PDF"):
        MarkItDown().convert_stream(
            io.BytesIO(drawing_pdf(**metadata)), reject_cad_pdfs=True
        )


@pytest.mark.parametrize(
    "creator", ["", "Microsoft Word", "AutoCADish", "Revision tool"]
)
def test_unknown_metadata_is_not_classified_as_cad(creator):
    result = MarkItDown().convert_stream(
        io.BytesIO(drawing_pdf(creator=creator)), reject_cad_pdfs=True
    )
    assert "ROOM A" in result.markdown


def test_existing_partial_extraction_remains_available():
    result = MarkItDown().convert_stream(io.BytesIO(drawing_pdf()))
    assert "ROOM A" in result.markdown
    assert "ROOM B" in result.markdown


def test_strict_option_does_not_change_non_pdf_conversion():
    result = MarkItDown().convert_stream(
        io.BytesIO(b"# AutoCAD documentation"),
        stream_info=StreamInfo(extension=".md"),
        reject_cad_pdfs=True,
    )
    assert result.markdown == "# AutoCAD documentation"


def test_rejection_precedes_registered_converters():
    class UnexpectedConverter(DocumentConverter):
        def accepts(self, *args, **kwargs):
            pytest.fail("Policy must run before a plugin or cloud converter")

    md = MarkItDown()
    md.register_converter(UnexpectedConverter(), priority=-100)
    with pytest.raises(UnsupportedFormatException, match="CAD-generated PDF"):
        md.convert_stream(io.BytesIO(drawing_pdf()), reject_cad_pdfs=True)


@pytest.mark.parametrize("creator", ["AutoCAD", "Microsoft Word"])
def test_inspection_restores_stream_position(creator):
    stream = io.BytesIO(drawing_pdf(creator=creator))
    stream.seek(5)
    try:
        _pdf_converter.PdfConverter.reject_cad_pdf(stream)
    except UnsupportedFormatException:
        assert creator == "AutoCAD"
    assert stream.tell() == 5


def test_missing_pdf_dependencies_do_not_bypass_policy(monkeypatch):
    error = ImportError("missing PDF library")
    monkeypatch.setattr(
        _pdf_converter, "_dependency_exc_info", (ImportError, error, None)
    )
    with pytest.raises(MissingDependencyException, match="CAD PDF detection requires"):
        MarkItDown().convert_stream(io.BytesIO(drawing_pdf()), reject_cad_pdfs=True)


def test_malformed_pdf_does_not_fall_back_to_partial_conversion():
    with pytest.raises(PdfminerException, match="No /Root object"):
        MarkItDown().convert_stream(
            io.BytesIO(b"%PDF-1.4\ninvalid"),
            stream_info=StreamInfo(extension=".pdf"),
            reject_cad_pdfs=True,
        )


@pytest.mark.parametrize("stdin", [True, False])
def test_cli_rejects_without_writing_output(tmp_path, stdin):
    source = tmp_path / "drawing.pdf"
    source.write_bytes(drawing_pdf())
    output = tmp_path / "drawing.md"
    output.write_text("existing output", encoding="utf-8")
    command = [
        sys.executable,
        "-m",
        "markitdown",
        "--reject-cad-pdfs",
        "-o",
        str(output),
    ]
    if not stdin:
        command.append(str(source))
    result = subprocess.run(
        command, input=source.read_bytes() if stdin else None, capture_output=True
    )
    assert result.returncode != 0
    assert b"CAD-generated PDF" in result.stderr
    assert result.stdout == b""
    assert output.read_text(encoding="utf-8") == "existing output"
