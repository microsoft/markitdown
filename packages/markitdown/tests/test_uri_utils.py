from markitdown._uri_utils import file_uri_to_path


def test_file_uri_to_path_decodes_percent_encoded_space() -> None:
    _, path = file_uri_to_path("file:///path/to/my%20file.txt")
    assert "my file.txt" in path
    assert "%20" not in path


def test_file_uri_to_path_decodes_percent_encoded_unicode() -> None:
    _, path = file_uri_to_path("file:///path/to/%E6%B5%8B%E8%AF%95.txt")
    assert "测试.txt" in path
    assert "%E6%B5%8B%E8%AF%95" not in path
