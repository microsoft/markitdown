# Specification: Optional PDF vector-graphics diagnostic

**ID:** pdf-vector-graphics-diagnostic
**Status:** Approved
**Version:** 1.0
**Created:** 2026-11-05
**Source intent:** [changes/pdf-vector-graphics-diagnostic/intent.md](intent.md) (Approved 2026-11-05, Gary Bake)
**Owner:** Gary Bake

---

## 1. Overview

### Purpose

PDF conversion drops vector graphics (charts, diagrams, drawn figures) without telling the caller. This change adds an opt-in diagnostic. It reports which pages appear to contain meaningful vector graphics, so developers can see when the Markdown may be missing visual information.

### Desired outcome

```python
result = md.convert("architecture.pdf", detect_vector_graphics=True)
for w in result.warnings:
    print(w.page, w.code, w.counts)
```

- With the option off (the default), behaviour and output are unchanged, and `result.warnings` is `None`.
- With the option on, `result.warnings` is a list containing one `VECTOR_GRAPHICS_PRESENT` warning per affected page, and the Markdown is unchanged.

### Scope

**In scope:**
- A typed, general-purpose `ConversionWarning` object.
- A new optional `warnings` attribute on `DocumentConverterResult`.
- An opt-in vector-graphics check in the built-in `PdfConverter`, reporting per-page counts.

**Out of scope (from intent):**
- Raster images.
- Extracting, rendering or captioning graphics.
- Markdown placeholders.
- Bounding boxes.
- Populating `warnings` from any other converter.
- Changes to PDF text or table extraction.
- Upstream contribution.

**Proposed out of scope (needs approval, see DD-6):**
- A CLI flag or CLI output of warnings.
- MCP server exposure.

## 2. Functional Requirements

### FR-001: Typed conversion warning

**Description:** Provide a public, typed, immutable warning object usable by any converter.

**Trigger:** A converter creates a warning.

**Expected behaviour:**
- Exposes `code` (str), `severity` (int, a standard Python `logging` level such as `logging.WARNING`), `message` (str).
- Optionally exposes `page` (1-based int, or `None` for document-level) and `counts` (mapping of str to int, may be empty).
- Importable from the top-level `markitdown` package.
- Instances are immutable and compare by value.

**Failure behaviour:** Not applicable (a value object).

**Priority:** Must

**Source:** Intent §5 *Typed warnings*, *Field name and shape*.

### FR-002: Optional `warnings` on the conversion result

**Description:** `DocumentConverterResult` gains a `warnings` attribute.

**Trigger:** Any conversion.

**Expected behaviour:**
- `warnings` is `None` unless a converter ran a diagnostic. It is a list of `ConversionWarning` when a diagnostic ran, and an empty list means it ran and found nothing.
- The constructor accepts `warnings` as an optional keyword-only argument defaulting to `None`. Existing calls, `DocumentConverterResult(markdown=..., title=...)`, keep working unchanged.

**Failure behaviour:** Not applicable.

**Priority:** Must

**Source:** Intent §2, §4 SC5, §5 *Not checked versus nothing found*, *Public API*.

### FR-003: Opt-in vector-graphics check for PDFs

**Description:** When the caller enables the option, the built-in PDF converter inspects each page's vector drawing objects.

**Trigger:** A PDF is converted by `PdfConverter` with the option enabled.

**Expected behaviour:**
- `result.warnings` is a list.
- It contains exactly one warning per page classified as containing meaningful vector graphics (see FR-004), in ascending page order.
- Each warning has:
  - `code="VECTOR_GRAPHICS_PRESENT"`
  - `severity=logging.WARNING`
  - `message="PDF contains vector graphics that may not be represented in Markdown."`
  - `page` set to the 1-based page number
  - `counts={"curves": n, "lines": n, "rects": n}` for that page

**Failure behaviour:** See FR-006.

**Priority:** Must

**Source:** Intent §2, §4 SC2, §5 *One warning per affected page*.

### FR-004: Classification ignores table borders and decorative lines

**Description:** Straight lines and axis-aligned rectangles never cause a page to be flagged by themselves. A page is flagged when it contains at least one curve object, meaning any drawn path that is not a simple straight line or rectangle.

**Trigger:** Page classification under FR-003.

**Expected behaviour:**
- A page with only lines and/or rectangles produces no warning.
- A page with one or more curves produces a warning.
- Lines and rectangles are still reported in `counts` on flagged pages.

**Failure behaviour:** Not applicable.

**Priority:** Must

**Source:** Intent §4 SC3, SC4; §5 *Detection heuristic*. The threshold of one curve is approved as DD-4.

### FR-005: No change when the option is disabled

**Description:** With the option absent or false, conversion output, the result's existing attributes and the code path's behaviour match current behaviour, and `warnings` is `None`.

**Trigger:** Any conversion without the option.

**Priority:** Must

**Source:** Intent §2, §4 SC1, §5 *Compatibility*.

### FR-006: Check cannot complete

**Description:** If the per-page pdfplumber pass fails, the existing fallback to pdfminer still produces the Markdown exactly as today. In that case the check is reported as incomplete rather than silently returning "nothing found".

**Trigger:** The option is enabled and the pdfplumber pass raises an exception.

**Expected behaviour (DD-5):**
- `result.warnings` is a list containing one document-level warning:
  - `code="VECTOR_GRAPHICS_CHECK_INCOMPLETE"`
  - `severity=logging.INFO`
  - `page=None`
  - message: "Vector graphics check could not be completed for this PDF."
- Partial per-page results are discarded.

**Failure behaviour:** Conversion must not fail because of the check.

**Priority:** Must

**Source:** Intent §7 open question *Fallback path*. Approved as DD-5.

### FR-007: Markdown unaffected by the option

**Description:** Enabling the option never changes the Markdown or title produced for the same input.

**Priority:** Must

**Source:** Intent §4 SC6.

## 3. Non-Functional Requirements

### Performance

- With the option disabled, no additional page-object inspection is performed.
- With the option enabled, the check reuses the existing per-page pdfplumber pass. It adds no extra parse of the document and no new full-document pass.
- No numeric overhead target exists. The intent leaves this open, and none is proposed.

### Security and Privacy

- No new parsing surface. pdfplumber already parses every page on the existing path.
- Warnings contain only fixed strings, page numbers and integer counts. They contain no document text or metadata, so no document content leaks into diagnostics or logs.
- No new dependencies.

### Reliability

- The check must not raise or change the existing fallback behaviour (FR-006).
- Memory: counts are read before the existing `page.close()`, so the current memory guarantees are preserved.

### Observability

- Diagnostics are returned in the result only. No logging or Python `warnings` are emitted.

### Compatibility

- `DocumentConverterResult` constructor and attributes stay backward compatible for built-in converters, the OCR plugin, the sample plugin and third-party plugins.
- `text_content` normalisation in `MarkItDown._convert` is unaffected.
- The new keyword argument is ignored by every other converter, which already accept `**kwargs`.
- Type checking (mypy, run by the project's hatch `check` script) and black formatting continue to pass.

## 4. Proposed Solution Design

### Architecture

Observed in the existing code:
- `MarkItDown.convert*` copies caller `**kwargs` into each converter's `convert()` call (`_markitdown.py`, `_convert`). This is the same route as `keep_data_uris`, so no orchestration change is needed.
- `PdfConverter.convert` opens the document once with pdfplumber and iterates over every page, calling `page.close()` per page. It then either uses the per-page output or re-extracts with pdfminer. If pdfplumber raises, it falls back to pdfminer.

Changes:
1. **`ConversionWarning`** (new): a small frozen dataclass placed alongside `DocumentConverterResult` and exported from `markitdown`.
2. **`DocumentConverterResult`**: adds a keyword-only `warnings: Optional[List[ConversionWarning]] = None` argument and attribute.
3. **`PdfConverter`**: if `kwargs.get("detect_vector_graphics")` is truthy, then inside the existing page loop, before `page.close()`, it reads `len(page.curves)`, `len(page.lines)` and `len(page.rects)` and classifies per FR-004. It attaches the list to the result, or applies FR-006 on exception.

```
caller --convert(..., detect_vector_graphics=True)--> MarkItDown._convert --kwargs--> PdfConverter.convert
                                                                        pdfplumber page loop
                                                                          ├─ existing text/table extraction (unchanged)
                                                                          └─ [if enabled] count curves/lines/rects → classify
                                                                        DocumentConverterResult(markdown, warnings=[...])
```

### Data Model

No persistent data. New in-memory type:

| Field | Type | Notes |
|---|---|---|
| `code` | `str` | Stable machine-readable identifier, e.g. `VECTOR_GRAPHICS_PRESENT` |
| `severity` | `int` | Standard `logging` level: `logging.INFO` (20), `logging.WARNING` (30), etc. (DD-2) |
| `message` | `str` | Human-readable; fixed text, no document content |
| `page` | `Optional[int]` | 1-based page number; `None` for document-level |
| `counts` | `Mapping[str, int]` | Diagnostic counts; empty by default |

### Interfaces and Contracts

**New:**
- `markitdown.ConversionWarning`
- Warning codes `VECTOR_GRAPHICS_PRESENT` and `VECTOR_GRAPHICS_CHECK_INCOMPLETE`
- Conversion keyword argument `detect_vector_graphics: bool` (default false)

**Changed (backward compatible):** `DocumentConverterResult.__init__(markdown, *, title=None, warnings=None)` and the `DocumentConverterResult.warnings` attribute.

**Unchanged:** CLI, MCP server, all other converters.

### Key Design Decisions

**DD-1: Warning fields beyond the approved three**
- **Decision:** Add optional `page` and `counts` fields to `ConversionWarning`.
- **Rationale:** The approved per-page granularity needs a machine-readable page number and counts. Parsing these from `message` would be fragile, and named fields keep the type stable for other converters (slides, sheets).
- **Alternatives considered:** A generic `details: dict[str, Any]`. This is more flexible but less typed.
- **Trade-offs:** `counts` is integer-only, which suits this diagnostic. Future converters may need other detail types, which would mean adding fields.
- **Approval required:** Approved (Gary Bake, 2026-11-05)

**DD-2: `severity` uses standard Python `logging` levels**
- **Decision:** `severity` is an `int` taken from the standard `logging` level constants (`logging.DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). This change uses `logging.WARNING` and `logging.INFO`.
- **Rationale:** Requested by Gary Bake on 2026-11-05. Standard, familiar, and a warning can be passed straight to `logger.log(w.severity, w.message)`. `logging.getLevelName(w.severity)` gives `"WARNING"` for display.
- **Alternatives considered:**
  - Level names as strings (`"WARNING"`). These read better in a printout but are less directly usable with `logging`.
  - A custom enum.
- **Trade-offs:** This differs from the intent's illustrative `"severity": "warning"` string. The meaning is the same and the representation is standardised.
- **Approval required:** Approved (Gary Bake, 2026-11-05)

**DD-3: Opt-in mechanism**
- **Decision:** A per-call keyword argument, `detect_vector_graphics=True`.
- **Rationale:** Follows the existing `keep_data_uris` precedent and needs no change to `MarkItDown`.
- **Alternatives considered:** A `MarkItDown(...)` constructor option, like `llm_client`, which would need forwarding code in `_convert`. A generic `diagnostics=True` was rejected because only PDF honours it, which would be misleading.
- **Trade-offs:** It must be passed on every call.
- **Approval required:** Approved (Gary Bake, 2026-11-05)

**DD-4: Classification rule (one or more curves)**
- **Decision:** Flag a page when `curves ≥ 1`. Lines and rects never trigger alone.
- **Rationale:** This is the simplest rule that satisfies the approved "ignore table borders and decorative lines". It was verified by experiment on 2026-11-05 with hand-built PDFs: a Bézier pie slice and a polyline chart each classified as one curve, a horizontal rule as one line, and filled bars as rects. All existing PDF fixtures, including table-heavy forms, contain zero curves.
- **Alternatives considered:**
  - A minimum curve count or size threshold. This reduces false positives but there is no data yet to calibrate it.
  - Weighted scoring across all object types.
- **Trade-offs (known limitations):**
  - Bar charts and other rectangle-only charts are **not** flagged.
  - Rounded-corner boxes, verified to classify as curves, and PDFs that draw text as outlines **are** flagged (false positives).
  - Both are accepted under the intent's "ignore borders, revisit later" decision but should be documented.
- **Approval required:** Approved (Gary Bake, 2026-11-05); limitations accepted

**DD-5: Incomplete check**
- **Decision:** On a pdfplumber failure, return `[VECTOR_GRAPHICS_CHECK_INCOMPLETE]`, keep the existing Markdown fallback, and discard partial results.
- **Rationale:** `None` would wrongly mean "not requested", and `[]` would wrongly mean "nothing found".
- **Alternatives considered:**
  - `None`. This is simpler, but the caller cannot tell a failure from "not checked".
  - Keeping the partial per-page warnings plus the incomplete warning. This gives more information but more cases to test.
- **Trade-offs:** Introduces a second code not in the intent's example.
- **Approval required:** Approved (Gary Bake, 2026-11-05) (resolves an intent open question)

**DD-6: CLI and MCP**
- **Decision:** No CLI or MCP changes in this version. Python API only.
- **Rationale:** Smallest change that meets the intent. The CLI has no existing channel for non-Markdown output.
- **Alternatives considered:** A `--detect-vector-graphics` flag printing warnings to stderr.
- **Approval required:** Approved (Gary Bake, 2026-11-05): Python API only (resolves an intent open question)

**DD-7: Other converters handling PDFs**
- **Decision:** When a PDF is handled by a different converter (OCR plugin at priority -1, Document Intelligence, Content Understanding), `warnings` stays `None` even if the option was passed. The same applies to PDFs nested inside a ZIP, because `ZipConverter` builds its own result.
- **Rationale:** `None` correctly means "not checked". Populating `warnings` from other converters is out of scope.
- **Approval required:** No (follows from the approved scope), but recorded for visibility.

## 5. Behaviour and Edge Cases

| Case | Behaviour |
|---|---|
| Option absent or `False` | `warnings is None`; output identical to today (FR-005) |
| Option on, no curves on any page | `warnings == []` |
| Option on, only table borders or rules | `warnings == []` (FR-004) |
| Option on, curves on pages 2 and 5 | Two warnings, `page=2` then `page=5` |
| Option on, PDF with no form pages (pdfminer whole-document path) | Check still uses the pdfplumber pass, which already runs over every page; Markdown is from pdfminer as today |
| Option on, pdfplumber raises | Markdown from the pdfminer fallback as today; `warnings == [VECTOR_GRAPHICS_CHECK_INCOMPLETE]` (FR-006, DD-5) |
| Option on, pdfminer fallback also fails | Same exception behaviour as today; no result returned |
| Option on, zero-page or empty PDF | `warnings == []` if pdfplumber succeeds |
| Option on, non-PDF input | Option ignored; `warnings is None` |
| Option on, PDF handled by OCR plugin, DocIntel, CU, or nested in ZIP | `warnings is None` (DD-7) |
| Encrypted or malformed PDF | Unchanged from today; the check follows the FR-006 path if pdfplumber raises |
| Truthy non-bool value for the option | Treated as enabled (consistent with existing `kwargs.get` usage) |

## 6. Acceptance Criteria

### AC-001: Default behaviour unchanged

**Related requirements:** FR-005, FR-002

**Given:** Each existing PDF in `tests/test_files`.

**When:** Converted without the option.

**Then:** The Markdown equals the output before the change, `warnings is None`, and the existing test suite passes unmodified.

### AC-002: Graphics page flagged with counts

**Related requirements:** FR-003, FR-004

**Given:** A PDF whose page 1 has a Bézier figure.

**When:** Converted with the option enabled.

**Then:** `warnings` contains exactly one `ConversionWarning` with `code="VECTOR_GRAPHICS_PRESENT"`, `severity=logging.WARNING`, `page=1`, the approved message, and `counts["curves"] ≥ 1`.

### AC-003: Per-page warnings, in order

**Related requirements:** FR-003

**Given:** A multi-page PDF where only some pages contain curves.

**When:** Converted with the option enabled.

**Then:** There is one warning per curve-bearing page, in ascending page order, and none for other pages.

### AC-004: Borders and rules not flagged

**Related requirements:** FR-004

**Given:** Existing table and form fixtures (rects and lines, zero curves) and a PDF containing only a horizontal rule.

**When:** Converted with the option enabled.

**Then:** `warnings == []`.

### AC-005: Checked with nothing found is distinguishable

**Related requirements:** FR-002, FR-003

**Given:** A plain-text PDF.

**When:** Converted once with the option and once without.

**Then:** `warnings == []` with the option and `warnings is None` without.

### AC-006: Markdown unaffected by enabling

**Related requirements:** FR-007

**Given:** Each existing PDF fixture and each new graphics fixture.

**When:** Converted with and without the option.

**Then:** `markdown` and `title` are identical in both runs.

### AC-007: Incomplete check reported

**Related requirements:** FR-006

**Given:** pdfplumber raises during page processing (simulated).

**When:** Converted with the option enabled.

**Then:** The Markdown equals the pdfminer fallback output and `warnings` contains exactly one `VECTOR_GRAPHICS_CHECK_INCOMPLETE` warning with `page is None`.

### AC-008: Other converters and plugins unaffected

**Related requirements:** FR-002, NFR Compatibility

**Given:** Non-PDF inputs, and a result constructed positionally or with `title=` only.

**When:** Converted with or without the option.

**Then:** Conversion succeeds and `warnings is None`.

### AC-009: Public type available

**Related requirements:** FR-001

**When:** `from markitdown import ConversionWarning` is run.

**Then:** It succeeds. Instances are immutable and compare equal by value.

## 7. Verification Strategy

### Automated Tests

- **Unit tests:** `ConversionWarning` behaviour, and `DocumentConverterResult` defaults and constructor compatibility (AC-008, AC-009).
- **PDF tests** in `tests/test_pdf.py`:
  - AC-001 to AC-007, using existing fixtures for the negative cases.
  - New small positive fixtures (Bézier figure, polyline chart, multi-page mix, rule only). Proposed: generate these with a stdlib-only script, as the 2026-11-05 experiment showed is feasible, so no fixture-generation dependency is added. Commit the fixtures beside the existing generator-script convention.
- **Fallback test:** patch pdfplumber to raise, using the same `unittest.mock.patch` approach the test module already uses (AC-007).
- **Static checks:** mypy (hatch `check`) and black.

### Manual Verification

- Run the check on a few real-world PDFs containing charts and diagrams, if available. This gives a qualitative check of the DD-4 false positive and false negative rates.

### Security and Operational Verification

- Confirm no document text appears in any warning field (review and test assertion on fixed messages).
- Confirm no new runtime dependency is added to `pyproject.toml`.

**Cannot currently be verified:** real-world detection accuracy, because no representative sample PDFs have been provided (intent open question).

## 8. Dependencies and Risks

### Dependencies

- pdfplumber's `page.curves`, `page.lines` and `page.rects`. These are already a dependency and their behaviour was verified on 2026-11-05 with the installed version.

### Risks

**Risk:** Heuristic accuracy. Bar charts are missed and rounded boxes or outlined text are flagged.
- **Impact:** Medium
- **Mitigation:** Document the limitations. Keep the rule in one place so it can be tuned later.
- **Residual concern:** No real-world calibration data.

**Risk:** A public API change to a shared base class.
- **Impact:** Low
- **Mitigation:** Keyword-only argument with a `None` default. The change is fork-local.
- **Residual concern:** Divergence from upstream may complicate future merges from microsoft/markitdown.

**Risk:** Graphics inside form XObjects may not be counted.
- **Impact:** Low/Medium
- **Mitigation:** Add a fixture with a graphic inside a form XObject during implementation and record the result.
- **Residual concern:** Unverified (see assumptions).

**Risk:** Callers using the OCR plugin or DocIntel get `None` and may assume the check ran.
- **Impact:** Low
- **Mitigation:** `None` is documented as "not checked". The docstring for the option states it applies to the built-in PDF converter only.

## 9. Assumptions and Open Questions

### Confirmed Assumptions

- Fork-local; not for upstream (Gary Bake, 2026-11-05).
- `warnings`: `None` means not checked, `[]` means checked with nothing found. Entries are typed objects, one per affected page (Gary Bake, 2026-11-05).
- pdfplumber classifies Bézier and polyline paths as curves, straight segments as lines, and axis-aligned rectangles as rects. Rounded boxes are curves (observed by experiment, 2026-11-05).

### Unconfirmed Assumptions

- pdfplumber's object lists include paths drawn inside form XObjects.
- Reading `page.curves` before `extract_text()` or `extract_words()` does not alter extraction output. AC-006 will verify this.

### Open Questions

- Sample real-world PDFs for manual verification (non-blocking).
- Cognitive Ownership development objective (non-blocking; the team policy is an unadopted example).

No open questions block implementation.

## 10. Intent Traceability

| Intent reference | Specification reference | Verification |
|---|---|---|
| SC1: Default output identical; suite passes | FR-005, NFR Compatibility | AC-001 |
| SC2: Per-page detection with counts | FR-003 | AC-002, AC-003 |
| SC3: Borders and decorative lines not flagged | FR-004, DD-4 | AC-004 |
| SC4: Representative figure flagged | FR-003, FR-004 | AC-002 |
| SC5: Default "not checked"; distinguishable | FR-002 | AC-005, AC-008 |
| SC6: Markdown unchanged when enabled | FR-007 | AC-006 |
| C: Field name `warnings`, code/severity/message, `VECTOR_GRAPHICS_PRESENT` | FR-001, FR-002, FR-003 | AC-002, AC-009 |
| C: One warning per affected page | FR-003 | AC-003 |
| C: Typed warnings | FR-001, DD-1, DD-2 | AC-009 |
| C: Public API backward compatible | FR-002 | AC-008 |
| C: Only PDF populates | DD-7 | AC-008 |
| C: No new dependencies | NFR Security | Review of `pyproject.toml` |
| C: No overhead when disabled | NFR Performance | Code review (no numeric target) |
| Out of scope (raster images, placeholders, bounding boxes, other converters) | §1 Scope | Review |

**Introduced during design (approved by Gary Bake, 2026-11-05):**
- FR-006 / DD-5: the `VECTOR_GRAPHICS_CHECK_INCOMPLETE` code.
- DD-1: the `page` and `counts` fields.
- DD-3: the option name.
- DD-6: CLI and MCP excluded.
- DD-2: `severity` uses standard `logging` levels instead of the intent example's string.

## 11. Design Review and Approval

**Decision:** Approved

**Reviewed by:** Gary Bake

**Review date:** 2026-11-05

**Technical review required:** Yes (public API addition to a shared base class)

**Blocking issues:** None

**Approval notes:** DD-1 to DD-6 approved individually; DD-2 revised to standard Python `logging` levels at the reviewer's request. Spec approved as a whole on 2026-11-05.
