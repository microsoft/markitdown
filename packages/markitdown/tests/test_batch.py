#!/usr/bin/env python3 -m pytest
# NOTE: importing from private module until Task 3 exports BatchConversionResult publicly
from markitdown._base_converter import BatchConversionResult, DocumentConverterResult


def test_batch_result_success_true():
    r = BatchConversionResult(
        source="test.txt",
        result=DocumentConverterResult(markdown="# Hello"),
    )
    assert r.success is True
    assert r.result is not None
    assert r.error is None


def test_batch_result_success_false():
    r = BatchConversionResult(source="test.txt", error=ValueError("oops"))
    assert r.success is False
    assert r.result is None
    assert r.error is not None


def test_batch_result_defaults():
    r = BatchConversionResult(source="test.txt")
    assert r.result is None
    assert r.error is None
    assert r.success is True


import os
import concurrent.futures

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


def test_convert_batch_basic():
    from markitdown import MarkItDown
    md = MarkItDown()
    sources = [
        os.path.join(TEST_FILES_DIR, "test.docx"),
        os.path.join(TEST_FILES_DIR, "test.pdf"),
        os.path.join(TEST_FILES_DIR, "test.pptx"),
    ]
    results = list(md.convert_batch(sources))
    assert len(results) == 3
    assert all(isinstance(r, BatchConversionResult) for r in results)
    assert all(r.success for r in results)
    assert all(isinstance(r.result, DocumentConverterResult) for r in results)
    assert {r.source for r in results} == set(sources)


def test_convert_batch_on_error_collect():
    from markitdown import MarkItDown
    md = MarkItDown()
    sources = [
        os.path.join(TEST_FILES_DIR, "test.docx"),
        os.path.join(TEST_FILES_DIR, "nonexistent_file_xyz.docx"),
    ]
    results = list(md.convert_batch(sources, on_error="collect"))
    assert len(results) == 2
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    assert len(successful) == 1
    assert len(failed) == 1
    assert failed[0].error is not None


def test_convert_batch_on_error_raise():
    import pytest
    from markitdown import MarkItDown
    md = MarkItDown()
    sources = [os.path.join(TEST_FILES_DIR, "nonexistent_file_xyz.docx")]
    raised = False
    try:
        list(md.convert_batch(sources, on_error="raise"))
    except Exception:
        raised = True
    assert raised, "Expected an exception to be raised"


def test_convert_batch_invalid_on_error():
    from markitdown import MarkItDown
    md = MarkItDown()
    raised = False
    try:
        list(md.convert_batch([], on_error="bad_value"))
    except ValueError as e:
        raised = True
        assert "on_error" in str(e)
    assert raised, "Expected ValueError"


def test_convert_batch_empty():
    from markitdown import MarkItDown
    md = MarkItDown()
    results = list(md.convert_batch([]))
    assert results == []


def test_convert_batch_custom_executor():
    from markitdown import MarkItDown
    md = MarkItDown()
    sources = [
        os.path.join(TEST_FILES_DIR, "test.docx"),
        os.path.join(TEST_FILES_DIR, "test.pdf"),
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(md.convert_batch(sources, executor=executor))
    assert len(results) == 2
    assert all(r.success for r in results)


def test_convert_batch_workers_param():
    from markitdown import MarkItDown
    md = MarkItDown()
    sources = [
        os.path.join(TEST_FILES_DIR, "test.docx"),
        os.path.join(TEST_FILES_DIR, "test.pdf"),
    ]
    results = list(md.convert_batch(sources, workers=1))
    assert len(results) == 2
    assert all(r.success for r in results)
