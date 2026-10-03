# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from importlib.metadata import requires

from packaging.requirements import Requirement


def markitdown_requirements():
    return [
        requirement
        for value in requires("markitdown-mcp") or []
        if (requirement := Requirement(value)).name == "markitdown"
    ]


def test_base_install_does_not_require_optional_converters():
    requirements = [
        requirement
        for requirement in markitdown_requirements()
        if requirement.marker is None or requirement.marker.evaluate({"extra": ""})
    ]
    assert len(requirements) == 1
    assert requirements[0].extras == set()


def test_all_extra_enables_converters_with_the_same_version_range():
    requirements = markitdown_requirements()
    base = next(
        requirement for requirement in requirements if requirement.marker is None
    )
    optional = [
        requirement
        for requirement in requirements
        if requirement.marker is not None
        and requirement.marker.evaluate({"extra": "all"})
    ]
    assert len(optional) == 1
    assert optional[0].extras == {"all"}
    assert optional[0].specifier == base.specifier


def test_mcp_tool_converts_html_without_optional_converters():
    from markitdown_mcp.__main__ import convert_to_markdown

    result = asyncio.run(convert_to_markdown("data:text/html,%3Ch1%3EHello%3C%2Fh1%3E"))
    assert result.strip() == "# Hello"
