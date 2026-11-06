import io

from markitdown import MarkItDown


def test_extensionless_log_text_is_not_rendered_as_csv_table() -> None:
    content = (
        "2026-09-12 18:00:01 INFO boot ok\n"
        "2026-09-12 18:00:02 ERROR disk full\n"
    )

    result = MarkItDown(enable_plugins=False).convert_stream(
        io.BytesIO(content.encode("utf-8"))
    )

    assert result.markdown == content


def test_extensionless_comma_csv_is_still_rendered_as_table() -> None:
    content = "name,age\nAlice,30\n"

    result = MarkItDown(enable_plugins=False).convert_stream(
        io.BytesIO(content.encode("utf-8"))
    )

    assert result.markdown == "| name | age |\n| --- | --- |\n| Alice | 30 |"
