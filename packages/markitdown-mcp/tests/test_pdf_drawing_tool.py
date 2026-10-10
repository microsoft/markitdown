import asyncio
import base64
import runpy
from pathlib import Path

from markitdown_mcp import __main__ as server


def test_sdk_drawing_mode_returns_inline_views_and_limitations_without_files(
    tmp_path, monkeypatch
):
    fixture = (
        Path(__file__).resolve().parents[2] / "markitdown/tests/test_pdf_drawing.py"
    )
    drawing_pdf = runpy.run_path(str(fixture))["drawing_pdf"]
    uri = (
        "data:application/pdf;base64,"
        + base64.b64encode(drawing_pdf(annotation=True)).decode()
    )
    monkeypatch.chdir(tmp_path)
    result = asyncio.run(
        server.mcp.call_tool(
            "convert_to_markdown", {"uri": uri, "pdf_drawing_mode": True}
        )
    )
    text = "\n".join(item.text for item in result.content if hasattr(item, "text"))
    assert "data:image/png;base64," in text
    assert "SHX LABEL" in text
    assert "# Drawing conversion report" in text
    assert "not exhaustive" in text
    assert not list(tmp_path.iterdir())
