# Intent: Optional PDF vector-graphics diagnostic

**ID:** pdf-vector-graphics-diagnostic
**Author:** Gary Bake
**Status:** Approved
**Created:** 2026-11-05

## 1. Problem

When MarkItDown converts a PDF to Markdown, it extracts text and tables only. Vector graphics such as charts, diagrams, flowcharts and drawn figures are discarded without any indication that they existed.

Developers using MarkItDown (often to feed documents into LLM or search pipelines) cannot tell from the result whether a page contained important visual content that is missing from the Markdown. A converted document can therefore look complete while silently omitting information, and there is no programmatic signal to trigger review, an alternative conversion path or a human check.

Evidence: inspection of `PdfConverter` confirms that no graphics or image information reaches `DocumentConverterResult`, which currently carries only `markdown` and `title`. No sample PDFs demonstrating real-world impact have been collected yet (see Open Questions).

## 2. Desired Outcome

A developer can opt in to a diagnostic when converting a PDF and receive, alongside the unchanged Markdown, a per-page indication of whether the page appears to contain meaningful vector graphics, with counts of the relevant drawing objects. This lets them identify pages where conversion may have omitted important visual information.

The diagnostic is delivered through a new optional `warnings` field on the conversion result, designed so other converters can populate it in future. For example:

```python
result = md.convert("architecture.pdf")
print(result.warnings)
```

Each warning carries at least a code, a severity and a human-readable message, for example:

```json
{
  "code": "VECTOR_GRAPHICS_PRESENT",
  "severity": "warning",
  "message": "PDF contains vector graphics that may not be represented in Markdown."
}
```

When the option is not enabled, conversion behaves exactly as it does today.

### Cognitive Ownership (when enabled)

**Delivery objective:** The opt-in, per-page vector-graphics diagnostic described above.

**Development objective:** Not yet decided (see Open Questions).

**Development budget / constraints:** Per `policies/team-policy.md` (currently an example policy, not adopted).

## 3. Users and Systems Affected

**Users:** Developers calling MarkItDown from Python who need to know whether PDF output may be incomplete. Existing users who do not enable the option should be unaffected.

**Systems:**
- `PdfConverter` (`packages/markitdown/src/markitdown/converters/_pdf_converter.py`)
- `DocumentConverterResult` (`packages/markitdown/src/markitdown/_base_converter.py`): shared by all converters; gains an optional field.
- Possibly the CLI (`__main__.py`), depending on an open decision.

## 4. Success Criteria

- [ ] With the option disabled (the default), the Markdown output and existing result attributes for every existing PDF test file are identical to current behaviour, and the existing test suite passes unchanged.
- [ ] With the option enabled, the result reports, for each page, whether meaningful vector graphics were detected, together with counts of the relevant drawing objects.
- [ ] Pages whose only vector content is table borders or decorative lines (for example rules, underlines, simple boxes) are not flagged.
- [ ] Pages containing a representative vector figure (for example a chart or diagram) are flagged.
- [ ] The new field defaults to a "not checked" state. Converters that do not populate it continue to work unchanged, and "not checked" is distinguishable from "checked, no graphics detected".
- [ ] Enabling the option does not change the Markdown content produced. The diagnostic appears only in the new field, preserving backward compatibility.

## 5. Constraints

- **Compatibility:** Existing conversions must continue to work unchanged. The diagnostic is opt-in and off by default.
- **Public API:** The new result field must be optional and backward compatible for all converters and any third-party plugin converters that construct `DocumentConverterResult`.
- **Field name and shape:** The new result field is named `warnings`. Each entry includes `code`, `severity` and `message`; the PDF diagnostic uses code `VECTOR_GRAPHICS_PRESENT` and severity `warning`.
- **One warning per affected page:** `warnings` is a list containing one `VECTOR_GRAPHICS_PRESENT` warning for each affected page, carrying that page's number and drawing-object counts. This granularity was chosen as the most reusable by other converters.
- **Not checked versus nothing found:** `warnings` is `None` when no diagnostic ran, and an empty list when diagnostics ran and found nothing. `warnings` may later hold warnings from other checks or converters.
- **Typed warnings:** Entries are a typed object (not plain dicts) exposing at least `code`, `severity` and `message`, for API stability. Exact class name and additional fields are for design.
- **Distribution:** Fork-local; not currently intended for contribution to upstream microsoft/markitdown.
- **Generality:** The result field should be designed for future use by other converters, but only the PDF converter populates it in this change.
- **Detection heuristic:** Table borders and decorative lines are deliberately ignored, accepting that simple line-only charts may be missed. This trade-off may be revisited later.
- **Dependencies:** No new runtime dependencies are expected. The PDF converter already uses pdfplumber, which exposes drawing objects. (Assumption to confirm during design.)
- **Performance:** No measurable overhead when the option is disabled. Acceptable overhead when enabled is not yet defined.

## 6. Out of Scope

- Raster (embedded bitmap) images. These are also dropped today, but are deferred to keep this first step simple.
- Extracting, rendering, describing or captioning the graphics themselves (for example via LLM).
- Inserting placeholders or markers into the Markdown output.
- Bounding-box or location information for detected graphics.
- Populating the new result field from any converter other than PDF.
- Changing PDF text or table extraction behaviour.

## 7. Open Questions

- **Fallback path:** When pdfplumber fails and conversion falls back to pdfminer, should the diagnostic report "unavailable" for the document, or attempt detection another way?
- **CLI exposure:** Should the option be available from the command line in this first version, and if so, how is the diagnostic presented (for example on stderr)? Or is it Python API only?
- **Definition of "meaningful" graphics:** What exact signals and thresholds separate figures from borders and decoration? To be resolved in design, validated against sample PDFs.
- **Sample PDFs:** Are there real documents exhibiting the problem that can serve as reference fixtures? If not, synthetic fixtures will be needed.
- **Performance budget:** What overhead is acceptable when the option is enabled?
- **Cognitive Ownership:** Is there a development objective for this task, or None?

## 8. Supporting Context

- `packages/markitdown/src/markitdown/converters/_pdf_converter.py`: current PDF conversion (pdfplumber per-page pass, pdfminer whole-document path and exception fallback).
- `packages/markitdown/src/markitdown/_base_converter.py`: `DocumentConverterResult`.
- Existing opt-in kwarg precedent: `keep_data_uris`.
- Existing PDF tests: `packages/markitdown/tests/test_pdf.py` and fixtures in `packages/markitdown/tests/test_files/`.

## 9. Approval

**Decision:** Approved

**Approved by:** Gary Bake

**Decision date:** 2026-11-05

**Notes:** Decisions recorded 2026-11-05 by Gary Bake: diagnostic delivered via a new optional, general-purpose result field; per-page flag with counts; ignore table borders and decorative lines; Markdown output unchanged when enabled; new field defaults to "not checked"; raster images out of scope. Amended 2026-11-05 by Gary Bake: field named `warnings` with code/severity/message entries; not intended for upstream; one warning per affected page; `None` = not checked, empty list = checked with no findings; entries are typed objects.
