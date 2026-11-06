#!/usr/bin/env python3 -m pytest
"""--use-docintel must keep the CLI's filename-optional stdin mode."""

import io
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from markitdown.__main__ import main

DOC_INTEL = "markitdown.converters._doc_intel_converter"


def test_use_docintel_reads_from_stdin(monkeypatch, capsys) -> None:
    pdf_bytes = b"%PDF-1.4 fake pdf"
    monkeypatch.setattr(sys, "stdin", SimpleNamespace(buffer=io.BytesIO(pdf_bytes)))
    monkeypatch.setattr(
        sys,
        "argv",
        ["markitdown", "--use-docintel", "-e", "https://fake-di", "-x", "pdf"],
    )
    monkeypatch.delenv("AZURE_API_KEY", raising=False)

    client = MagicMock()
    client.begin_analyze_document.return_value.result.return_value.content = (
        "# Converted by Document Intelligence"
    )
    request = MagicMock()

    with patch(f"{DOC_INTEL}._dependency_exc_info", None), patch(
        f"{DOC_INTEL}.DocumentIntelligenceClient", return_value=client
    ), patch(f"{DOC_INTEL}.DefaultAzureCredential"), patch(
        f"{DOC_INTEL}.DocumentAnalysisFeature"
    ), patch(
        f"{DOC_INTEL}.AnalyzeDocumentRequest", request
    ):
        main()

    # The bytes read from stdin are what gets sent to Document Intelligence
    request.assert_called_once_with(bytes_source=pdf_bytes)
    assert capsys.readouterr().out.strip() == "# Converted by Document Intelligence"
