# Persian PDF defect ledger

These repository-local issue IDs track actionable reproductions. They are **not
published GitHub issues**. Status: resolved for the synthetic reproductions; see `current.json`. Baseline revision:
`7482c092d9c0074a89803c9fdb63a969e7fe17fc`. Originally affected fixtures,
classifications, expected/actual strings and dependency diagnostics are in
`baseline.json`. No active known failures remain. Production fixes
are in `_pdf_layout.py` and its converter integration.
The descriptions below document original behavior; every affected fixture now
passes its original exact/structural assertion without an expected-failure mark.

## RTL-001

Resolution: order glyph mappings and directional runs separately; retain
ligatures and coincident joiners/combining marks without normalization.

**Logical Persian strings are extracted in visual character order.**

Reproduce with `basic_sentence`: expected `این یک سند آزمایشی برای بررسی استخراج متن فارسی است.`;
actual `.تسا یسراف نتم جارختسا یسررب یارب یشیامزآ دنس کی نیا`.
The same issue affects simple sentences, paragraphs, headings, letter variants,
ZWNJ, combining marks, and several mixed runs. English identifiers such as
`DOC-2026-A15` survive in some cases; do not claim universal Latin reversal.
The standalone numeral fixtures pass. ZWNJ counts can survive while their
logical positions do not. These are string defects, not merely bidi rendering.

For the affected fixtures MarkItDown agrees with pdfminer after outer page
framing is removed. This supports an upstream extraction limitation, not proof
that every PDF producer or upstream version is affected. A fix should preserve
original codepoints without Arabic/Persian normalization.

## RTL-002

Resolution: group mixed-font glyphs by their shared text-matrix baseline and
reconstruct RTL prose before running the form heuristic.

**Mixed-font prose is incorrectly classified as a form/table.**

Fixtures: `contract_date`, `url`, `parentheses_math`. The rendered single line
contains intact expressions, but MarkItDown emits multiple table cells/rows.
For example the URL is split into `https`, `//example`, and `com` headers.
Raw pdfminer and pdfplumber outputs in the report provide the comparison;
MarkItDown's form inference adds structural damage beyond RTL reversal.
The fixture uses Noto Arabic plus Latin fallback, whose glyph positions/font
metrics exercise the form heuristic. This is not evidence about single-font
PDFs. Acceptance: exact original logical line, no invented table.

## RTL-003

Resolution: recognize a persistent wide gutter and finish each column in its
inferred direction. Ruled tables and spanning headings are excluded.

**Two-column documents interleave rows instead of finishing a column.**

Fixtures: `two_column_rtl`, `two_column_ltr`. Both have two lines per column.
Expected: right then left for the RTL fixture, left then right for the LTR
control, each top to bottom. Actual: left-top, right-top, left-bottom,
right-bottom (Persian characters additionally reverse). pdfminer produces the
same order. The LTR reproduction demonstrates that this layout limitation is
not specific to Persian. A future fix must respect explicit per-fixture order.

## RTL-004

Resolution: use ruled cell geometry, rebuild each cell from directional glyph
runs, and order columns using the header direction.

**RTL table associations and embedded identifiers are damaged.**

Fixture: `rtl_table`. Rightmost name, middle code, leftmost quantity are the
specified logical column order. MarkItDown emits reversed columns, reverses
Persian cell characters, and places `PE`/`PP` outside the rows containing their
numeric suffixes. Acceptance: the entire expected matrix, including header
association and row order; a bag of correct tokens or a flattened table fails.
Inspect the raw library output before attributing each symptom upstream:
MarkItDown's heuristic adds cell reconstruction on top of library words.
