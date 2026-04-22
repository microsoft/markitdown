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
