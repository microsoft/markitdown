"""Drawing-aware extraction and safe CLI output regressions."""
import base64
import io
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from markitdown import MarkItDown, StreamInfo, DocumentConverter
from PIL import Image


# Valid PDF fixture construction uses no extra test dependency.
def drawing_pdf(
    labels=True,
    rotated=False,
    annotation=False,
    crop=False,
    multipage=False,
    page_rotation=0,
):
    content = b"50 50 400 300 re S 250 50 m 250 350 l S"
    if labels:
        matrix = {
            90: b"0 1 -1 0 80 100 Tm",
            180: b"-1 0 0 -1 400 200 Tm",
            270: b"0 -1 1 0 200 300 Tm",
        }.get(90 if rotated is True else rotated, b"1 0 0 1 80 200 Tm")
        content += b" BT /F1 12 Tf " + matrix + b" (ROOM A | <script>) Tj ET"
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        (
            f"<< /Type /Pages /Kids [3 0 R {8 if annotation else 7} 0 R] /Count 2 >>".encode()
            if multipage
            else b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>"
        ),
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 500 400] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R "
        + (b"/Annots [7 0 R] " if annotation else b"")
        + (b"/CropBox [40 40 460 360] " if crop else b"")
        + f"/Rotate {page_rotation} >>".encode(),
        b"<< /Length "
        + str(len(content)).encode()
        + b" >>\nstream\n"
        + content
        + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Creator (AutoCAD 2026) >>",
    ]
    if annotation:
        objects.append(
            b"<< /Type /Annot /Subtype /Text /Rect [10 10 100 30] /T (AutoCAD SHX Text) /Contents (SHX LABEL) >>"
        )
    if multipage:
        objects.append(objects[2])
    data = b"%PDF-1.4\n"
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref = len(data)
    data += f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode()
    data += b"".join(f"{offset:010} 00000 n \n".encode() for offset in offsets[1:])
    return (
        data
        + f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R /Info 6 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    )


def test_drawing_mode_preserves_native_shx_and_visual_content():
    result = MarkItDown().convert_stream(
        io.BytesIO(drawing_pdf(annotation=True)), pdf_drawing_mode=True
    )
    assert "SHX LABEL" in result.markdown
    assert "&lt;script&gt;" in result.markdown
    assert "&#124;" in result.markdown
    assert "| Source |" in result.markdown
    assert "](page-1.png)" in result.markdown
    assert "not lossless" in result.markdown
    assert "not exhaustive" in result.conversion_report
    assert "semantic" in result.conversion_report.lower()
    image = Image.open(io.BytesIO(result.assets["page-1.png"]))
    # White background plus vector plan must appear, including when no images
    # were embedded in the PDF. This is a real raster, not a decorative URI.
    assert image.width > 1000
    assert image.convert("L").getextrema() == (0, 255)


def test_geometry_only_has_visual_and_no_searchable_label_report():
    result = MarkItDown().convert_stream(
        io.BytesIO(drawing_pdf(labels=False)), pdf_drawing_mode=True
    )
    assert result.assets
    assert "No searchable labels" in result.conversion_report


def test_rotated_labels_are_not_dropped():
    result = MarkItDown().convert_stream(
        io.BytesIO(drawing_pdf(rotated=True)), pdf_drawing_mode=True
    )
    assert "rotated" in result.markdown
    assert "ROOM" in result.markdown


def test_explicit_inline_pages_are_decodable():
    result = MarkItDown().convert_stream(
        io.BytesIO(drawing_pdf()), pdf_drawing_mode=True, keep_data_uris=True
    )
    assert not result.assets
    encoded = result.markdown.split("data:image/png;base64,", 1)[1].split(")", 1)[0]
    assert Image.open(io.BytesIO(base64.b64decode(encoded))).format == "PNG"


def test_render_failure_does_not_fall_back_to_text_conversion():
    with patch(
        "pdfplumber.page.Page.to_image", side_effect=RuntimeError("render failed")
    ):
        with pytest.raises(Exception, match="render failed"):
            MarkItDown().convert_stream(
                io.BytesIO(drawing_pdf()), pdf_drawing_mode=True
            )


def test_drawing_mode_precedes_custom_pdf_converters():
    class UnexpectedConverter(DocumentConverter):
        def accepts(self, *args, **kwargs):
            pytest.fail("drawing mode must not return text-only plugin results")

    md = MarkItDown()
    md.register_converter(UnexpectedConverter(), priority=-100)
    assert md.convert_stream(io.BytesIO(drawing_pdf()), pdf_drawing_mode=True).assets


def cli(tmp_path, *options):
    source = tmp_path / "drawing.pdf"
    source.write_bytes(drawing_pdf(annotation=True))
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "markitdown",
            str(source),
            "--pdf-drawing-mode",
            *map(str, options),
        ],
        capture_output=True,
    )


def test_cli_writes_external_images_and_markdown_report(tmp_path):
    output = tmp_path / "drawing.md"
    result = cli(tmp_path, "-o", output)
    assert result.returncode == 0, result.stderr.decode()
    assert "](drawing.assets/page-1.png)" in output.read_text()
    assert (tmp_path / "drawing.assets/page-1.png").is_file()
    assert "not exhaustive" in (tmp_path / "drawing.report.md").read_text()


@pytest.mark.parametrize("collision", ["output", "report", "assets"])
def test_cli_refuses_existing_output_destinations(tmp_path, collision):
    target = (
        tmp_path
        / {
            "output": "drawing.md",
            "report": "drawing.report.md",
            "assets": "drawing.assets",
        }[collision]
    )
    target.write_text("keep me")
    result = cli(tmp_path, "-o", tmp_path / "drawing.md")
    assert result.returncode != 0
    assert target.read_text() == "keep me"
    if collision != "output":
        assert not (tmp_path / "drawing.md").exists()


def test_cli_refuses_report_source_collision(tmp_path):
    result = cli(
        tmp_path,
        "-o",
        tmp_path / "drawing.md",
        "--conversion-report",
        tmp_path / "drawing.pdf",
    )
    assert result.returncode != 0
    assert (tmp_path / "drawing.pdf").read_bytes().startswith(b"%PDF-")
    assert not (tmp_path / "drawing.md").exists()


def test_cli_report_output_collision(tmp_path):
    result = cli(
        tmp_path,
        "-o",
        tmp_path / "drawing.md",
        "--conversion-report",
        tmp_path / "drawing.md",
    )
    assert result.returncode != 0
    assert not (tmp_path / "drawing.md").exists()


def test_cli_stdout_requires_report_and_inline_opt_in(tmp_path):
    result = cli(
        tmp_path, "--keep-data-uris", "--conversion-report", tmp_path / "report.md"
    )
    assert result.returncode == 0, result.stderr.decode()
    assert b"data:image/png;base64," in result.stdout
    assert (tmp_path / "report.md").exists()
    result = cli(tmp_path)
    assert result.returncode != 0


@pytest.mark.parametrize("angle", [90, 180, 270])
def test_all_orthogonal_text_rotations_keep_word_order(angle):
    result = MarkItDown().convert_stream(
        io.BytesIO(drawing_pdf(rotated=angle)), pdf_drawing_mode=True
    )
    assert "| ROOM |" in result.markdown
    assert f"rotated {angle}" in result.markdown


def test_cropped_and_rotated_multipage_pdf_accounts_for_every_page():
    result = MarkItDown().convert_stream(
        io.BytesIO(drawing_pdf(crop=True, multipage=True, page_rotation=90)),
        pdf_drawing_mode=True,
    )
    assert set(result.assets) == {"page-1.png", "page-2.png"}
    assert "## Page 2" in result.markdown
    assert "### Page 2" in result.conversion_report
    assert "ROOM" in result.markdown


@pytest.mark.parametrize(
    "destination", ["drawing.md", "drawing.report.md", "drawing.assets"]
)
def test_cli_rejects_symlink_destinations(tmp_path, destination):
    preserved = tmp_path / "preserved.txt"
    preserved.write_text("keep me")
    (tmp_path / destination).symlink_to(preserved)
    result = cli(tmp_path, "-o", tmp_path / "drawing.md")
    assert result.returncode != 0
    assert preserved.read_text() == "keep me"


def test_output_staging_failure_leaves_no_partial_output(tmp_path):
    from markitdown._drawing_output import write_drawing_output

    result = MarkItDown().convert_stream(
        io.BytesIO(drawing_pdf()), pdf_drawing_mode=True
    )
    with patch(
        "markitdown._drawing_output.os.link", side_effect=OSError("publish failed")
    ):
        with pytest.raises(OSError, match="publish failed"):
            write_drawing_output(
                str(tmp_path / "drawing.md"),
                str(tmp_path / "drawing.report.md"),
                result,
            )
    assert not list(tmp_path.iterdir())


def test_zip_keeps_distinct_page_assets_and_reports():
    import zipfile

    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("one.pdf", drawing_pdf())
        archive.writestr("two.pdf", drawing_pdf(annotation=True))
    stream.seek(0)
    result = MarkItDown().convert_stream(
        stream, stream_info=StreamInfo(extension=".zip"), pdf_drawing_mode=True
    )
    assert set(result.assets) == {"member-1/page-1.png", "member-2/page-1.png"}
    assert "## Archive member 2" in result.conversion_report
    assert "](member-2/page-1.png)" in result.markdown


def test_drawing_mode_restores_stream_position():
    stream = io.BytesIO(drawing_pdf())
    MarkItDown().convert_stream(stream, pdf_drawing_mode=True)
    assert stream.tell() == 0


def test_zip_drawing_render_failure_cannot_be_silently_skipped():
    import zipfile

    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("drawing.pdf", drawing_pdf())
    stream.seek(0)
    with patch(
        "pdfplumber.page.Page.to_image", side_effect=RuntimeError("render failed")
    ):
        with pytest.raises(Exception, match="render failed"):
            MarkItDown().convert_stream(
                stream, stream_info=StreamInfo(extension=".zip"), pdf_drawing_mode=True
            )


def test_drawing_mode_does_not_hide_missing_dependencies(monkeypatch):
    from markitdown import MissingDependencyException
    from markitdown.converters import _pdf_converter

    monkeypatch.setattr(
        _pdf_converter,
        "_dependency_exc_info",
        (ImportError, ImportError("missing PDF dependencies"), None),
    )
    with pytest.raises(MissingDependencyException):
        MarkItDown().convert_stream(io.BytesIO(drawing_pdf()), pdf_drawing_mode=True)
