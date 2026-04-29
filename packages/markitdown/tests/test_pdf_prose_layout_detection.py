def _make_fake_page(width: float, rows: list[list[dict]]):
    class FakePage:
        def __init__(self, width: float, rows: list[list[dict]]):
            self.width = width
            self._words = []
            for i, row in enumerate(rows):
                y_top = 50 + i * 12
                for w in row:
                    self._words.append(
                        {
                            "text": w["text"],
                            "x0": float(w["x0"]),
                            "x1": float(w["x0"]) + float(w.get("w", 12)),
                            "top": float(y_top),
                        }
                    )

        def extract_words(self, keep_blank_chars=True, x_tolerance=3, y_tolerance=3):
            return list(self._words)

    return FakePage(width=width, rows=rows)


def test_multicolumn_prose_falls_back_to_text_extraction():
    """Regression: wide multi-column prose should not be emitted as a table.

    This page shape mimics the failure mode from issue #120: many tentative
    columns are discovered across the page, but each row only uses a small
    fraction of them. That is typical of two-column prose with staggered word
    positions, not real form/table data.
    """

    from markitdown.converters._pdf_converter import _extract_form_content_from_words

    # Thirteen stable x positions across the page; each row only touches four of
    # them, which should be treated as sparse multi-column prose rather than a
    # dense table.
    x_positions = [50, 105, 160, 215, 270, 325, 380, 435, 490, 545, 600, 655, 710]
    rows = []
    for i in range(10):
        start = i
        selected = x_positions[start : start + 4]
        rows.append(
            [
                {"x0": selected[0], "text": f"alpha{i}"},
                {"x0": selected[1], "text": f"beta{i}"},
                {"x0": selected[2], "text": f"gamma{i}"},
                {"x0": selected[3], "text": f"delta{i}"},
            ]
        )

    fake_page = _make_fake_page(width=760, rows=rows)

    assert _extract_form_content_from_words(fake_page) is None


def test_wide_dense_table_is_still_extracted():
    """Wide but dense tables should survive the sparse-prose guard."""

    from markitdown.converters._pdf_converter import _extract_form_content_from_words

    x_positions = [50, 105, 160, 215, 270, 325, 380, 435, 490, 545, 600]
    rows = []
    for i in range(6):
        rows.append(
            [
                {"x0": x, "text": f"c{col}_{i}"}
                for col, x in enumerate(x_positions)
            ]
        )

    fake_page = _make_fake_page(width=660, rows=rows)
    output = _extract_form_content_from_words(fake_page)

    assert output is not None
    assert "|" in output

