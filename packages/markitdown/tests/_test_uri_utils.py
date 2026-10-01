import pytest

import markitdown._uri_utils


class TestUriUtils:

    def test_file_uri_to_path(self):
        assert markitdown._uri_utils.file_uri_to_path("file://markitdown/tests/test_files/test.docx") == ("markitdown", "/tests/test_files/test.docx")

    def test_file_uri_to_path_raises_error(self):
        with pytest.raises(ValueError):
            markitdown._uri_utils.file_uri_to_path("https://google.com/")

    @pytest.mark.parametrize("uri, expected", [("data:,Hello%2C%20World%21", (None, {}, b"Hello, World!")),
                                               ("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==", ("text/plain", {}, b"Hello, World!")),
                                               ("data:text/plain;first=Hello;second=World,attributes%20with%20%3D", ("text/plain", {"first":"Hello", "second":"World"}, b"attributes with =")),
                                               ("data:text/plain;test_attribute,empty%20attribute", ("text/plain", {'test_attribute': ''}, b"empty attribute")),
                                               ])
    def test_parse_data_uri(self, uri, expected):
        assert markitdown._uri_utils.parse_data_uri(uri) == expected

    def test_parse_data_uri_raises_error_not_data_uri(self):
        with pytest.raises(ValueError):
            markitdown._uri_utils.parse_data_uri("https://google.com/")

    def test_parse_data_uri_raises_error_malformed_uri(self):
        with pytest.raises(ValueError):
            markitdown._uri_utils.parse_data_uri("data:Hello%2C%20World%21")