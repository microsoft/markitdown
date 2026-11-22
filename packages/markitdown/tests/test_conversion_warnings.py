"""ConversionWarning type and DocumentConverterResult.warnings compatibility."""

import copy
import dataclasses
import json
import logging
import pickle

import pytest

from markitdown import ConversionWarning, DocumentConverterResult


def test_conversion_warning_fields_and_defaults():
    w = ConversionWarning(
        code="VECTOR_GRAPHICS_PRESENT",
        severity=logging.WARNING,
        message="PDF contains vector graphics that may not be represented in Markdown.",
    )
    assert w.code == "VECTOR_GRAPHICS_PRESENT"
    assert w.severity == logging.WARNING
    assert logging.getLevelName(w.severity) == "WARNING"
    assert w.page is None
    assert dict(w.counts) == {}


def test_conversion_warning_is_immutable():
    w = ConversionWarning(code="X", severity=logging.INFO, message="m", page=2)
    with pytest.raises(dataclasses.FrozenInstanceError):
        w.page = 3  # type: ignore[misc]


def test_conversion_warning_counts_read_only():
    source = {"curves": 1}
    w = ConversionWarning("X", logging.WARNING, "m", counts=source)
    with pytest.raises(TypeError):
        w.counts["curves"] = 99  # type: ignore[index]
    source["curves"] = 5  # later changes to the caller's dict do not leak in
    assert w.counts["curves"] == 1


def test_conversion_warning_serialisable():
    w = ConversionWarning(
        "VECTOR_GRAPHICS_PRESENT", logging.WARNING, "m", page=1, counts={"curves": 2}
    )
    assert dataclasses.asdict(w) == {
        "code": "VECTOR_GRAPHICS_PRESENT",
        "severity": logging.WARNING,
        "message": "m",
        "page": 1,
        "counts": {"curves": 2},
    }
    assert json.loads(json.dumps(dataclasses.asdict(w)))["counts"] == {"curves": 2}
    # Safe: round-trips an object created in this test; no untrusted data.
    assert pickle.loads(pickle.dumps(w)) == w
    assert copy.deepcopy(w) == w
    restored = pickle.loads(pickle.dumps(w))
    with pytest.raises(TypeError):
        restored.counts["curves"] = 99  # type: ignore[index]


def test_conversion_warning_value_equality():
    a = ConversionWarning("X", logging.WARNING, "m", page=1, counts={"curves": 2})
    b = ConversionWarning("X", logging.WARNING, "m", page=1, counts={"curves": 2})
    c = ConversionWarning("X", logging.WARNING, "m", page=2, counts={"curves": 2})
    assert a == b
    assert a != c


def test_result_warnings_default_none():
    assert DocumentConverterResult("x").warnings is None


def test_result_legacy_construction_still_works():
    res = DocumentConverterResult(markdown="x", title="t")
    assert res.markdown == "x"
    assert res.title == "t"
    assert res.warnings is None


def test_result_stores_warnings():
    w = ConversionWarning("X", logging.INFO, "m")
    assert DocumentConverterResult("x", warnings=[w]).warnings == [w]
    assert DocumentConverterResult("x", warnings=[]).warnings == []
