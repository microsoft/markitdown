# Persian PDF acceptance baseline

The corpus contains one deterministic 22-page PDF, `persian_cases.pdf`, with
20 focused Persian/RTL cases and two English controls. Each case has a one-based
`page` in `manifest.json`. Tests copy that page into an in-memory PDF with
PDFium (already a pdfplumber dependency), then invoke the public
`MarkItDown.convert_stream` interface. A whole-document test also converts the
complete bundle through `MarkItDown.convert`. The initial report captures the unmodified converter; production fixes now make
all 22 acceptance cases pass. `baseline.json` remains the historical measurement;
`current.json` records the fixed implementation, including converter source hashes.
`manifest.json` defines authored source, intent, layout type, and direction;
`expected.json` holds logical acceptance text/matrices keyed by fixture ID,
separate from the source/layout specification.
Expected text was authored before extraction, never copied from converter output.

## Coverage and review

The cases cover sentences, paragraph boundaries, heading-before-body order,
Latin identifiers, versions, URLs, email, dates, decimals/units, parentheses,
math, Persian/Arabic Yeh and Kaf, ZWNJ, combining fatha, three numeral systems,
a ruled RTL table, and explicitly ordered RTL/LTR columns. Heading markup is
not inferred: heading text and position are asserted. Table columns are defined
in logical reading order (rightmost name first), independent of Markdown display.

All 22 pages were rendered with Poppler and visually inspected during authoring
on 2026-10-24. An initial missing-Latin-glyph problem was corrected before the
recorded baseline. Connected Persian glyphs, visible content, column placement,
heading placement and table associations were inspected. Invisible codepoints
are defined by source/expected JSON and tested as codepoints, not inferred from
pixels. **This is agent visual review, not independent human/Persian-linguist
sign-off.** Human validation remains necessary to meet that requirement fully.

No real-world documents are included yet. The real-world licensing/provenance
and independent ground-truth review deliverables remain open; do not describe
this synthetic corpus as representative of all Persian PDF producers. In
particular it has one shaping producer, no OCR, and no legacy broken encodings.

## Reproduce

From repository root, with Python 3.13 (the baseline used 3.13.5):

```sh
python -m venv .venv
.venv/bin/python -m pip install -r packages/markitdown/tests/test_files/persian/requirements-baseline.txt
.venv/bin/python -m pip install --no-deps -e packages/markitdown
.venv/bin/python -m pytest packages/markitdown/tests/test_persian_pdf.py -ra
cd packages/markitdown
../../.venv/bin/python -m tests.report_persian_pdf --output /tmp/persian-report.json
```

On Windows use `.venv\Scripts\python.exe`. Pins record the measured environment,
not a change to production requirements. Normal tests need only pytest and
MarkItDown's PDF extras; generation dependencies are not imported by tests.
Existing Hatch CI discovers `test_persian_pdf.py` automatically.

The baseline converter commit is `7482c092d9c0074a89803c9fdb63a969e7fe17fc`.
To measure that revision, create a worktree at
that SHA, copy this corpus and `report_persian_pdf.py` into its
`packages/markitdown/tests`, install that worktree's package, and run the report
command above. Do not copy the current test module into the baseline checkout:
it also imports the reconstruction helpers that did not exist at that revision. `baseline.json` records the
commit, Python/OS/package versions, PDF hashes, expected/actual output, raw
pdfminer/pdfplumber output, classifications and per-category metrics.

## Generate and inspect

```sh
python packages/markitdown/tests/test_files/persian/generate.py
pdftoppm -f 19 -l 19 -png -scale-to 1400 packages/markitdown/tests/test_files/persian/persian_cases.pdf /tmp/rtl-table
```

Generation uses fpdf2 with HarfBuzz shaping enabled and explicit `rtl`/`ltr`
base direction, A4 points, fixed creation time 2026-01-01 UTC, fixed coordinates,
14pt body and 20pt heading. Noto Sans Arabic 2.010 plus Noto Sans 2.015 Latin
fallback are bundled unchanged under SIL OFL 1.1 with their licenses. LTR
controls use Noto Sans directly. Fonts came from the bundled LibreOffice font
set; upstream copyright/source URLs are in each OFL file and font metadata.
Synthetic content and generation code use the repository's MIT license.
No normalization, presentation-form replacement, or manual string reversal is
used in generation. The source's normal Unicode bidi behavior governs mixed
runs (including the unisolated decimal/unit example).

The bundled PDF and fonts have SHA-256 checksums in `sha256.json`. Regeneration with the
pinned environment must preserve PDF bytes; inspect regenerated renders before
accepting changed hashes. Tests never download or regenerate the source PDF. Only in-memory single-page
containers are created for isolation. The report records the bundle hash and
page number for each case. Historical `baseline.json` retains the hashes of the
original separate files; the combined pages were verified pixel-identical and
both libraries' raw extraction strings matched the original baseline for all
22 cases. The combined PDF is also byte-identical across regeneration.

## Assertions and metrics

Only outer CR/LF/form-feed transport framing is removed from exact assertions.
No whitespace folding, Unicode normalization, removal of ZWNJ, bidi reversal,
or digit substitution occurs. Interior paragraph breaks are exact.

CER is Levenshtein distance over Unicode codepoints divided by expected length.
WER uses Python Unicode whitespace splitting, keeping ZWNJ inside a token and
punctuation attached. Rates can exceed one. Reading order is the fraction of
expected span pairs found in increasing order; missing/reversed spans score
zero, single-span cases have no order score. This intentionally does not
separate ordering from missing/reversed content; use raw outputs to diagnose.
Unicode diagnostics compare occurrence counts of selected variants, ZWNJ,
digits, combining marks and Latin spans. Counts are supplemental; the exact
acceptance assertion catches position changes that counts cannot detect.

Tables parse pipe-delimited Markdown cells, ignoring padding and separator
alignment syntax only. The full matrix must match, preserving shape, rows,
columns, content and header association. Structure accuracy is the fraction of
expected cells equal at their exact row/column coordinates, with shape reported
separately. A flattened table is never accepted. CER/WER for parsed tables use
canonical cell delimiters; they do not replace the matrix assertion.

## Failure policy

The historical baseline had four acceptance passes and 18 failures, linked to
our repository-local [defect ledger](ISSUES.md). Those IDs are not hosted issue
URLs. All 22 extraction assertions now run as ordinary passing tests. There are
no xfails or skips in this suite. The obsolete empty known-failure file has
been removed. Expected
text, source specifications, PDFs and font hashes have not changed.

The 18 snapshot guards that required broken output to remain unchanged have
been removed after their corresponding exact/structural assertions passed.
`test_persian_pdf.py` also includes adversarial checks for glyph mappings, logical paint
order, overlapping joiners, font metrics, English embedded RTL, missing spaces,
conservative column detection, and fallback extraction.

Never regenerate expected text from actual output or automatically create xfails.

## Reconstruction behavior and limits

Horizontal glyphs are grouped by text-matrix baseline rather than font-specific
bounding-box top; mixed fonts on one line no longer become separate form rows.
Glyph mappings are kept intact, preserving multi-codepoint ligatures, variants,
combining marks and ZWNJ. RTL glyphs and LTR runs are ordered separately, so
identifiers, dates, URL/email punctuation and numeric sequences survive. Ruled
RTL tables use cell geometry and header direction rather than inferred words.
Sparse two-column pages need a persistent gutter of at least 20% of page width,
two segments on every line, and at least two lines; ruled pages are excluded.
Wrapped RTL columns are also recognized when exactly one vertical band at least
one line-height wide is free of text across the whole page and both sides hold
two or more lines. Existing prose/form extraction remains the fallback for LTR
and unsupported layouts, including rotated text and columns with spanning
headings.

Found with Chromium/Skia output (see below), the reconstruction also:

- maps Arabic Presentation Forms (U+FB50-FDFF, U+FE70-FEFF), which that
  producer reports for shaped glyphs, to their base letters. This is the one
  deliberate normalization; ordinary letters (including Yeh/Kaf variants), ZWNJ
  and digits are never changed;
- restores ZWNJ when a font shares one glyph between space and U+200C and the
  PDF text layer can only say U+0020. A space glyph whose box the next letter
  starts inside (zero advance) is a ZWNJ; a real space advances the pen;
- keeps positioned combining marks (tanwin, hamza) on the line of the base
  letter they overlap instead of giving them their own line;
- derives paragraph breaks from the page's regular line pitch, so generous line
  spacing is not paragraph spacing, and starts a new block on a size change or a
  list marker such as `1.` or a bullet;
- takes the base direction of a wrapped paragraph from its letter counts rather
  than from one line's rightmost character, so a line that starts with Latin
  text keeps its Persian order;
- treats a bracket pair enclosing left-to-right text as part of that text, and
  restores brackets and guillemets that a shaper drew mirrored inside RTL text.

This is heuristic reconstruction, not a complete inverse Unicode bidi algorithm.
An untagged PDF may lose the metadata needed to distinguish logically different
strings with the same visual positions. Line direction is inferred from the
rightmost strong character. In RTL text a standalone Latin compound unit such
as `mg/L` displayed before a number is interpreted as quantity-before-unit;
versions and URLs are excluded from that rule. Ambiguous neutral punctuation,
explicit bidi controls, borderless RTL tables, arbitrary scripts, narrow-gutter
columns, and legacy broken encodings require additional real-document coverage.
Wrapped lines are joined with a single line break; hyphenation, footnotes, nested
lists, headers repeated on every page and Word/LaTeX encodings are untested.
All fixture tests passing does not establish correctness for every Persian PDF.

## Chromium-produced corpus

`chrome/` holds authored HTML (`cases.html`), the PDF printed from it with
headless Chrome (`chrome_cases.pdf`, producer Skia/PDF) and the logical ground
truth `chrome/expected.json`. A second producer matters because encodings differ:
Skia reports presentation forms, folds ZWNJ into the space glyph, mirrors
brackets and positions marks with offsets, none of which the fpdf2 pages show.
The 11 pages cover wrapped justified prose, headings, a numbered list, a ruled
table, mixed Latin/URL/email text, two-column pages with 40pt and 14pt gutters,
a footer page number, quotation marks and percent signs, bracketed math, and a
multi-paragraph page.

The ground truth is parsed from the HTML source by `chrome/generate.py`, never
from extraction results, and a test asserts the committed file equals that
parse. Soft line wraps inside one paragraph are folded to a space before
comparison because wrap positions are layout; paragraph boundaries, ZWNJ, digits
and punctuation are compared exactly. Skia embeds a creation date, so
regenerating changes the PDF bytes: the committed PDF is the fixture and is
hashed in `sha256.json`. Regenerate only deliberately:

```sh
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    python packages/markitdown/tests/test_files/persian/chrome/generate.py
```

The content and HTML are authored for this repository (MIT); the bundled Noto
fonts keep their OFL licenses. This remains synthetic: it adds a producer, not
real-world documents.

## Remaining dataset work

Before calling the full requested dataset complete, obtain independently reviewed
Persian ground truth and legally redistributable real PDFs spanning ordinary
prose, academic text, tables, multiple columns and mixed text. Record original
URL, license/version, permission evidence, author, download date, SHA-256,
page selection, expected reading order and a reviewer for each. Public download
availability alone is not redistribution permission. Add focused cases toward
30–50 fixtures without silently changing this initial synthetic baseline.

A researched candidate is [CTAN lshort-persian 5.01](https://ctan.org/pkg/lshort-persian), whose current catalog and upstream README specify GPL-2.0-or-later (not public domain, despite an obsolete catalog entry). It has not been imported or validated; retain applicable license/source obligations when preparing excerpts.
