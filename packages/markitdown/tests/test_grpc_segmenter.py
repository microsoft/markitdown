from markitdown.grpc._segmenter import (
    BlockQuoteBlock,
    CodeBlock,
    HeadingBlock,
    HorizontalRuleBlock,
    ImageBlock,
    ListBlock,
    ParagraphBlock,
    TableBlock,
    segment_markdown,
)

SAMPLE_DOCUMENT = """# Quarterly Report

An **overview** paragraph spanning
two lines.

## Sales

| Region | Revenue |
| ------ | ------- |
| East   | 100     |
| West   | 200     |

- First item
- Second item
  with continuation

1. Step one
2. Step two

```python
print("hello")
```

> A wise quote
> on two lines.

![Chart](https://example.com/chart.png "Q3 chart")

---

Closing remarks.
"""


def test_segments_full_document_in_order():
    blocks = list(segment_markdown(SAMPLE_DOCUMENT))
    kinds = [type(block).__name__ for block in blocks]
    assert kinds == [
        "HeadingBlock",
        "ParagraphBlock",
        "HeadingBlock",
        "TableBlock",
        "ListBlock",
        "ListBlock",
        "CodeBlock",
        "BlockQuoteBlock",
        "ImageBlock",
        "HorizontalRuleBlock",
        "ParagraphBlock",
    ]


def test_heading_levels_and_text():
    blocks = list(segment_markdown("# Title\n\n### Sub"))
    assert blocks == [
        HeadingBlock(level=1, text="Title"),
        HeadingBlock(level=3, text="Sub"),
    ]


def test_table_rows_parsed_without_delimiter_row():
    markdown = "| A | B |\n| - | - |\n| 1 | 2 |"
    (table,) = segment_markdown(markdown)
    assert isinstance(table, TableBlock)
    assert table.rows == [["A", "B"], ["1", "2"]]
    assert table.markdown == markdown


def test_table_with_escaped_pipe():
    (table,) = segment_markdown("| A\\|B | C |\n| --- | --- |\n| 1 | 2 |")
    assert table.rows[0] == ["A|B", "C"]


def test_unordered_list_items():
    (lst,) = segment_markdown("- one\n- two\n- three")
    assert isinstance(lst, ListBlock)
    assert not lst.ordered
    assert lst.items == ["one", "two", "three"]


def test_ordered_list_items():
    (lst,) = segment_markdown("1. one\n2. two")
    assert lst.ordered
    assert lst.items == ["one", "two"]


def test_nested_list_stays_with_parent_item():
    (lst,) = segment_markdown("- parent\n  - child\n- sibling")
    assert lst.items == ["parent\n- child", "sibling"]


def test_adjacent_lists_of_different_type_are_separate_blocks():
    blocks = list(segment_markdown("- bullet\n1. number"))
    assert [type(b).__name__ for b in blocks] == ["ListBlock", "ListBlock"]
    assert not blocks[0].ordered
    assert blocks[1].ordered


def test_code_block_language_and_content():
    (code,) = segment_markdown('```python\nprint("x")\n```')
    assert code == CodeBlock(language="python", code='print("x")')


def test_unterminated_code_block_consumes_remainder():
    (code,) = segment_markdown("```\nline1\nline2")
    assert code.code == "line1\nline2"


def test_image_block_with_title():
    (image,) = segment_markdown('![Alt text](https://example.com/a.png "The title")')
    assert image == ImageBlock(
        alt_text="Alt text", url="https://example.com/a.png", title="The title"
    )


def test_image_inside_paragraph_is_not_extracted():
    (paragraph,) = segment_markdown("See ![icon](i.png) inline.")
    assert isinstance(paragraph, ParagraphBlock)


def test_block_quote_text():
    (quote,) = segment_markdown("> line one\n> line two")
    assert quote == BlockQuoteBlock(text="line one\nline two")


def test_horizontal_rule_variants():
    blocks = list(segment_markdown("---\n\n***\n\n___"))
    assert all(isinstance(block, HorizontalRuleBlock) for block in blocks)


def test_table_like_line_without_delimiter_is_paragraph():
    (paragraph,) = segment_markdown("| not | a table |")
    assert isinstance(paragraph, ParagraphBlock)


def test_empty_markdown_yields_nothing():
    assert list(segment_markdown("")) == []


def test_whitespace_only_markdown_yields_nothing():
    assert list(segment_markdown("\n  \n\t\n")) == []


def test_no_content_dropped():
    """Every non-blank source line must appear in some block."""
    blocks = list(segment_markdown(SAMPLE_DOCUMENT))
    combined = "\n".join(
        getattr(block, "text", "")
        + getattr(block, "markdown", "")
        + getattr(block, "code", "")
        + getattr(block, "alt_text", "")
        for block in blocks
    )
    for token in ("Quarterly Report", "overview", "East", "Step one", "hello", "wise"):
        assert token in combined
