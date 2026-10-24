# Fixed synthetic acceptance results

All 22 original PDF fixtures now pass their unchanged logical ground truth.
The historical baseline remains in `baseline.json` / `BASELINE.md`; `current.json`
records the fixed implementation and SHA-256 hashes of its converter sources.
Its `commit` field is the starting revision (the baseline), not the fixed one; the
source hashes identify the fixed code and must be regenerated after any change to
the converter.

| Category | Fixtures | Original passes | Current passes | Current mean CER | Current mean WER |
|---|---:|---:|---:|---:|---:|
| Basic text | 2 | 0 | 2 | 0 | 0 |
| Paragraphs, headings, RTL columns | 3 | 0 | 3 | 0 | 0 |
| Mixed RTL/LTR | 4 | 0 | 4 | 0 | 0 |
| Unicode/ZWNJ/diacritics | 3 | 0 | 3 | 0 | 0 |
| Numerals | 3 | 3 | 3 | 0 | 0 |
| Embedded LTR expressions | 4 | 0 | 4 | 0 | 0 |
| RTL table | 1 | 0 | 1 | 0 | 0 |
| LTR controls | 2 | 1 | 2 | 0 | 0 |

Reading-order accuracy is 1.0 for every fixture with multiple expected spans.
The RTL table has structure accuracy 1.0 and the correct shape. All reported
Unicode occurrence checks pass; exact assertions additionally check positions.

Validation: the consolidated `test_persian_pdf.py` and existing `test_pdf.py`
run together with `--runxfail`: **86 passed**, including the remote PDF test.
The consolidated Persian suite alone reports **49 passed**, with no skips or expected failures.
The full package suite with all optional extras installed passed
**1,212 tests with 12 existing skips and no failures**. `black --check` is clean
and `current.json` is byte-identical to a fresh `report_persian_pdf` run.
The original 18 guards requiring defective output to remain unchanged were
removed once their corresponding acceptance cases passed. The 22 separate PDFs
are now one 22-page `persian_cases.pdf`; manifest entries specify their page.
Rendered pages were verified pixel-identical to the originals and all raw
pdfminer/pdfplumber strings matched the original baseline. Expected text/matrices
and fonts remain unchanged. The added whole-document test checks cross-page
ordering as well as the isolated page assertions.

These results establish the supplied synthetic cases, not universal bidi/PDF
correctness. See README.md for reconstruction heuristics and untested layouts.
