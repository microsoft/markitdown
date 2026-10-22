"""Tests for the YAML converter."""

import io
import pytest
from markitdown import MarkItDown


@pytest.fixture
def md():
    return MarkItDown()


class TestYamlConverterBasic:
    """Basic YAML conversion tests."""

    def test_simple_key_value(self, md):
        """Simple key-value pairs should convert to labeled blocks."""
        yaml_content = b"name: John\nage: 30\ncity: New York"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        md_text = result.markdown
        assert "**name:** John" in md_text
        assert "**age:** 30" in md_text
        assert "**city:** New York" in md_text

    def test_nested_mapping(self, md):
        """Nested mappings should use bold labels with proper hierarchy."""
        yaml_content = b"person:\n  name: Alice\n  address:\n    city: Boston\n    zip: \"02101\""
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        md_text = result.markdown
        assert "**person:**" in md_text
        assert "**name:** Alice" in md_text
        assert "**city:** Boston" in md_text
        assert "**zip:** 02101" in md_text

    def test_sequence_of_mappings_table(self, md):
        """Sequence of mappings with uniform keys must render as a Markdown table with pipes and separators."""
        yaml_content = (
            b"- name: Bob\n  age: 25\n"
            b"- name: Carol\n  age: 28\n"
            b"- name: Dave\n  age: 35"
        )
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        md_text = result.markdown
        assert "|" in md_text, "Table must use pipe characters"
        lines = [l.strip() for l in md_text.strip().split("\n") if l.strip()]
        table_lines = [l for l in lines if l.startswith("|")]
        assert len(table_lines) >= 3, "Table must have header + separator + data rows"
        assert "---" in table_lines[1], "Second row must be separator"
        header_cells = [c.strip().lower() for c in table_lines[0].split("|") if c.strip()]
        assert "name" in header_cells
        assert "age" in header_cells
        for name in ["bob", "carol", "dave"]:
            assert name in md_text.lower()

    def test_yaml_extension(self, md):
        """Both .yaml and .yml extensions should work."""
        yaml_content = b"key: value"
        for ext in [".yaml", ".yml"]:
            result = md.convert_stream(io.BytesIO(yaml_content), file_extension=ext)
            assert result.markdown.strip() != ""

    def test_yml_extension(self, md):
        """YML extension should produce same output as YAML."""
        yaml_content = b"key: value"
        r1 = md.convert_stream(io.BytesIO(yaml_content), file_extension=".yaml")
        r2 = md.convert_stream(io.BytesIO(yaml_content), file_extension=".yml")
        assert r1.markdown.strip() == r2.markdown.strip()


class TestYamlConverterEdgeCases:
    """Edge case tests for YAML converter."""

    def test_empty_yaml(self, md):
        """Empty YAML should not crash and should return a result."""
        yaml_content = b""
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert result is not None
        assert isinstance(result.markdown, str)

    def test_scalar_value(self, md):
        """A single scalar string value should be in the output."""
        yaml_content = b'"just a string"'
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "just a string" in result.markdown

    def test_deeply_nested(self, md):
        """Deeply nested structures should render all levels."""
        yaml_content = b"a:\n  b:\n    c:\n      d:\n        e: deep_value"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "deep_value" in result.markdown.lower()
        assert "**a:**" in result.markdown

    def test_special_characters(self, md):
        """YAML with special characters should be handled."""
        yaml_content = b"message: \"Hello World!\"\npath: /usr/local/bin"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "hello world" in result.markdown.lower()

    def test_multiline_string(self, md):
        """Multiline YAML strings should be preserved."""
        yaml_content = b"description: |\n  This is line one.\n  This is line two.\n  This is line three."
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "line one" in result.markdown.lower()
        assert "line two" in result.markdown.lower()
        assert "line three" in result.markdown.lower()

    def test_list_of_scalars(self, md):
        """A list of scalar values should use bullet points."""
        yaml_content = b"- apple\n- banana\n- cherry"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        md_text = result.markdown
        assert "- " in md_text, "Lists should use bullet points"
        assert "apple" in md_text.lower()
        assert "banana" in md_text.lower()
        assert "cherry" in md_text.lower()

    def test_mixed_types_in_list(self, md):
        """Lists with mixed types should not crash."""
        yaml_content = b"- 42\n- hello\n- true\n- 3.14"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "42" in result.markdown
        assert "hello" in result.markdown.lower()

    def test_null_values(self, md):
        """YAML null values should be rendered as 'null'."""
        yaml_content = b"name: test\nvalue: null"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "**name:** test" in result.markdown
        assert "**value:** null" in result.markdown

    def test_boolean_values(self, md):
        """YAML booleans should be rendered as lowercase."""
        yaml_content = b"enabled: true\ndisabled: false"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "**enabled:** true" in result.markdown
        assert "**disabled:** false" in result.markdown

    def test_numeric_types(self, md):
        """YAML numeric types should be rendered as strings."""
        yaml_content = b"integer: 42\nfloat: 3.14\nnegative: -10"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "**integer:** 42" in result.markdown
        assert "**float:** 3.14" in result.markdown
        assert "**negative:** -10" in result.markdown

    def test_multiple_documents(self, md):
        """Multiple YAML documents separated by --- should be handled in order."""
        yaml_content = b"first: one\n---\nsecond: two"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        md_lower = result.markdown.lower()
        first_pos = md_lower.find("first")
        second_pos = md_lower.find("second")
        assert first_pos != -1, "Should contain 'first'"
        assert second_pos != -1, "Should contain 'second'"
        assert first_pos < second_pos, "Documents should appear in order"

    def test_anchor_and_alias(self, md):
        """YAML anchors and aliases should be resolved."""
        yaml_content = b"defaults: &defaults\n  adapter: postgres\n  host: localhost\ndevelopment:\n  <<: *defaults"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "postgres" in result.markdown.lower()
        assert "localhost" in result.markdown.lower()

    def test_complex_key(self, md):
        """YAML with complex (quoted) keys should be handled."""
        yaml_content = b"\"quoted key\": value\n'another key': other"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "value" in result.markdown.lower()
        assert "other" in result.markdown.lower()

    def test_flow_mapping(self, md):
        """YAML flow mappings {key: value} should be handled."""
        yaml_content = b"inline: {name: test, value: 42}"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "test" in result.markdown.lower()
        assert "42" in result.markdown

    def test_flow_sequence(self, md):
        """YAML flow sequences [1, 2, 3] should be handled."""
        yaml_content = b"items: [apple, banana, cherry]"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "apple" in result.markdown.lower()
        assert "banana" in result.markdown.lower()
        assert "cherry" in result.markdown.lower()

    def test_mixed_table_and_non_table(self, md):
        """A list of dicts with different keys should use bullets, not a table."""
        yaml_content = (
            b"- name: Bob\n  age: 25\n"
            b"- city: Boston\n  zip: 02101"
        )
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        md_text = result.markdown
        table_lines = [l for l in md_text.strip().split("\n") if l.strip().startswith("|")]
        assert len(table_lines) < 3, "Non-uniform dicts should not render as table"

    def test_multiline_folded_string(self, md):
        """YAML folded multiline strings should be preserved."""
        yaml_content = b"description: >\n  This is a long\n  description that\n  spans multiple lines"
        result = md.convert_stream(
            io.BytesIO(yaml_content), file_extension=".yaml"
        )
        assert "long" in result.markdown.lower()
        assert "description" in result.markdown.lower()
