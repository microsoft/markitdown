# Implementation Plan: Optional PDF vector-graphics diagnostic

**ID:** pdf-vector-graphics-diagnostic
**Status:** Draft
**Version:** 0.1
**Created:** 2026-11-05
**Source intent:** [changes/pdf-vector-graphics-diagnostic/intent.md](intent.md) (Approved 2026-11-05, Gary Bake)
**Source specification:** [changes/pdf-vector-graphics-diagnostic/spec.md](spec.md) (Approved v1.0, 2026-11-05, Gary Bake)
**Owner:** Gary Bake

---

## 1. Implementation Overview

### Objective

Implement the approved specification: an opt-in `detect_vector_graphics` conversion option. With it enabled, the built-in `PdfConverter` returns one typed `ConversionWarning` per page containing vector curves in a new `DocumentConverterResult.warnings` attribute. Default behaviour is unchanged and `warnings` is `None`.

### Approach

1. Add a frozen `ConversionWarning` dataclass and a keyword-only `warnings=None` argument to `DocumentConverterResult` in `_base_converter.py`. Export the class from `markitdown`.
2. Add small, dependency-free PDF fixtures, built by a stdlib-only generator script, covering curves, polylines, rules and multi-page mixes.
3. In `PdfConverter.convert`, when `kwargs.get("detect_vector_graphics")` is truthy, read `len(page.curves/lines/rects)` inside the existing pdfplumber page loop before `page.close()`.
   - Pages with at least one curve produce a `VECTOR_GRAPHICS_PRESENT` warning at `logging.WARNING`.
   - If the page loop does not complete, the result carries a single `VECTOR_GRAPHICS_CHECK_INCOMPLETE` warning at `logging.INFO`.
   - Markdown extraction logic is not touched.

No change to `MarkItDown._convert`. Caller kwargs already reach converters (verified).

### Scope

**In scope:**
- Spec FR-001 to FR-007 and AC-001 to AC-009.
- Fixtures and tests.
- Docstrings documenting the option and the DD-4 limitations.

**Out of scope:**
- CLI and MCP changes (DD-6).
- README changes.
- Other converters populating `warnings`.
- Raster images.
- Changes to PDF text or table extraction.
- Upstream contribution.

## 2. Codebase Analysis

All paths are relative to `packages/markitdown/`. Everything in the table below was verified by inspection on 2026-11-05.

### Existing Components

| Component / File | Current Responsibility | Planned Change |
|---|---|---|
| `src/markitdown/_base_converter.py` | `DocumentConverterResult(markdown, *, title=None)`, `text_content` alias, `DocumentConverter` base | Add `ConversionWarning`; add `warnings` keyword argument and attribute |
| `src/markitdown/__init__.py` | Public exports and `__all__` | Export `ConversionWarning` |
| `src/markitdown/converters/_pdf_converter.py` | `PdfConverter.convert`: a pdfplumber per-page loop with `page.close()`; whole-document pdfminer if there are no form pages; `except Exception` falls back to pdfminer; a second fallback if empty; partial-numbering post-processing | Add the optional per-page counting and warnings; extend docstrings |
| `src/markitdown/_markitdown.py` `_convert` | Copies caller kwargs to each converter; normalises only `text_content` on the returned result | None |
| `tests/test_pdf.py` | 37 PDF tests (baseline: 37 passed via `hatch test tests/test_pdf.py`, 2026-11-05); uses `unittest.mock.patch` | Add diagnostic tests |
| `tests/test_files/generate_pdf_cleanup_fixtures.py` | Fixture generator convention (uses PyMuPDF, which is not installed in the root venv) | None; a new stdlib-only generator follows the same convention |

### Existing Patterns to Reuse

- Per-call opt-in via `**kwargs`, like `keep_data_uris`.
- Committed binary fixtures in `tests/test_files/` alongside a generator script.
- `unittest.mock.patch` in `tests/test_pdf.py` to simulate failures.
- Keyword-only optional constructor arguments on `DocumentConverterResult`.

### Technical Constraints

- **Verified:** the pdfplumber `page.curves`, `page.lines` and `page.rects` classification. A hand-built Bézier and a polyline each give one curve, a rule gives one line, bars give rects, and a rounded box gives one curve. All 12 existing PDF fixtures have zero curves.
- **Verified:** `DocumentConverterResult` is constructed in 23 places outside the tests, including the OCR and sample plugins. All of them use `markdown=` with an optional `title=`, so a new keyword-only argument with a default is compatible.
- **Verified:** inside `convert`, the `try` block covers both the pdfplumber loop **and** the whole-document pdfminer call. An exception from pdfminer after a completed loop would also reach `except`. A "loop completed" flag is therefore required so that a finished check is not reported as incomplete.
- **Verified:** black (`~/.local/bin/black`) and pytest are available. `.pre-commit-config.yaml` pins black 26.10.1. CI runs `hatch test` and `pre-commit run --all-files`.
- **Not verified:** the mypy `types` hatch environment is not created locally. Creating it installs packages from the network. See the gate in §10.

## 3. Files and Modules

| File / Module | Action | Purpose |
|---|---|---|
| `src/markitdown/_base_converter.py` | Modify (**shared public API**) | `ConversionWarning`; `warnings` on the result |
| `src/markitdown/__init__.py` | Modify (**public API**) | Export `ConversionWarning` |
| `src/markitdown/converters/_pdf_converter.py` | Modify | Detection and warnings |
| `tests/test_conversion_warnings.py` | Create (proposed path) | Unit tests for the type and result compatibility |
| `tests/test_pdf.py` | Modify (append only) | Diagnostic tests; existing tests untouched |
| `tests/test_files/generate_vector_graphics_fixtures.py` | Create (proposed path) | Stdlib-only fixture generator |
| `tests/test_files/vector_graphics_*.pdf` | Create (proposed names) | Fixtures listed in TASK-002 |
| `changes/pdf-vector-graphics-diagnostic/plan.md` | Modify during execution | Progress and evidence |

No schema, auth, infrastructure, configuration or dependency changes.

## 4. Implementation Tasks

### TASK-001: Warning type and result field

**Objective:** Add the public `ConversionWarning` type and the optional `warnings` attribute.

**Requirements:** FR-001, FR-002

**Acceptance criteria:** AC-008 (the result-construction part), AC-009

**Dependencies:** None

**Files affected:** `src/markitdown/_base_converter.py`, `src/markitdown/__init__.py`, `tests/test_conversion_warnings.py`

**Steps:**
1. Write `ConversionWarning` as `@dataclass(frozen=True)` with fields:
   - `code: str`
   - `severity: int`, documented as a standard `logging` level
   - `message: str`
   - `page: Optional[int] = None`, 1-based
   - `counts: Mapping[str, int] = field(default_factory=dict)`

   The docstring should explain the fields and the `None` versus `[]` semantics. Note: a frozen dataclass containing a dict is not hashable. That is acceptable, because the spec requires immutability and value equality, not hashing. Wrapping counts in `types.MappingProxyType` is optional; keep it simple.
2. Extend `DocumentConverterResult.__init__` with a keyword-only argument `warnings: Optional[List[ConversionWarning]] = None` and store it as `self.warnings`. Update the docstring.
3. Add `ConversionWarning` to the imports and `__all__` in `__init__.py`.
4. Write the unit tests:
   - The import works.
   - Fields and defaults are correct.
   - Assigning to an attribute raises `FrozenInstanceError`.
   - Equal values compare equal.
   - `DocumentConverterResult("x").warnings is None`.
   - `DocumentConverterResult(markdown="x", title="t")` still works.
   - `warnings=[w]` is stored.

**Verification:**
- `hatch test tests/test_conversion_warnings.py`: all pass.
- `hatch test`: the full suite passes with no regressions.
- `black --check src tests`: clean.

**Completion conditions:**
- [ ] Type and field implemented with docstrings.
- [ ] New and existing tests pass.
- [ ] No other converter modified.

### TASK-002: Vector-graphics fixtures

**Objective:** Provide deterministic positive and negative PDFs without adding dependencies.

**Requirements:** Supports FR-003, FR-004 and FR-006 testing

**Acceptance criteria:** Enables AC-002 to AC-006

**Dependencies:** None (can run before or after TASK-001)

**Files affected:** `tests/test_files/generate_vector_graphics_fixtures.py`, `tests/test_files/vector_graphics_*.pdf`

**Steps:**
1. Write a stdlib-only generator that emits minimal valid PDFs with correct xref offsets. Each page has a Helvetica text line so the Markdown is non-empty, plus drawing operators. It should follow the docstring and run-instructions style of `generate_pdf_cleanup_fixtures.py`.
2. Generate:
   - `vector_graphics_curve.pdf`: one page, text plus a Bézier pie slice.
   - `vector_graphics_mixed.pdf`: three pages. Page 1 has a curve, page 2 is text only, page 3 has a polyline chart.
   - `vector_graphics_rule_only.pdf`: text plus a horizontal rule and a rectangle box.
   - `vector_graphics_form_xobject.pdf`: a Bézier drawn inside a form XObject. This resolves the spec's unverified assumption.
3. Check with a one-off pdfplumber script that each page has the expected curve, line and rect counts and that its text is extractable.

**Verification:**
- Running the generator twice produces byte-identical files.
- The pdfplumber counts match the expectations above. Record the actual form XObject curve count in §11.

**Completion conditions:**
- [ ] Fixtures committed-ready, with no new dependency.
- [ ] Form XObject behaviour recorded. If curves inside the XObject are **not** counted, record it as a known limitation (DEV entry, no approval needed, since it is within the DD-4 accepted limitations). Do not add extra detection logic.

### TASK-003: PDF detection and warnings

**Objective:** Implement detection, the warnings and the incomplete-check behaviour in `PdfConverter`.

**Requirements:** FR-003, FR-004, FR-005, FR-006, FR-007

**Acceptance criteria:** AC-001 to AC-007, AC-008 (non-PDF part)

**Dependencies:** TASK-001, TASK-002

**Files affected:** `src/markitdown/converters/_pdf_converter.py`, `tests/test_pdf.py`

**Steps:**
1. Add module constants for the codes, the approved message texts and the curve threshold (`1`), and a small helper that turns per-page counts into a `ConversionWarning` or `None`.
2. In `convert`:
   - Set `detect = bool(kwargs.get("detect_vector_graphics"))`.
   - If detecting, set up `page_warnings: list = []` and `check_complete = False`.
   - Inside the existing loop, before `page.close()` and only if detecting, read the three counts and append any warning with `page=page_idx + 1`.
   - Set `check_complete = True` immediately after the `with pdfplumber.open(...)` block ends.
3. After all existing Markdown logic (unchanged):
   - If not detecting, `warnings = None`.
   - Elif `check_complete`, `warnings = page_warnings`.
   - Else, `warnings = [ConversionWarning(VECTOR_GRAPHICS_CHECK_INCOMPLETE, logging.INFO, msg, page=None)]`.

   Pass `warnings=` to `DocumentConverterResult`. Counting must sit outside the extraction calls and must not alter their arguments or order.
4. Update the `PdfConverter` docstring to describe the option, that it applies to the built-in converter only, and the limitations (bar charts missed; rounded boxes and outlined text flagged).
5. Append tests to `tests/test_pdf.py`:
   - **AC-001:** for every existing PDF fixture, without the option, `warnings is None`. The existing tests already cover the Markdown.
   - **AC-002:** curve fixture gives one warning with all fields and `counts["curves"] >= 1`.
   - **AC-003:** mixed fixture gives pages `[1, 3]` in order.
   - **AC-004:** the rule-only fixture and all existing fixtures with the option give `[]`.
   - **AC-005:** plain PDF gives `[]` with the option and `None` without.
   - **AC-006:** for all existing and new fixtures, `markdown` and `title` are equal with and without the option.
   - **AC-007:** patch `pdfplumber.open` to raise. The Markdown equals pdfminer output and `warnings` holds one incomplete warning with `page is None` and `severity == logging.INFO`.
   - **Complete-check-not-misreported case:** patch `pdfminer.high_level.extract_text` to raise on its first call only, on a no-form-page PDF. The warnings must not include the incomplete code.
   - **AC-008:** a non-PDF fixture (for example `test.docx`) with the option gives `warnings is None`.

**Verification:**
- `hatch test tests/test_pdf.py`: all pass. 37 existing plus the new tests; the existing tests are unmodified.
- `git diff tests/test_pdf.py` shows additions only.

**Completion conditions:**
- [ ] AC-001 to AC-008 automated and passing.
- [ ] No change to Markdown extraction code paths beyond the added counting.
- [ ] Docstrings updated.

### TASK-004: Full verification and static checks

**Objective:** Prove no regressions and that the code passes the project's quality gates.

**Requirements:** All; NFR Compatibility

**Acceptance criteria:** AC-001 to AC-009

**Dependencies:** TASK-003

**Files affected:** `plan.md` (evidence only)

**Steps:**
1. `hatch test` (full suite).
2. `black --check .` from the repository root. If the global black version differs from the pinned 26.10.1 and the output disagrees, use `pre-commit run black --all-files`. Note that pre-commit may download hooks.
3. mypy through `hatch run types:check` (GATE-1 approved; required). If mypy reports errors that already exist on the baseline, record them separately from any errors introduced by this change.
4. `git diff --stat` and `git diff -- pyproject.toml`: no dependency changes, and no files outside §3.
5. Confirm by inspection and test assertions that warning messages contain no document text.
6. Record the results in §13 and request independent verification (the `verifier` agent).

**Verification:** All commands succeed. Any pre-existing failures unrelated to this change are recorded with their output, not "fixed".

**Completion conditions:**
- [ ] Evidence recorded in §13.
- [ ] Independent verification requested.

## 5. Execution Order and Dependencies

| Order | Task | Depends On | Parallel Safe |
|---|---|---|---|
| 1 | TASK-001 | None | Yes, with TASK-002 (disjoint files) |
| 2 | TASK-002 | None | Yes, with TASK-001 |
| 3 | TASK-003 | TASK-001, TASK-002 | No |
| 4 | TASK-004 | TASK-003 | No |

Recommendation: execute sequentially in this order. Parallelism gives negligible benefit at this size.

## 6. Testing Strategy

### Unit Tests

- `ConversionWarning` fields, defaults, immutability and equality.
- Default and backward-compatible construction of `DocumentConverterResult`.

### Integration Tests

- `MarkItDown().convert(path, detect_vector_graphics=...)` end to end across the new and existing PDF fixtures.

### Contract / End-to-End Tests

- `from markitdown import ConversionWarning`; `result.warnings` semantics (`None`, `[]`, populated).
- Failure path: pdfplumber raising leads to the incomplete warning while the Markdown still comes from the fallback.

### Regression Tests

- All existing tests unchanged and passing.
- Markdown equality with and without the option on every PDF fixture (AC-006).
- `warnings is None` by default on every existing PDF fixture and on a non-PDF input.

### Verification Commands

Run from `packages/markitdown/` unless stated.

| Check | Command | Expected Result |
|---|---|---|
| PDF tests | `hatch test tests/test_pdf.py` | All pass (baseline 37 passed, verified 2026-11-05) |
| New unit tests | `hatch test tests/test_conversion_warnings.py` | All pass |
| Full suite | `hatch test` | All pass (full-suite baseline not yet run; run before TASK-001 to separate pre-existing failures) |
| Format | `black --check .` (repository root) | No changes (black available; version not compared to the 26.10.1 pin) |
| Type checking | `hatch run types:check` | No new errors (required; environment to be created under GATE-1) |
| Build | Not applicable | — |

## 7. Security and Operational Considerations

### Security and Privacy

- No new parsing surface, since pdfplumber already processes every page.
- Warning messages are fixed constants with integer counts and page numbers. No PDF text or metadata goes into warnings.

### Data and Migrations

Not applicable. Backward compatibility comes from the keyword-only default.

### Reliability

- The counting must never cause conversion to fail. The incomplete path is covered by tests.
- The `check_complete` flag prevents a pdfminer-stage error from being misreported.

### Observability

Not applicable. Warnings are returned, not logged (spec).

### Deployment

Not applicable. This is library code in a fork; there is no release in this plan.

## 8. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Counting accidentally changes extraction output (for example through pdfplumber caching side effects) | Low | High | AC-006 equality tests over every fixture; counting reads properties only |
| Mis-reporting a complete check as incomplete when pdfminer fails | Medium (without a flag) | Medium | `check_complete` flag plus a dedicated test |
| Public API change breaks plugins | Low | Medium | Keyword-only with default; unit test for legacy construction |
| Hand-written PDF fixtures are malformed or differ across pdfplumber versions | Low | Low | Generator validated with pdfplumber counts; text extraction asserted |
| Curves inside form XObjects not counted | Unknown | Low | Fixture recorded as a known limitation (TASK-002) |
| mypy environment cannot be created (network) | Low | Medium | GATE-1 approved; if creation fails, stop and report, because type checking is required |

**Highest-risk step:** TASK-003, editing `PdfConverter.convert` around the `try`/`except` fallback.

**Stop and escalate if any of these happen:**
- Any existing test fails after the change.
- AC-006 equality fails.
- Meeting the spec would require changing the extraction logic.

**Rollback:** revert the three source files. The fixtures and tests are additive.

## 9. Specification Traceability

| Requirement | Acceptance Criterion | Implementation Task | Verification |
|---|---|---|---|
| FR-001 | AC-009 | TASK-001 | `test_conversion_warnings.py` |
| FR-002 | AC-005, AC-008 | TASK-001, TASK-003 | Unit tests; PDF and non-PDF tests |
| FR-003 | AC-002, AC-003 | TASK-002, TASK-003 | `test_pdf.py` curve and mixed fixtures |
| FR-004 | AC-004 | TASK-002, TASK-003 | Rule-only and existing fixtures give `[]` |
| FR-005 | AC-001 | TASK-003 | Existing suite plus `warnings is None` checks |
| FR-006 | AC-007 | TASK-003 | Mocked pdfplumber failure plus the pdfminer-failure case |
| FR-007 | AC-006 | TASK-003 | Markdown/title equality across fixtures |
| NFR Compatibility | AC-001, AC-008 | TASK-001, TASK-004 | Full suite, black, mypy |
| NFR Security (no content in warnings, no new deps) | — | TASK-003, TASK-004 | Assertions on fixed messages; `pyproject.toml` diff |
| NFR Performance (no work when disabled) | — | TASK-003 | Code review: counting is guarded by the flag. No benchmark; none required by the spec |

All requirements are covered. No unapproved scope.

## 10. Assumptions, Decisions and Blockers

### Confirmed Technical Assumptions

- Kwargs reach `PdfConverter.convert` unchanged.
- pdfplumber's classification behaves as the spec states.
- The existing fixtures contain zero curves.
- The baseline PDF tests pass.

### Unverified Assumptions

- Reading `page.curves`, `page.lines` and `page.rects` does not alter later `extract_words` or `extract_text` output. AC-006 tests this.
- Form XObject curves are counted (TASK-002).
- The full suite passes on the baseline.
- mypy currently passes on the baseline.

### Decisions Requiring Approval

- **GATE-1 (TASK-004): Approved** by Gary Bake, 2026-11-05. Create the `types` hatch environment (downloads from PyPI) and run mypy. Type checking is a required check: a mypy failure blocks completion, and it must not be reported as "Not run". Running `pre-commit` (which may download hooks) is also covered.

All design decisions are already approved in the spec (DD-1 to DD-7).

### Blocking Issues

None.

### Cognitive Ownership Decisions and Development (when enabled)

Not enabled. `policies/team-policy.md` is marked "Example; review before adopting", and the intent records no development objective. Required approvals, testing and independent verification are unaffected.

## 11. Implementation Progress

| Task | Status | Verification | Notes |
|---|---|---|---|
| TASK-001 | Pending | Not run | |
| TASK-002 | Pending | Not run | |
| TASK-003 | Pending | Not run | |
| TASK-004 | Pending | Not run | |

## 12. Plan Deviations

None recorded.

## 13. Final Verification Evidence

### Verification Results

| Check | Result | Evidence |
|---|---|---|
| Unit tests | Not run | |
| Integration tests | Not run | |
| Lint (black) | Not run | |
| Type checking (mypy) | Not run | |
| Acceptance criteria | Not evaluated | |

### Requirement Coverage

- [ ] Every approved requirement has been addressed.
- [ ] Acceptance criteria have been evaluated.
- [ ] Important failure scenarios have been checked.
- [ ] No unapproved scope changes remain.
- [ ] Security and operational concerns have been reviewed.

### Security Review

**Required:** No. No auth, secrets or new input surface; untrusted PDFs are already parsed by the same library. The reviewer may request one.

**Result:** Not run

### Independent Verification

**Verifier:** Not run

**Result:** Pending

**Outstanding issues:** —

**Changes since last verifier run:** None

## 14. Plan Review and Approval

**Decision:** Pending

**Reviewed by:** —

**Review date:** —

**Implementation authorised:** No

**Conditions:** —

**Approval notes:** —
