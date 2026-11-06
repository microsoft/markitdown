"""Run with python -m tests.report_persian_pdf --output /tmp/baseline.json."""

import argparse
import hashlib
import io
import importlib.metadata
import json
import platform
import re
import subprocess
from collections import defaultdict
from pathlib import Path

import pdfminer.high_level
import pdfplumber
import pypdfium2
from markitdown import MarkItDown, StreamInfo
from markitdown.converters import _pdf_converter

ROOT = Path(__file__).parent / "test_files" / "persian"
CASES = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
EXPECTED = json.loads((ROOT / "expected.json").read_text(encoding="utf-8"))


BUNDLE = ROOT / "persian_cases.pdf"


def case_pdf(case):
    """Copy one fixture page without changing glyphs, fonts or text encoding.

    PDFium is already a dependency of pdfplumber. Only the page container is
    rebuilt; extraction still runs through MarkItDown's public API.
    """
    output = io.BytesIO()
    with pypdfium2.PdfDocument(BUNDLE) as source:
        with pypdfium2.PdfDocument.new() as selected:
            selected.import_pages(source, pages=[case["page"] - 1])
            selected.save(output)
    output.seek(0)
    return output


def expected(case):
    return EXPECTED[case["id"]]


def body(text):
    # PDF page terminators and outer line breaks are transport framing only.
    return text.strip("\n\r\f")


def distance(a, b):
    previous = list(range(len(b) + 1))
    for i, left in enumerate(a, 1):
        current = [i]
        for j, right in enumerate(b, 1):
            current.append(
                min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (left != right))
            )
        previous = current
    return previous[-1]


def table_rows(text):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            cells = [cell.strip() for cell in line[1:-1].split("|")]
            if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            rows.append(cells)
    return rows


def order_accuracy(blocks, actual):
    if len(blocks) < 2:
        return None
    positions = [actual.find(block) for block in blocks]
    pairs = [(i, j) for i in range(len(blocks)) for j in range(i + 1, len(blocks))]
    return sum(0 <= positions[i] < positions[j] for i, j in pairs) / len(pairs)


def evaluate(case, actual):
    truth = expected(case)
    actual = body(actual)
    rows = table_rows(actual) if isinstance(truth, list) else None
    text = "\n".join(" | ".join(row) for row in truth) if rows is not None else truth
    comparison = (
        "\n".join(" | ".join(row) for row in rows) if rows is not None else actual
    )
    if rows is not None and not rows:
        comparison = actual  # A flattened table is not a successful table.
    spans = case["blocks"] if rows is None else [cell for row in truth for cell in row]
    result = {
        "pass": rows == truth if rows is not None else actual == truth,
        "cer": distance(text, comparison) / max(1, len(text)),
        # Unicode whitespace splitting; ZWNJ stays inside words, punctuation attached.
        "wer": distance(text.split(), comparison.split()) / max(1, len(text.split())),
        "reading_order_accuracy": order_accuracy(spans, actual),
        "exact_span_preservation": sum(actual.count(s) == text.count(s) for s in spans)
        / max(1, len(spans)),
        "unicode_sequence_preservation": {
            s: actual.count(s) == text.count(s)
            for s in re.findall(
                r"[\u200c\u06cc\u064a\u06a9\u0643\u06f0-\u06f9\u0660-\u0669\u064b-\u065f]|[A-Za-z0-9][A-Za-z0-9:/@.+=-]*",
                text,
            )
        },
    }
    if rows is not None:
        total = sum(map(len, truth))
        result["table_structure_accuracy"] = (
            sum(
                r < len(rows) and c < len(rows[r]) and cell == rows[r][c]
                for r, row in enumerate(truth)
                for c, cell in enumerate(row)
            )
            / total
        )
        result["table_shape_correct"] = len(rows) == len(truth) and all(
            len(row) == len(truth[i]) for i, row in enumerate(rows)
        )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = {
        "commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip(),
        "python": platform.python_version(),
        "os": platform.platform(),
        # HEAD alone cannot identify an implementation measured before commit.
        "converter_source_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(Path(_pdf_converter.__file__).parent.glob("_pdf*.py"))
        },
        "versions": {
            name: importlib.metadata.version(name)
            for name in [
                "markitdown",
                "pdfplumber",
                "pdfminer.six",
                "fpdf2",
                "uharfbuzz",
                "fonttools",
                "pytest",
            ]
        },
        "fixtures": [],
    }
    converter = MarkItDown()
    groups = defaultdict(list)
    for case in CASES:
        source = case_pdf(case)
        actual = converter.convert_stream(
            source, stream_info=StreamInfo(extension=".pdf")
        ).markdown
        metrics = evaluate(case, actual)
        source.seek(0)
        with pdfplumber.open(source) as pdf:
            plumber = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
        row = dict(
            id=case["id"],
            category=case["category"],
            sha256=hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            page=case["page"],
            expected=expected(case),
            actual=actual,
            metrics=metrics,
            pdfminer=pdfminer.high_level.extract_text(case_pdf(case)),
            pdfplumber=plumber,
            classification=None if metrics["pass"] else {"category": "Unclassified"},
        )
        report["fixtures"].append(row)
        groups[case["category"]].append(metrics)
    report["categories"] = {
        category: {
            "count": len(rows),
            "passed": sum(row["pass"] for row in rows),
            **{
                key: sum(row[key] for row in rows if row.get(key) is not None)
                / sum(row.get(key) is not None for row in rows)
                for key in [
                    "cer",
                    "wer",
                    "reading_order_accuracy",
                    "table_structure_accuracy",
                ]
                if any(row.get(key) is not None for row in rows)
            },
        }
        for category, rows in groups.items()
    }
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
